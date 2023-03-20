# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_result.py
@create->time 2023/3/19-22:30
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_json import CJson


class CResult:

    @classmethod
    def merge_result(cls, result_result, result_messag):
        result = dict()
        result["result_result"] = result_result,
        result["message"] = result_messag
        cj = CJson()
        cj.load(result)
        return cj

    @classmethod
    def result_msg(cls, result):
        return result.json_path_one("message")

    @classmethod
    def result_result(cls, result):
        return result.json_path_one("result_result")


if __name__ == '__main__':
    result = CResult.merge_result(
        1,
        "test"
    )
    result_result = CResult.result_result(result)
    print(result_result)
