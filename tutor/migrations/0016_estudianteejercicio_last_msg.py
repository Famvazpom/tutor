# Generated by Django 3.2.15 on 2023-03-18 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0015_estudiantetema_maestria'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudianteejercicio',
            name='last_msg',
            field=models.TextField(blank=True, null=True),
        ),
    ]