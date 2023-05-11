# Generated by Django 3.2.15 on 2023-05-04 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_perfil_nivel_acceso'),
        ('tutor', '0020_explicacion_detalles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.perfil')),
            ],
        ),
    ]
