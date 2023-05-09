# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_utils.py
@create->time 2023/3/20-14:40
@desc->
++++++++++++++++++++++++++++++++++++++ """
import re
import uuid
from base.c_json import CJson
from base.c_resource import CResource
from c_mysql import CMysql


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

    @classmethod
    def one_id(cls):
        return uuid.uuid4().hex

    @classmethod
    def replace_params(cls, old_params, replaced_params):
        matches = re.findall(r"(?<=\$\{params).*?(?=\})", old_params)
        cj = CJson()
        cj.load(replaced_params)
        for i in matches:
            i = "params" + i
            old_params = old_params.replace("${" + i + "}", cj.json_path_one(i))
        return eval(old_params)

    @classmethod
    def replace_output(cls, params:dict, workflow_id):
        matches = re.findall(r"(?<=\$\{).*?(?=\})", str(params))
        for one_match in matches:
            node_model_name = one_match.split(".")[0]
            one_config_name = one_match.split(".")[1]
            cm = CMysql()
            node_config = cm.fetchall(
                '''
                select node_config from python_platform.do_nodes where workflow_id =:workflow_id and node_model_name =:node_model_name
                ''', {
                    "workflow_id": workflow_id,
                    "node_model_name": node_model_name
                }
            )[0][0]
            cj = CJson()
            cj.load(node_config)
            for replace_key_name, replace_value_name in params.items():
                if replace_value_name == "${" + one_match + "}":
                    params[replace_key_name] = cj.json_path_one(one_config_name)
        return params



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

