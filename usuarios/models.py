from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Modelo de Programa educativo
class ProgramaEducativo(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=15)
    def __str__(self):
        return self.nombre

# Modelo de Perfil de usuario
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apellido_materno = models.CharField(max_length=50, blank=True)
    programa_educativo = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE)
    nivel_acceso = models.IntegerField(default=1)

    def __str__(self):
        return f'{ self.user.username } - { self.user.first_name } { self.user.last_name } { self.apellido_materno }'

    def save(self,*args, **kwargs) -> None:
        super().save(*args, **kwargs)
        
        # Convertir a mayusculas 
        self.user.first_name = self.user.first_name.upper()
        self.user.last_name = self.user.last_name.upper()
        self.apellido_materno = self.apellido_materno.upper()
        self.user.save()