# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_project.py
@create->time 2023/4/20-16:41
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_file import CFile
from base.c_resource import CResource


class CProject:

    @classmethod
    def project_path(cls):
        return CFile.path_dir_path(CFile.path_dir_path(CFile.get_absolute_path(__file__)))

    @classmethod
    def config_path(cls):
        return CFile.path_join(cls.project_path(), CResource.CONFIG_NAME)