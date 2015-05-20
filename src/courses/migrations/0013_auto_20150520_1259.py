# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20150520_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile',
            name='Path',
        ),
        migrations.AddField(
            model_name='assignment',
            name='Folder_path',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Folder_path', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='Folder_path',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Folder_path', blank=True),
        ),
        migrations.AddField(
            model_name='userfile',
            name='Folder_path',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Folder_path', blank=True),
        ),
    ]
