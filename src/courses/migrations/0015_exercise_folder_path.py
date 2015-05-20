# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20150520_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='Folder_path',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Folder_path', blank=True),
        ),
    ]
