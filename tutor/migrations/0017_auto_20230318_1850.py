# Generated by Django 3.2.15 on 2023-03-18 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0016_estudianteejercicio_last_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudianteejercicio',
            name='last_msg',
        ),
        migrations.AddField(
            model_name='estudiantetema',
            name='last_msg',
            field=models.TextField(blank=True, null=True),
        ),
    ]
