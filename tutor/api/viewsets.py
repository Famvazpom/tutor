from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from tutor.models import Materia, Tema, Explicacion, Ejercicio
from .serializers import *

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = []

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
    permission_classes = []

class ExplicacionViewSet(viewsets.ModelViewSet):
    queryset = Explicacion.objects.all()
    serializer_class = ExplicacionSerializer
    permission_classes = []

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = []
