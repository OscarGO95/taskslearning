# Generated by Django 2.0.5 on 2018-06-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskLearning', '0005_auto_20180622_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='activa',
            field=models.BooleanField(default=True),
        ),
    ]
