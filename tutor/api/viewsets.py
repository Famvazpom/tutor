from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from tutor.models import Materia, Tema, Explicacion, Ejercicio
from usuarios.models import Perfil
from .serializers import *

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaTemaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaExplicacionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

class ExplicacionViewSet(viewsets.ModelViewSet):
    queryset = Explicacion.objects.all()
    serializer_class = ExplicacionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

class EjercicioAdmonViewSet(viewsets.ModelViewSet):
    queryset = EstudianteEjercicio.objects.all()
    serializer_class = EstudianteEjercicioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

    def get_queryset(self):
        return super().get_queryset() if self.request.user.is_superuser else super().get_queryset().filter(estudiante=self.request.user.perfil)

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication,]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
