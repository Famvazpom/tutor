from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from tutor.api.serializers import EjercicioSerializer
from tutor.models import Ejercicio,Tema
from tutor.sistema_experto.Ejercicios.EjProdNotFact import rand_fact, mix_fact_1, mix_fact_2


class GenerarEjercicioApiView(APIView):
    """
    Genera un ejercicio aleatorio y se le asigna al usuario.

    * Requiere autenticacion.
    """
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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