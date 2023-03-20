# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name compress_file.py
@create->time 2023/3/20-15:30
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_result import CResult
from node.base.node_base import NodeBase


class CompressFile(NodeBase):
    def __init__(self, node_json):
        super().__init__(node_json)

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

    def check_params(self):
        result = super().check_params()
        if not CResult.result_result(result):
            return result

    def check_input(self):
        result = super().check_input()
        if not CResult.result_result(result):
            return result

    def _run(self):
        result = super()._run()
        if not CResult.result_result(result):
            return result

