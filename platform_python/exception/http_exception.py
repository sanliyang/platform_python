# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name http_exception.py
@create->time 2023/6/6-15:02
@desc->
++++++++++++++++++++++++++++++++++++++ """
from builtins import Exception


class HttpException(Exception):

    def __init__(self, err_code, err_msg):
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):
        return f"{self.err_code}: {self.err_msg}"


if __name__ == '__main__':
    raise HttpException("0x01", "test")