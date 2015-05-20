# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20150520_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='Points',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
