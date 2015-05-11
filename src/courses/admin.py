#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 16:35:37
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-11 17:00:11

from django.contrib import admin
# Register your models here.
from .models import *


class CourseAdmin(admin.ModelAdmin):
    '''
        Admin View for Course
    '''

admin.site.register(Course, CourseAdmin)
