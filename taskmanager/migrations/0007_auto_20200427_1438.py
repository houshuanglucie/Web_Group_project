# Generated by Django 2.1.15 on 2020-04-27 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0006_auto_20200427_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Responsable'),
        ),
    ]
