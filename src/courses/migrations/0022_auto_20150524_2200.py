# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_auto_20150524_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='Creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
