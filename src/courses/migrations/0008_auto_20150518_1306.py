# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20150518_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='Activation_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Due_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Hard_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
