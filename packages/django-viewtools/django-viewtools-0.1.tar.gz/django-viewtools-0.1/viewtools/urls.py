# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns

from viewtools import views

urlpatterns = patterns('',
    (r'^db_error/$', views.db_error),
    (r'^py_error/$', views.py_error),
)
