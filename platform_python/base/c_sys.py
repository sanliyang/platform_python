# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_sys.py
@create->time 2023/4/21-23:08
@desc->
++++++++++++++++++++++++++++++++++++++ """
import os


class CSys:

    @classmethod
    def get_pid(cls):
        return os.getpid()

    @classmethod
    def get_gid(cls):
        return os.getgid()
