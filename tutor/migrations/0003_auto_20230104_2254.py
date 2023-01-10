# Generated by Django 3.2.15 on 2023-01-04 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_tema_function'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ejercicio',
            old_name='descripcion',
            new_name='enunciado',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='titulo',
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='respuesta',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]