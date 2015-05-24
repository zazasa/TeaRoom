# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_auto_20150524_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='Submit_key',
            field=models.CharField(verbose_name=b'Submit key', max_length=25, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='userfile',
            unique_together=set([('Exercise', 'Name')]),
        ),
    ]
