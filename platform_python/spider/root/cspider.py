# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name cspider.py
@create->time 2023/6/6-10:29
@desc->
++++++++++++++++++++++++++++++++++++++ """
import lxml
import requests
from bs4 import BeautifulSoup

from c_utils import CUtils
from exception.http_exception import HttpException
from spider.useragent import user_agent


class CSpider:
    def __init__(self):
        self.headers = {
            "User-Agent": user_agent.get_ua_random()
        }

    def request(self, url: str, r_type: str, options=None):
        if options is None:
            options = {}
        data_data = CUtils.dict_value_by_name(options, "data", None)
        json_data = CUtils.dict_value_by_name(options, "json", None)
        params_data = CUtils.dict_value_by_name(options, "params", None)

        if r_type == "post":
            response = requests.post(url=url, headers=self.headers, data=data_data, json=json_data, params=params_data)
        else:
            response = requests.get(url=url, headers=self.headers, data=data_data, json=json_data, params=params_data)
        if response.status_code == 200:
            return response
        else:
            raise HttpException("0x001",
                                f"当前请求[{url}]失败，响应状态码为[{response.status_code}], 响应内容为[{response.text}], 请检查修正！")

    def parse(self, response, parse_grammar):
        bs = BeautifulSoup(response.content, "lxml")
        all_elements = bs.select(parse_grammar)

    def download_with_url(self, url, download_path):
        ...

    def download_content(self, content, path):
        with open(path, "wb") as f:
            f.write(content)

    def content_2_db(self, *args, **kwargs):
        ...


if __name__ == '__main__':
    cs = CSpider()
    rsp_tx = cs.request("http://cncdn2.54ntr.site/video/lqsi4ik3yi7w/f833b5.ts", "get")
    cs.download_content(rsp_tx.content, "a.ts")
