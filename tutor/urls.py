from django.urls import path,include
from tutor.api.viewsets import *
from django.contrib.auth.decorators import login_required,permission_required
from tutor.views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register('materia',MateriaViewSet)
router.register('temas',TemaViewSet)
router.register('explicaciones',ExplicacionViewSet)
router.register('estudiante',EstudianteViewSet)

urlpatterns = [
    # [------------- API --------------] # 
    path('api/',include(router.urls)),
    path('api/ejercicio/',EjercicioAPIView.as_view()),
]