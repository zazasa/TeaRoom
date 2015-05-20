# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20150520_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='Number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('Course', 'Number')]),
        ),
    ]
