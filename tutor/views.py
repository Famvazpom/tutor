from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate, login
from tutor.api.serializers import EjercicioSerializer,LoginSerializer
from tutor.models import Ejercicio,Tema
from tutor.sistema_experto.Ejercicios.EjProdNotFact import rand_fact, mix_fact_1, mix_fact_2


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