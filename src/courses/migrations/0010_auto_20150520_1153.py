# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20150520_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='Has_due_date',
            field=models.BooleanField(default=False),
        ),
    ]
