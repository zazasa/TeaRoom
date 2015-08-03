# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_auto_20150802_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='Has_due_date',
        ),
    ]
