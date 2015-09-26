#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 16:35:37
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-09-26 19:05:53

from django.contrib import admin
from django.conf import settings

# Register your models here.
from .models import *


class CourseAdmin(admin.ModelAdmin):
    '''
        Admin View for Course
    '''

    list_display = ('course_full_name', 'Start_date', 'End_date',
                    'Enrollment_due_date', 'id')
    readonly_fields = ('Folder_path',)
    list_filter = []

    def course_full_name(self, obj):
        return obj


class EnrolledAdmin(admin.ModelAdmin):
    '''
        Admin View for Enrolled
    '''
    list_display = ('Course', 'Student', 'Date_joined')

    def __init__(self, *args, **kwargs):
        super(EnrolledAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


class AssignmentAdmin(admin.ModelAdmin):
    '''
        Assignment View for Course
    '''

    list_display = ('Title', 'Creation_date', 'Activation_date', 'Course')
    readonly_fields = ('Folder_path',)
    list_filter = []

# from django.contrib.admin.helpers import ActionForm
# from django import forms
# class ExerciseFormAdmin(ActionForm):
#     price = forms.IntegerField(required=False)


class ExerciseAdmin(admin.ModelAdmin):
    '''
        Exercise View for Course
    '''

    list_display = ('id', 'Number', 'Description', 'Assignment', 'file_to_complete_list', 'file_to_test_list', 'parser_list')
    readonly_fields = ('Folder_path',)

    list_filter = []

    # action_form = ExerciseFormAdmin

    def file_to_complete_list(self, obj):
        dataSet = UserFile.objects.filter(Exercise=obj, Type='to_complete')
        filelist = []
        for item in dataSet:
            filelist.append(item.Name)
        return ','.join(filelist)
    file_to_complete_list.short_description = 'To Complete'

    def file_to_test_list(self, obj):
        dataSet = UserFile.objects.filter(Exercise=obj, Type='to_test')
        filelist = []
        for item in dataSet:
            filelist.append(item.Name)
        return ','.join(filelist)
    file_to_test_list.short_description = 'To Test'

    def parser_list(self, obj):
        dataSet = UserFile.objects.filter(Exercise=obj, Type='parser')
        filelist = []
        for item in dataSet:
            filelist.append(item.Name)
        return ','.join(filelist)
    parser_list.short_description = 'Parser'


class AssignedAdmin(admin.ModelAdmin):
    '''
        Admin View for Enrolled
    '''
    list_display = ('Student', 'Exercise', 'Assigned_by')

    def __init__(self, *args, **kwargs):
        super(AssignedAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'Assigned_by', None) is None:
            obj.Assigned_by = request.user
            print request.user
        obj.save()


class UserFileAdmin(admin.ModelAdmin):
    '''
        Admin View for UserFile
    '''

    def __init__(self, *args, **kwargs):
        super(UserFileAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


class ResultAdmin(admin.ModelAdmin):
    '''
        Admin View for Result
    '''
    list_display = ('User', 'Exercise', 'Creation_date', 'Pass', 'Submit_by')
    readonly_fields = ('User', 'Exercise', 'Pass', 'Creation_date', 'Parser_output')
        

if settings.ADMIN_SITE_URL:
    admin.site.site_url = settings.ADMIN_SITE_URL

admin.site.register(Enrolled, EnrolledAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(UserFile, UserFileAdmin)
admin.site.register(Assigned, AssignedAdmin)
