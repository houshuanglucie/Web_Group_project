# Generated by Django 2.1.15 on 2020-05-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0023_auto_20200508_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]
