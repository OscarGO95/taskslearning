# Generated by Django 2.0.5 on 2018-06-23 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskLearning', '0006_tarea_activa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='image',
            field=models.ImageField(upload_to='media/profileImages'),
        ),
    ]
