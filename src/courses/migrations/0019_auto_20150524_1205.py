# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_auto_20150521_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='Submit_key',
            field=models.CharField(default=0, verbose_name=b'Submit secret key', max_length=25, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='Pass',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='assigned',
            unique_together=set([('Student', 'Exercise')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrolled',
            unique_together=set([('Student', 'Course')]),
        ),
    ]
