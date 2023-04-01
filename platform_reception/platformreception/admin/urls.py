# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_reception
@editor->name Sanliy
@file->name urls.py
@create->time 2023/3/27-13:37
@desc->
++++++++++++++++++++++++++++++++++++++ """

from django.urls import path
from . import views


# app_name = "admin"
urlpatterns = [
    path('control', views.control, name="control"),
    path('index', views.index, name="index"),
    path('check', views.post, name="check")
]