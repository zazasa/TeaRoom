# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0023_exercise_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='UniqueString',
            field=models.CharField(default=b'None', max_length=50, verbose_name=b'UniqueString'),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('Course', 'UniqueString')]),
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='Number',
        ),
    ]
