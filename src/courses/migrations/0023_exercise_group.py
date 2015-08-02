# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_auto_20150524_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='Group',
            field=models.CharField(default=b'None', max_length=50, verbose_name=b'Group'),
        ),
    ]
