# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name mail_slice.py
@create->time 2023/5/11-11:11
@desc->
++++++++++++++++++++++++++++++++++++++ """
from c_json import CJson
from c_result import CResult
from node.base.node_base import NodeBase


class MailSlice(NodeBase):
    def help(self):
        return '''
                    算法名称: 邮箱切片算法
                    分属类别：mail
                    算法作用：获取到@符号之前的字符
                    算法接收参数
                    {
                        "input": ["xxx@126.com", "xxx@163.com"],
                        "output": [],
                        "params": {
                        }
                    }
                '''

    def check_params(self):
        result = super().check_params()
        if CResult.result_faild(result):
            return result

    def check_input(self):
        result = super().check_input()
        if CResult.result_faild(result):
            return result
        if self.input_list == [] or self.input_list is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "请输入目标邮箱, 算法将不再继续往下执行, 请输入邮箱后重试!"
            )
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入邮箱检查成功，算法将继续运行..."
        )

    def run(self):
        result = super().run()
        if CResult.result_faild(result):
            return result
        slice_mail_result = self.slice_mail()
        return slice_mail_result

    def slice_mail(self):
        try:
            classify_mail = {}
            for one_email in self.input_list:
                mail_features = one_email.split("@")[0]
                mail_type = one_email.split("@")[1].split(".")[0]
                if mail_type not in classify_mail.keys():
                    classify_mail[mail_type] = []
                classify_mail[mail_type].append(mail_features)
            # 保存邮件分类到文件
            with open("mail.json", "w") as f:
                f.write(CJson.dict_2_json(classify_mail))
            result = CResult.merge_result(
                self.RESULT_SUCCESS,
                "已完成邮箱分类!"
            )
        except Exception as error:
            result = CResult.merge_result(
                self.RESULT_FAILD,
                f"邮箱分类失败，具体原因是[{error}], 请检查重试！"
            )
        return result


if __name__ == '__main__':
    MailSlice.run_test(
        '''
        {
            "input": ["xxx@126.com", "xxx@163.com"],
            "output": [],
            "params": {
            }
        }
        '''
    )
