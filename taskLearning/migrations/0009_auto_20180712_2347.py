# Generated by Django 2.0.5 on 2018-07-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskLearning', '0008_estudiante_isvisiblegame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='isvisibleGame',
            field=models.BooleanField(default=False),
        ),
    ]