from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from tutor.models import Materia, Tema, Explicacion, Ejercicio,EstudianteEjercicio,EstudianteTema
from django.contrib.auth import authenticate

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        exclude = ( "function","materia")

class ExplicacionSerializer(serializers.ModelSerializer):
    anterior = serializers.SerializerMethodField()
    siguiente = serializers.SerializerMethodField()
    class Meta:
        model = Explicacion
        exclude = ( "tema",)

    def get_anterior(self,obj):
        return reverse_lazy('explicacion-detail',kwargs={'pk':obj.anterior.pk}) if obj.anterior else None
    
    def get_siguiente(self,obj):
        return reverse_lazy('explicacion-detail',kwargs={'pk':obj.siguiente.pk}) if obj.siguiente else None

class TemaExplicacionSerializer(serializers.ModelSerializer):
    explicacion = serializers.SerializerMethodField()
    class Meta:
        model = Tema
        exclude = ( "function","materia")
    
    def get_explicacion(self,obj):
        explicacion = Explicacion.objects.filter(tema=obj).last()
        return ExplicacionSerializer(explicacion).data

class MateriaTemaSerializer(serializers.ModelSerializer):
    temas = serializers.SerializerMethodField()
    class Meta:
        model = Materia
        fields = '__all__'

    def get_temas(self,obj):
        temas = Tema.objects.filter(materia=obj)
        return TemaExplicacionSerializer(temas,many=True).data

class EjercicioSerializer(serializers.ModelSerializer):
    tema = TemaSerializer()
    class Meta:
        model = Ejercicio
        fields = '__all__'

class EstudianteEjercicioSerializer(serializers.ModelSerializer):
    ejercicio = EjercicioSerializer()
    class Meta:
        model = EstudianteEjercicio
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs