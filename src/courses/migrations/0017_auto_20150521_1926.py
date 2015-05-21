# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20150521_1911'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assigned',
            options={'verbose_name': 'Assigned', 'verbose_name_plural': '5-Assigned'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'Result', 'verbose_name_plural': '6-Results'},
        ),
        migrations.AlterModelOptions(
            name='userfile',
            options={'verbose_name': 'UserFile', 'verbose_name_plural': '7-UserFiles'},
        ),
        migrations.AlterField(
            model_name='assigned',
            name='Assigned_by',
            field=models.CharField(verbose_name=b'Assigned By', max_length=50, null=True, editable=False, blank=True),
        ),
    ]
