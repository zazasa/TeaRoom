#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 17:31:12
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 12:54:45

from django.conf.urls import patterns, url


from . import views
urlpatterns = patterns('',
                       url(r'^upload-assignment/$', views.UploadAssignmentView.as_view(), name="upload-assigment"),
                       url(r'^upload-result/$', views.UploadResultView.as_view(), name="upload-result"),
                       )