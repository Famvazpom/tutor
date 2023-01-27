from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate, login
from tutor.api.serializers import EjercicioSerializer,LoginSerializer
from tutor.models import Ejercicio,Tema
from tutor.sistema_experto.Ejercicios.EjProdNotFact import rand_fact, mix_fact_1, mix_fact_2


class GenerarEjercicioApiView(APIView):
    """
    Genera un ejercicio aleatorio y se le asigna al usuario.

    * Requiere autenticacion.
    """
    permission_classes = [JSONWebTokenAuthentication,]

    def get(self, request,tema=None):
        """
        Genera un ejercicio aleatorio y lo devuelve en formato JSON
        """
        if not tema:
            return Response(
                {"detail": "Must provide a Tema."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            solved = False
            tema = Tema.objects.get(pk=tema)

            # Iterar hasta que se genere un ejercicio que no este resuelto
            while not solved:
                example = rand_fact(t=tema.function).getData()
                solved = False if ('not_solvd' in example.keys()) else True
                    
            ejercicio = Ejercicio.objects.create(
                tema=tema,
                enunciado=example['question'],
                respuesta=example['dataToAssess']['ans'],
                alumno=request.user.perfil,
            )

            ejercicio = Ejercicio.objects.filter(tema=tema).order_by('?').first()
            serializer = EjercicioSerializer(ejercicio)
            return Response(serializer.data)

        except Tema.DoesNotExist:
            return Response(
                {"detail": "Tema does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class GenerarEjercicioExplicadoApiView(APIView):
    """
    Genera un ejercicio aleatorio y se le asigna al usuario.

    * Requiere autenticacion.
    """
    permission_classes = [JSONWebTokenAuthentication,]

    def get(self, request,tema=None):
        """
        Genera un ejercicio aleatorio y lo devuelve en formato JSON
        """
        if not tema:
            return Response(
                {"detail": "Must provide a Tema."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            solved = False
            tema = Tema.objects.get(pk=tema)

            # Iterar hasta que se genere un ejercicio que no este resuelto
            while not solved:
                example = rand_fact(t=tema.function).getData()
                solved = False if ('not_solvd' in example.keys()) else True
                    
            ejercicio = Ejercicio.objects.create(
                tema=tema,
                enunciado=example['question'],
                respuesta=example['dataToAssess']['ans'],
                alumno=request.user.perfil,
            )

            ejercicio = Ejercicio.objects.filter(tema=tema).order_by('?').first()
            serializer = EjercicioSerializer(ejercicio)
            return Response(serializer.data)

        except Tema.DoesNotExist:
            return Response(
                {"detail": "Tema does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

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