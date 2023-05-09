# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name node_connector.py
@create->time 2023/5/3-17:55
@desc->
++++++++++++++++++++++++++++++++++++++ """
import importlib

from base.c_result import CResult
from base.c_utils import CUtils
from node.base.node_base import NodeBase


class NodeConnector(NodeBase):
    def __init__(self):
        super().__init__()
        self.node = []

    def help(self):
        return '''
                算法名称: node节点连接器
                分属类别：connect
                算法作用：连接两个node节点
                算法接收参数
                {
                    "input": [],
                    "output": [],
                    "params": {
                        "workflow_id": "aaa",
                        "node": [
                            {
                                "class_name": "GetWeather",
                                "node_type": "weather",
                                "model_name": "get_weather",
                                "config": {
                                    "input": [],
                                    "output": [],
                                    "params": {
                                        "city": "北京"
                                    }
                                }
                            },
                            {
                                "class_name": "QQEmailSend",
                                "node_type": "mail",
                                "model_name": "qq_email_send",
                                "config": {
                                    "input": ["xxxxxxxxxxxx"],
                                    "output": [],
                                    "params": {
                                        "email_title": "这是一个测试邮件",
                                        "email_content": "<html><head></head><body><h1>Hello, World!</h1><p>这是一封 HTML 邮件。</p></body></html>",
                                        "email_type": "html",
                                        "email_annex": "D:/工具/新建文本文档.html",
                                        "email_annex_type": "html"
                                    }
                                }
                            }
                        ]
                    }
                }
                '''

    def check_params(self):
        result = super().check_params()
        if CResult.result_faild(result):
            return result
        if self.params is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "请选择设置算法的参数， 因为有一些必要参数未设置，算法将停止运行，请检查后重试!"
            )
        self.node = CUtils.dict_value_by_name(self.params, "node", [])
        if not self.node:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "部分参数未设置，算法将停止运行，请检查后重试!"
            )

        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入参数检查成功，算法将继续运行..."
        )

    def connect(self):
        for one_node in self.node:
            class_name = CUtils.dict_value_by_name(one_node, "class_name", None)
            node_type = CUtils.dict_value_by_name(one_node, "node_type", None)
            model_name = CUtils.dict_value_by_name(one_node, "model_name", None)
            config = CUtils.dict_value_by_name(one_node, "config", None)

            try:
                node_obj = importlib.import_module(f"node.{node_type}.{model_name}")
                class_obj = getattr(node_obj, class_name)
                class_obj.run_test(config)
            except Exception as error:
                return CResult.merge_result(
                    self.RESULT_FAILD,
                    f"{node_type}.{model_name}.{class_name}导包失败，具体原因是{error},请检查后重试!"
                )

        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "所有算法均已在此执行完毕!"
        )

    def run(self):
        result = super().run()
        if CResult.result_faild(result):
            return result
        connect_result = self.connect()
        return connect_result


if __name__ == '__main__':
    NodeConnector.run_test(
        '''
        {
                    "input": [],
                    "output": [],
                    "params": {
                        "node": [
                            {
                                "class_name": "GetWeather",
                                "node_type": "weather",
                                "model_name": "get_weather",
                                "config": {
                                    "input": [],
                                    "output": [],
                                    "params": {
                                        "city": "北京"
                                    }
                                }
                            },
                            {
                                "class_name": "GetWeather",
                                "node_type": "weather",
                                "model_name": "get_weather",
                                "config": {
                                    "input": [],
                                    "output": [],
                                    "params": {
                                        "city": "郑州"
                                    }
                                }
                            }
                        ]
                    }
                }
        '''
    )
