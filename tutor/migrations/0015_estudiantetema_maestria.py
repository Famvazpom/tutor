# Generated by Django 3.2.15 on 2023-03-14 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0014_estudianteejercicio_correctos'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiantetema',
            name='maestria',
            field=models.FloatField(default=0),
        ),
    ]