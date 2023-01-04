from django.urls import path,include
from tutor.api.viewsets import *
from django.contrib.auth.decorators import login_required,permission_required
from rest_framework import routers

router = routers.SimpleRouter()

router.register('materias',MateriaViewSet)
router.register('temas',TemaViewSet)
router.register('explicaciones',ExplicacionViewSet)

urlpatterns = [
    # [------------- API --------------] # 
    path('api/',include(router.urls))
]