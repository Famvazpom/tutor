# Generated by Django 3.2.15 on 2023-01-04 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tema',
            name='function',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]