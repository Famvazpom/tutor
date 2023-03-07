from django.contrib import admin
from tutor.models import Materia, Tema, Explicacion, Ejercicio,EstudianteEjercicio,EstudianteTema

# Register your models here.
admin.site.register(Materia)
admin.site.register(Tema)
admin.site.register(Explicacion)
admin.site.register(Ejercicio)
admin.site.register(EstudianteTema)
admin.site.register(EstudianteEjercicio)

