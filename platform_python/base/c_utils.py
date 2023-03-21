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
    def get_input(cls, node_config):
        cj = CJson()
        cj.load(node_config)
        return cj.json_path(CResource.NODE_INPUT)

    @classmethod
    def get_params(cls, node_config):
        cj = CJson()
        cj.load(node_config)
        return cj.json_path_one(CResource.NODE_PARAMS)

    @classmethod
    def get_output(cls, node_config):
        cj = CJson()
        cj.load(node_config)
        return cj.json_path_one(CResource.NODE_OUTPUT)

    @classmethod
    def dict_value_by_name(cls, target_dict: dict, name, default_value=None):
        try:
            value = target_dict[name]
        except KeyError:
            value = default_value
        return value


if __name__ == '__main__':
    node_json = {
        "input": ["aa/bb", "cc/dd"],
        "output": [],
        "params": {
            "target_path": "aa/bb",
            "target_suffix": ".zip",
            "password": "123",
            "compress_level": 6
        }
    }
    print(type(node_json))

    print(type(CUtils.get_input(node_json)))
    print(CUtils.get_input(node_json))

    print(type(CUtils.get_params(node_json)))
    print(CUtils.dict_value_by_name(CUtils.get_params(node_json), "aa"))

    print(type(CUtils.get_output(node_json)))
    print(CUtils.get_output(node_json))

