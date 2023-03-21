# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name node_base.py
@create->time 2023/3/19-22:11
@desc->
++++++++++++++++++++++++++++++++++++++ """
import abc
from base.c_resource import CResource
from base.c_result import CResult
from base.c_utils import CUtils


class NodeBase(CResource, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        self.input_list = None
        self.output_list = []
        self.params = None

    @abc.abstractmethod
    def help(self):
        return '''
        算法名称: 抽象基类
        分属类别：base
        算法作用：这是所有node算法的基类，通过继承abc类，实现对node算法的约束
        算法接收参数
        {
            "input": [],
            "output": [],
            "params": {
                "test1": "test",
                "test2": "test2"
            }
        }
        '''

    @abc.abstractmethod
    def check_params(self):
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "this is a check_params test"
        )

    def check_input(self):
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "this is a check_input test"
        )

    def run(self):
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "this is a _run test"
        )

    def get_config(self, node_config):
        self.input_list = CUtils.get_input(node_config)
        self.params = CUtils.get_params(node_config)

    def update_output(self, output_obj):
        self.output_list.append(output_obj)

    def save_ouput(self):
        ...

    @classmethod
    def run_test(cls, node_config):
        class_obj = cls()
        class_obj.get_config(node_config)
        class_obj.run()
