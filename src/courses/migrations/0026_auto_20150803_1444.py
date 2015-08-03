# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_remove_assignment_has_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='Penality_percent',
            new_name='Penalty_percent',
        ),
    ]
