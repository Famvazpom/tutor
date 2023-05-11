from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate, login
from django.utils.timezone import now
from tutor.api.serializers import ExplicacionSerializer,LoginSerializer,EstudianteEjercicioSerializer,RequestSerializer
from tutor.api.exceptions import *
from tutor.models import Ejercicio,Tema,EstudianteEjercicio,EstudianteTema,Explicacion,Requests
from usuarios.models import Perfil
import pandas as pd
import numpy as np
import pickle
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
    

class ExplicacionAPIView(APIView):
    
    def get(self,request):
        tema = request.GET.get('tema',None)
        # Verificar la existencia de TEMA en GET, esto solo aplica si no se proporciona un ID
        if not tema:
            return Response(NoTheme.default_detail,status=NoTheme.status_code)
       
        # Se obtiene la dificultad del estudiante con respecto al tema
        tema = Tema.objects.get(pk=tema)
        estudiante,_ = EstudianteTema.objects.get_or_create(tema=tema,estudiante=request.user.perfil)
        # Si no se proporciona un ID, se selecciona un ejercicio aleatorio del tema en base
        # a la dificultad del estudiante
        nivel = estudiante.nivel
        ejercicio = None

        # Se buscan ejercicios de la dificultad del estudiante, si no se encuentran se buscan de dificultad menor
        while not ejercicio and nivel > 0:
            ejercicio = Explicacion.objects.filter(tema=tema,dificultad=estudiante.nivel,anterior=None)
            nivel -= 1

        # Si no se encuentran ejercicios se envia error
        if not ejercicio:
            return Response(NotExplain.default_detail,status=NoEjercicio.status_code)
        
        ejercicio = random.choice(ejercicio)    

        return Response(ExplicacionSerializer(ejercicio).data)
    
class EjercicioAPIView(APIView):

    def dump_roster(self,roster):
        with open('bkt-roster.pkl','wb') as f:
            pickle.dump(roster,f,protocol=pickle.HIGHEST_PROTOCOL)

    def create_model_roster(self):
        # Crear modelo bkt
        # Se obtienen todos los ejercicios y se crea un dataframe con los datos
        ejercicios = EstudianteEjercicio.objects.all()
        df = pd.DataFrame.from_records(ejercicios.values())
        
        # Se obtiene una lista de temas y se asigna al dataframe
        temas = [ f'{i.ejercicio.tema.__str__()} - { i.ejercicio.dificultad }' for i in ejercicios ]
        single = np.unique(temas).tolist()
        df['tema'] =  temas
        del df['fecha_inicio']
        del df['fecha_fin']
        df.to_csv('dataset.csv')
        del df

        df = pd.read_csv('dataset.csv')
        # Se asigna el valor correcto al dataframe, 0 si el estudiante no lo resolvió y 1 si lo resolvió y -1 si no lo intentó
        df['correcto'] = np.where((df['intentos'] == 0 ),-1,df['correcto'])
        df['Annon Student Id'] = df['estudiante_id']
        

        
        # Se crea el modelo y se ajustan los datos
        model = Model(seed = 50,num_fits=5)
        defaults = {'order_id': 'id','user_id':'estudiante_id' ,'skill_name': 'tema', 'correct': 'correcto'}
        model.fit(data=df,defaults = defaults)
        # Se guarda el modelo en un archivo pickle
        model.save('bkt-model.pkl')
        
        # Crear Roster
        estudiantes = list(df.estudiante_id.unique())
        temas = list(df.tema.unique())
        roster = Roster(students=estudiantes, skills = single, model = model,mastery_state=.8)
        roster.students = estudiantes
        roster.skills = temas
        # Se guarda el roster en un archivo pickle
        self.dump_roster(roster)
        # Liberar memoria
        return roster

    def get_or_create_model_roster(self):
        # Crear el modelo de BKT o cargarlo si ya existe
        try:
            with open('bkt-roster.pkl','rb') as f:
                roster = pickle.load(f)

        except IOError:
            roster = self.create_model_roster()
           
        return roster
    
    def get_status(self,ejercicio):
        # Si el ejercicio es correcto se envia un 1, si no se envia un 0 si no se contesto es -1
        return 1 if ejercicio.correcto == 1 else 0

    def update_difficulty(self,estudiante,tema,ejercicio):
        # Se obtiene el roster
        roster = self.get_or_create_model_roster()
        skill = f'{ejercicio.ejercicio.tema.__str__()} - { ejercicio.ejercicio.dificultad }'
        student = estudiante.pk
        # Se actualiza el roster con el ejercicio resuelto
        try:
            # Intentar actualizar estado
            roster.update_state(skill, student,self.get_status(ejercicio))

        except ValueError as e:
            # Si no existe skill, crear modelo de nuevo
            if 'skill not found' in str(e): 
                
                roster = self.create_model_roster()
            
            # Agregar estudiante y actualizar su estado
            if 'student name not found' in str(e):
                roster.add_student(skill,student)
                roster.update_state(skill, student,self.get_status(ejercicio))

        maestria = roster.get_mastery_prob(skill, estudiante.pk)

        # Se actualiza la dificultad del estudiante en base a la maestria del tema
        estudiantes_tema,_ = EstudianteTema.objects.get_or_create(tema=tema,estudiante=estudiante)
        if maestria > .80:
            estudiantes_tema.last_msg = 'Subir de nivel'
            estudiantes_tema.nivel = ejercicio.ejercicio.dificultad + 1
        elif maestria < .20:
            estudiantes_tema.last_msg = 'Bajar de nivel'
            estudiantes_tema.nivel = max(ejercicio.ejercicio.dificultad - 1,1)
        else:
            estudiantes_tema.last_msg = 'Mantener nivel'

        estudiantes_tema.maestria = maestria
        estudiantes_tema.save()
        del roster
        
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
        #estudiante_ejercicio,_ = EstudianteEjercicio.objects.get_or_create(ejercicio=ejercicio,estudiante=request.user.perfil)
        # Crear ejercicio sin importar si ya fue resuelto?
        estudiante_ejercicio = EstudianteEjercicio.objects.create(ejercicio=ejercicio,estudiante=request.user.perfil)

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
    
class RequestAPIView(APIView):
    
    def get(self,request):
        obj,_ = Requests.objects.get_or_create(estudiante=request.user.perfil)
        return Response(RequestSerializer(obj).data)
  
    def post(self, request, format=None):
        obj,_ = Requests.objects.get_or_create(estudiante=request.user.perfil)
        # Si es admin no hay limite
        if request.user.perfil.nivel_acceso == 3:
            obj.cantidad +=1
            obj.save()
            return Response(RequestSerializer(obj).data)
        
        # En todos los demas casos se limita a 10
        if obj.cantidad < 10:
            obj.cantidad +=1
            obj.save()
            return Response(RequestSerializer(obj).data)
        else:
            return Response(RequestLimit.default_detail, status=RequestLimit.status_code)
  