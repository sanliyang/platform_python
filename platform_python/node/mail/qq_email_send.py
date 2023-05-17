# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name qq_email_send.py
@create->time 2023/4/7-13:40
@desc->
++++++++++++++++++++++++++++++++++++++ """
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from base.c_config import CConfig
from base.c_file import CFile
from base.c_project import CProject
from base.c_result import CResult
from base.c_utils import CUtils
from node.base.node_base import NodeBase


class QQEmailSend(NodeBase):

    def __init__(self):
        super().__init__()
        self.email_title = None
        self.email_content = None
        self.email_type = None
        self.email_annex = None
        self.mail_host = "smtp.qq.com"
        self.mail_port = 465
        self.smtp_obj = None
        self.annex_type = None

        # 从配置文件中读取 发送邮箱和验证信息
        cc = CConfig(CProject.config_path())
        self.send_user = cc.get_value('email', 'auth_count')
        self.send_auth = cc.get_value('email', 'auth_pass')

    def help(self):
        return '''
                算法名称: 发送邮件算法
                分属类别：mail
                算法作用：使用QQemail发送电子邮件到指定的账户
                算法接收参数
                {
                    "input": ["email_count1", "email_count2"],
                    "output": [],
                    "params": {
                        "email_sender": "xxxxxxxx",
                        "email_auth": "xxxxxxxxxxx",
                        "email_cc": "xxxxxxxxxx",
                        "email_title": "",
                        "email_content: "",
                        "email_type: "",
                        "email_annex": "",
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
        self.email_title = CUtils.dict_value_by_name(self.params, "email_title", None)
        self.email_content = CUtils.dict_value_by_name(self.params, "email_content", None)
        self.email_type = CUtils.dict_value_by_name(self.params, "email_type", None)
        self.email_annex = CUtils.dict_value_by_name(self.params, "email_annex", None)
        self.email_annex_type = CUtils.dict_value_by_name(self.params, "email_annex_type", None)
        if self.email_title is None or self.email_content is None or self.email_type is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "部分必要参数未设定， 请检查修正！"
            )
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入参数检查成功，算法将继续运行..."
        )

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
        # 创建smtp对象
        self.create_smtp_obj()
        self.login_smtp()
        send_result = self.send(self.input_list)
        self.logout_smtp()
        return send_result

    def create_smtp_obj(self):
        self.smtp_obj = smtplib.SMTP_SSL(host=self.mail_host, port=self.mail_port)
        result = self.smtp_obj.connect(host=self.mail_host, port=self.mail_port)
        if result[0] == 220:
            return CResult.merge_result(
                self.RESULT_SUCCESS,
                "已经连接到邮箱服务器，邮件继续发送"
            )
        else:
            return CResult.merge_result(
                self.RESULT_FAILD,
                f"邮箱服务器连接失败,具体原因是{result[1]}"
            )

    def logout_smtp(self):
        self.smtp_obj.quit()

    def login_smtp(self):
        resp = self.smtp_obj.login(user=self.send_user, password=self.send_auth)
        if resp[0] == 235:
            return CResult.merge_result(
                self.RESULT_SUCCESS,
                "已经成功登录到邮箱，邮件继续发送"
            )
        else:
            return CResult.merge_result(
                self.RESULT_FAILD,
                f"邮箱登录失败,具体原因是{resp[1]}"
            )

    def send(self, email_target):

        mail_msg = MIMEMultipart()

        mail_msg["Subject"] = self.email_title
        mail_msg["from"] = self.send_user
        mail_msg["to"] = ",".join(email_target)
        mail_msg["Cc"] = self.send_user

        mail_msg.attach(MIMEText(self.email_content, self.email_type, self.ENCODE_UTF8))

        # 判断是否存在附件
        if self.email_annex is not None and self.email_annex != "":
            mail_msg = self.add_annex(mail_msg)

        send_result = self.smtp_obj.sendmail(from_addr=self.send_user, to_addrs=email_target, msg=mail_msg.as_string())
        if send_result == {}:
            return CResult.merge_result(
                self.RESULT_SUCCESS,
                f"邮件已经成功发送到{email_target}"
            )
        else:
            return CResult.merge_result(
                self.RESULT_FAILD,
                f"邮件发送到{email_target}失败！"
            )

    def add_annex(self, email_msg):
        # 添加附件
        with open(self.email_annex, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype=self.email_annex_type)
            attachment.add_header('Content-Disposition', 'attachment', filename=CFile.get_name_with_suffix(self.email_annex))
            email_msg.attach(attachment)
        return email_msg


if __name__ == '__main__':
    QQEmailSend.run_test(
        '''
        {
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
        '''
    )
