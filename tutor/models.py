import re
from django.db import models
from usuarios.models import Perfil
from .math2speech import math2speech
from django.conf import settings 
m2s = math2speech()

# Create your models here.
# Modelo de Materia
class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=15)
    def __str__(self):
        return self.nombre

# Modelo de Tema
class Tema(models.Model):
    nombre = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

# Modelo de Explicacion
class Explicacion(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    voz = models.FileField(upload_to='media/voz/',max_length=50,blank=True, null=True)
    anterior = models.ForeignKey('self', related_name='explicacion_anterior',on_delete=models.CASCADE, blank=True, null=True)
    siguiente = models.ForeignKey('self', related_name='explicacion_siguiente',on_delete=models.CASCADE, blank=True, null=True)
    
    def get_audiofile(self):
        filename = f'{self.id}_{self.titulo.replace(" ","_")}.mp3'
        voicename = f'{settings.MEDIA_ROOT}/voz/{filename}'
        result = re.split('\\\\begin{equation}\\r\\n(.*)\\r\\n\\\\end{equation}', self.descripcion)
        final = []
        for i in result:
            final += re.split('\$(.*)\$',i)
            
            
        for id,text in enumerate(final):
            if id > 0 and id%2==1:
                math = math2speech()
                c = math.procesaCadena(text,[char for char in text if char.isalpha()])
                final[id] = math.obtenCadena(0,c['arbol'])

        m2s.generaAudio(''.join(final),filename=voicename)
        return f'voz/{filename}'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.voz = self.get_audiofile()
        return super().save(*args, **kwargs)

# Modelo de Ejercicio
class Ejercicio(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Perfil, on_delete=models.CASCADE) #Alumno al que se le asigno el ejercicio
    
    def __str__(self):
        return self.titulo