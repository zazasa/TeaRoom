#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 17:31:12
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-09-11 16:05:32

from django.conf.urls import patterns, url


from . import views
urlpatterns = patterns('',
                       url(r'^upload-assignment/$', views.UploadAssignmentView.as_view(), name="upload-assigment"),
                       url(r'^upload-result/$', views.UploadResultView.as_view(), name="upload-result"),
                       url(r'^utils/$', views.UtilsView.as_view(), name="utils"),
                       url(r'^download-utils-file/$', views.DownloadUtilsFileView.as_view(), name="download-utils-file"),
                       )