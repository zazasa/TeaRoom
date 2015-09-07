# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assigned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Sate_assigned', models.DateField(auto_now_add=True)),
                ('Assigned_by', models.CharField(verbose_name=b'Assigned By', max_length=50, null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Assigned',
                'verbose_name_plural': '5-Assigned',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UniqueString', models.CharField(default=b'None', max_length=50, verbose_name=b'UniqueString')),
                ('Title', models.CharField(max_length=50, verbose_name=b'Title')),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Activation_date', models.DateField(null=True, blank=True)),
                ('Due_date', models.DateTimeField(null=True, blank=True)),
                ('Hard_date', models.DateTimeField(null=True, blank=True)),
                ('Penalty_percent', models.IntegerField(null=True, blank=True)),
                ('Folder_path', models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Assignment',
                'verbose_name_plural': '3-Assignments',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50, verbose_name=b'Course Name')),
                ('Year', models.IntegerField()),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Start_date', models.DateField()),
                ('End_date', models.DateField()),
                ('Enrollment_due_date', models.DateField()),
                ('Is_always_open', models.BooleanField()),
                ('Is_always_active', models.BooleanField()),
                ('Description', models.TextField()),
                ('Folder_path', models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': '1-Courses',
            },
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Date_joined', models.DateField(auto_now_add=True)),
                ('Course', models.ForeignKey(to='courses.Course')),
                ('Student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Enrolled',
                'verbose_name_plural': '2-Enrolled',
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Description', models.CharField(max_length=50, null=True, verbose_name=b'Description', blank=True)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Number', models.IntegerField()),
                ('Points', models.IntegerField(null=True, blank=True)),
                ('Folder_path', models.CharField(verbose_name=b'Folder_path', max_length=200, null=True, editable=False, blank=True)),
                ('Submit_key', models.CharField(verbose_name=b'Submit key', max_length=25, editable=False)),
                ('Group', models.CharField(default=b'None', max_length=50, verbose_name=b'Group')),
                ('Assignment', models.ForeignKey(to='courses.Assignment')),
                ('Students', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='courses.Assigned')),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': '4-Exercises',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Creation_date', models.DateTimeField(auto_now_add=True)),
                ('Pass', models.BooleanField(default=False)),
                ('Parser_output', models.TextField(default=b'', editable=False)),
                ('Exercise', models.ForeignKey(to='courses.Exercise', null=True)),
                ('User', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': '6-Results',
            },
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50, verbose_name=b'Filename')),
                ('Folder_path', models.CharField(max_length=200, null=True, verbose_name=b'Folder_path', blank=True)),
                ('Type', models.CharField(max_length=50, verbose_name=b'Type')),
                ('Exercise', models.ForeignKey(to='courses.Exercise')),
            ],
            options={
                'verbose_name': 'UserFile',
                'verbose_name_plural': '7-UserFiles',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='Students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='courses.Enrolled'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='Course',
            field=models.ForeignKey(to='courses.Course'),
        ),
        migrations.AddField(
            model_name='assigned',
            name='Exercise',
            field=models.ForeignKey(to='courses.Exercise'),
        ),
        migrations.AddField(
            model_name='assigned',
            name='Student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userfile',
            unique_together=set([('Exercise', 'Name')]),
        ),
        migrations.AlterUniqueTogether(
            name='exercise',
            unique_together=set([('Assignment', 'Number')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrolled',
            unique_together=set([('Student', 'Course')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('Name', 'Year')]),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('Course', 'UniqueString')]),
        ),
        migrations.AlterUniqueTogether(
            name='assigned',
            unique_together=set([('Student', 'Exercise')]),
        ),
    ]
