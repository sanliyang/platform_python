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

from base.c_mysql import CMysql
from base.c_resource import CResource
from base.c_result import CResult
from base.c_utils import CUtils


class NodeBase(CResource, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        self.input_list = None
        self.output_list = []
        self.params = None
        self.node_id = None
        self.node_config = None
        self.cm = CMysql()

    def get_node_id(self, node_id):
        self.node_id = node_id

    def update_status(self, node_status):
        self.cm.execute(
            '''
            update python_platform.do_nodes 
            set node_status =:node_status 
            where node_id =:node_id
            ''', {
                "node_status": node_status,
                "node_id": self.node_id
            }
        )

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
            "check_params 方法调用初始化！"
        )

    def check_input(self):
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "check_input 方法调用初始化！"
        )

    def run(self):
        if self.node_id is not None:
            self.update_status(CResource.NODE_PROCESS)
        self.get_node_config()
        self.get_config(None)
        result_check_input = self.check_input()
        result_check_params = self.check_params()
        result = CResult.result_xor(result_check_input, result_check_params)
        return result

    def get_node_config(self):
        """
        从数据库中读取当前任务的配置
        :return:
        """
        try:
            self.node_config = self.cm.fetchall(
                '''
                select node_config from python_platform.do_nodes where node_id =:node_id
                ''', {
                    "node_id": self.node_id
                }
            )[0][0]
        except:
            self.node_config = None

    def get_config(self, node_config):
        if self.node_config is None:
            self.node_config = node_config
        if self.node_config is not None:
            self.input_list = CUtils.get_input(self.node_config)
            self.params = CUtils.get_params(self.node_config)

    def update_output(self, output_obj):
        if type(output_obj) == str:
            self.output_list.append(output_obj)
        if type(output_obj) == list:
            self.output_list = output_obj

    def save_ouput(self):
        self.cm.execute(
            '''
            update python_platform.do_nodes 
            set node_config = JSON_ARRAY_APPEND(node_config, '$.output', :output) where node_id =:node_id
            ''', {
                "output": self.output_list,
                "node_id": self.node_id
            }
        )

    @classmethod
    def run_test(cls, node_config):
        class_obj = cls()
        class_obj.get_config(node_config)
        class_obj.run()
