# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20150518_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50, verbose_name=b'Filename')),
                ('Path', models.FilePathField()),
                ('Type', models.CharField(max_length=50, verbose_name=b'Type')),
            ],
            options={
                'verbose_name': 'UserFile',
                'verbose_name_plural': 'UserFiles',
            },
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='Exercise_folder',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='File_to_test',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Activation_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Due_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Hard_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AddField(
            model_name='userfile',
            name='Exercise',
            field=models.ForeignKey(to='courses.Exercise'),
        ),
    ]
