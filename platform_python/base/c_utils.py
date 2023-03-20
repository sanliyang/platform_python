# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_utils.py
@create->time 2023/3/20-14:40
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_json import CJson
from base.c_resource import CResource

class CUtils:

    @classmethod
    def get_input(cls, node_json):
        cj = CJson()
        cj.load(node_json)
        return cj.json_path_one(CResource.NODE_INPUT)

    @classmethod
    def get_params(cls, node_json):
        cj = CJson()
        cj.load(node_json)
        return cj.json_path_one(CResource.NODE_PARAMS)

    @classmethod
    def get_output(cls, node_json):
        cj = CJson()
        cj.load(node_json)
        return cj.json_path_one(CResource.NODE_OUTPUT)