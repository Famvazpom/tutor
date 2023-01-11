from django.urls import path,include
from tutor.api.viewsets import *
from django.contrib.auth.decorators import login_required,permission_required
from tutor.views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register('materia',MateriaViewSet)
router.register('temas',TemaViewSet)
router.register('explicaciones',ExplicacionViewSet)
router.register('ejercicios',EjercicioViewSet)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('api/ejercicios/<int:tema>/generar',login_required(GenerarEjercicioApiView.as_view()),name='ejercicio'),
    # [------------- API --------------] # 
    path('api/',include(router.urls))
]