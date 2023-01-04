from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from tutor.models import Materia, Tema, Explicacion, Ejercicio


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class TemaSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()
    class Meta:
        model = Tema
        fields = '__all__'

class ExplicacionSerializer(serializers.ModelSerializer):
    tema = TemaSerializer()
    class Meta:
        model = Explicacion
        fields = '__all__'