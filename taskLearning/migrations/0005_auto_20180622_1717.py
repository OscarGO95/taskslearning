# Generated by Django 2.0.5 on 2018-06-22 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskLearning', '0004_auto_20180622_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='file',
            field=models.FileField(blank=True, upload_to='media/tareas'),
        ),
    ]