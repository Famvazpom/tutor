import re
import json
from django.db import models
from usuarios.models import Perfil
from .math2speech import math2speech
from django.conf import settings 
m2s = math2speech()

# Create your models here.
# Modelo de Materia
class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    corto = models.CharField(max_length=50,blank=True,null=True)
    codigo = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.corto = self.nombre[:10]
        return super().save(*args, **kwargs)

# Modelo de Tema
class Tema(models.Model):
    nombre = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    function = models.CharField(max_length=50,blank=True, null=True)
    clave = models.CharField(max_length=50,blank=True, null=True)

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
        id = Explicacion.objects.last().pk + 1 if self._state.adding else self.id
        
        filename = f'{id}_{self.titulo.replace(" ","_")}.mp3'
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
    enunciado = models.TextField()
    respuesta = models.TextField()
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    opciones = models.TextField(blank=True, null=True)
    dificultad = models.IntegerField(default=1)

    def set_opciones(self, x):
        self.opciones = json.dumps(x)

    def get_opciones(self):
        return json.loads(self.opciones)

    def __str__(self):
        return f'{self.pk} - {self.enunciado}'

# Modelo de EstudianteTema (Relacion entre un estudiante y un tema)
class EstudianteTema(models.Model):
    estudiante = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=1) # Utilizado para determinar el nivel de dificultad de los ejercicios
    maestria = models.FloatField(default=0)
    
    def __str__(self):
        return f'{self.estudiante} - {self.tema}'
    
class EstudianteEjercicio(models.Model):
    estudiante = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    correcto = models.BooleanField(default=False) # Ya respondido correctamente
    correctos = models.IntegerField(verbose_name="VecesCorrecto",default=0) # Cuantas veces ha respondido correctamente
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(auto_now=True)
    intentos = models.IntegerField(default=0) # Cuantas veces lo ha realizado
    primera_respuesta = models.BooleanField(default=False) # Correcto al primer intento

    def __str__(self):
        return f'{self.estudiante} - {self.ejercicio} - {self.ejercicio.dificultad}'
