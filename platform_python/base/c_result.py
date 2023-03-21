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
from base.c_resource import CResource


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

    @classmethod
    def result_sucess(cls, result):
        return result.json_path_one("result_result") == CResource.RESULT_SUCCESS

    @classmethod
    def result_faild(cls, result):
        return result.json_path_one("result_result") == CResource.RESULT_FAILD

    @classmethod
    def result_xor(cls, result1, result2=None):
        if result2 is None:
            return result1
        result_result1 = cls.result_result(result1)
        result_result2 = cls.result_result(result2)
        if result_result1 ^ result_result2 != 0:
            return CResult.merge_result(
                CResource.RESULT_FAILD,
                [CResult.result_msg(result1), CResult.result_msg(result2)]
            )
        else:
            return CResult.merge_result(
                result_result1,
                [CResult.result_msg(result1), CResult.result_msg(result2)]
            )


if __name__ == '__main__':
    result = CResult.merge_result(
        1,
        "test"
    )
    result_result = CResult.result_result(result)
    print(result_result)
