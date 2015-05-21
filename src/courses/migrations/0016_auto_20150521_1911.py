# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0015_exercise_folder_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assigned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Sate_assigned', models.DateField(auto_now_add=True)),
                ('Assigned_by', models.CharField(max_length=50, verbose_name=b'Assigned By')),
            ],
            options={
                'verbose_name': 'Enrolled',
                'verbose_name_plural': '2-Enrolled',
            },
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Folder_path',
            field=models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='Folder_path',
            field=models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='Folder_path',
            field=models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='assigned',
            name='Exercise',
            field=models.ForeignKey(to='courses.Exercise'),
        ),
        migrations.AddField(
            model_name='assigned',
            name='Student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exercise',
            name='Students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='courses.Assigned'),
        ),
    ]
