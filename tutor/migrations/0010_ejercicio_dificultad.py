# Generated by Django 3.2.15 on 2023-02-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0009_remove_ejercicio_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercicio',
            name='dificultad',
            field=models.IntegerField(default=1),
        ),
    ]
