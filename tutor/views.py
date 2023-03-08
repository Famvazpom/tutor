from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate, login
from django.utils.timezone import now
from tutor.api.serializers import EjercicioSerializer,LoginSerializer,EstudianteEjercicioSerializer
from tutor.api.exceptions import *
from tutor.models import Ejercicio,Tema,EstudianteEjercicio,EstudianteTema
from tutor.sistema_experto.Ejercicios.EjProdNotFact import rand_fact, mix_fact_1, mix_fact_2
import pandas as pd
import numpy as np
from pyBKT.models import Model, Roster

import random

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    

class EjercicioAPIView(APIView):

    def update_difficulty(self,estudiante,tema,ejercicio):
        # Se filtran los ejercicios del tema y se crea un dataframe con los datos
        ejercicios = EstudianteEjercicio.objects.filter(ejercicio__tema=tema)
        df = pd.DataFrame.from_records(ejercicios.values())
        temas = [ f'{i.ejercicio.tema.__str__()} - { i.ejercicio.dificultad }' for i in ejercicios ]
        single = list(np.unique(temas))
        df['tema'] =  temas
        df['correcto'] = np.where((df['intentos'] == 0 ),-1,df['correcto'])

        # Se crea el modelo y se entrena con los datos del dataframe
        model = Model(seed=25)
        defaults = {'order_id': 'id','user_id':'estudiante_id' ,'skill_name': 'tema', 'correct': 'correcto'}
        model.fit(data=df,defaults = defaults)
        
        # Se crea un roster con los estudiantes y se obtiene la probabilidad de dominio del estudiante


        roster = Roster(students = [estudiante.pk], skills = single, model = model)
        maestria = roster.get_mastery_prob(f'{ejercicio.ejercicio.tema.__str__()} - { ejercicio.ejercicio.dificultad }', estudiante.pk)

        # Se actualiza la dificultad del estudiante en base a la maestria del tema
        if maestria > .80:

            estudiantes_tema,_ = EstudianteTema.objects.get_or_create(tema=tema,estudiante=estudiante)
            estudiantes_tema.nivel = ejercicio.ejercicio.dificultad + 1
            estudiantes_tema.save()
        
        if maestria < .20:

            estudiantes_tema,_ = EstudianteTema.objects.get_or_create(tema=tema,estudiante=estudiante)
            estudiantes_tema.nivel = max(ejercicio.ejercicio.dificultad - 1,1)
            estudiantes_tema.save()
        return
    
    def get(self,request):
        id = request.GET.get('id')
        tema = request.GET.get('tema')
        
        # Verificar la existencia de TEMA en GET, esto solo aplica si no se proporciona un ID
        if not tema and not id:
            return Response(NoTheme.default_detail,status=NoTheme.status_code)

        # Verificar si el estudiante ya tiene un ejercicio de ese tema
        if id:
            try:
                ejercicio = EstudianteEjercicio.objects.get(pk=id)
                serializer = EstudianteEjercicioSerializer(ejercicio)
                return Response(serializer.data)
            except EstudianteEjercicio.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Se obtiene la dificultad del estudiante con respecto al tema
        tema = Tema.objects.get(pk=tema)
        estudiante,_ = EstudianteTema.objects.get_or_create(tema=tema,estudiante=request.user.perfil)
        # Si no se proporciona un ID, se selecciona un ejercicio aleatorio del tema en base
        # a la dificultad del estudiante
        nivel = estudiante.nivel
        ejercicio = None

        # Se buscan ejercicios de la dificultad del estudiante, si no se encuentran se buscan de dificultad menor
        while not ejercicio and nivel > 0:
            ejercicio = Ejercicio.objects.filter(tema=tema,dificultad=estudiante.nivel)
            nivel -= 1

        # Si no se encuentran ejercicios se envia error
        if not ejercicio:
            return Response(NoEjercicio.default_detail,status=NoEjercicio.status_code)
        
        ejercicio = random.choice(ejercicio)    

        # Se verifica si el ejercicio ya fue contestado por el estudiante anteriormente, en caso de no existir un registro se crea
        estudiante_ejercicio,_ = EstudianteEjercicio.objects.get_or_create(ejercicio=ejercicio,estudiante=request.user.perfil)

        return Response(EstudianteEjercicioSerializer(estudiante_ejercicio).data)
    
    def post(self,request):
        id = request.GET.get('id') 
        respuesta = request.GET.get('answer') 
        if not id:
            return Response(NoID.default_detail,status=NoID.status_code)
        
        if not respuesta:
            return Response(NoAnswer.default_detail,status=NoAnswer.status_code)

        # Se obtiene el ejercicio y se verifica si existe
        try:
            ejercicio = EstudianteEjercicio.objects.get(pk=id)
        except EstudianteEjercicio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Se verifica si el ejercicio corresponde al estudiante que hace la request
        if ejercicio.estudiante != request.user.perfil:
            return Response(NotMatch.default_detail,status=NotMatch.status_code)
        
        # Se verifica si la respuesta es correcta y se agregan valores a los atributos del ejercicio
        if ejercicio.ejercicio.respuesta == respuesta.__str__():
            ejercicio.correcto = True
            ejercicio.correctos += 1
            ejercicio.primera_respuesta = True if ejercicio.intentos == 0 else False # Correcto en la primera respuesta
            ejercicio.intentos +=1
            ejercicio.fin = now()
        else:
            ejercicio.correcto = False
            ejercicio.intentos +=1
        ejercicio.save()

        self.update_difficulty(request.user.perfil,ejercicio.ejercicio.tema,ejercicio)
        return Response(EstudianteEjercicioSerializer(ejercicio).data)