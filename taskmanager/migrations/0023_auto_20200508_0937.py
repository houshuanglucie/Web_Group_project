# Generated by Django 2.1.15 on 2020-05-08 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0022_auto_20200508_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trace',
            name='object_task',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskmanager.Task', verbose_name='Tache'),
        ),
    ]
