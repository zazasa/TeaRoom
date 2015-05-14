#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 17:31:12
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-13 15:28:37

from django.conf.urls import patterns, url


from . import views
urlpatterns = patterns('',
                       url(r'^course-list/$', views.CourseListView.as_view(), name="course-list"),
                       url(r'^help/$', views.HelpView.as_view(), name="help"),
                       )