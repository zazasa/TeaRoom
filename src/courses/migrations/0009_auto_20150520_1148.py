# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20150518_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='Description',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Penality_percent',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
