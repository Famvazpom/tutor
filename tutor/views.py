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
            ejercicio.primera_respuesta = True if ejercicio.intentos == 0 else False # Correcto en la primera respuesta
            ejercicio.intentos +=1
            ejercicio.fin = now()
        else:
            ejercicio.correcto = False
            ejercicio.intentos +=1
        ejercicio.save()

        return Response(EstudianteEjercicioSerializer(ejercicio).data)