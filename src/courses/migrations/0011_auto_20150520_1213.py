# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20150520_1153'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='exercise',
            unique_together=set([('Assignment', 'Number')]),
        ),
    ]
