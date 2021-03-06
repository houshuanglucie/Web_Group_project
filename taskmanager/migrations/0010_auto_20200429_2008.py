# Generated by Django 2.1.15 on 2020-04-29 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0009_auto_20200429_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='file/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='taskmanager.Category', verbose_name='Catégorie'),
        ),
    ]
