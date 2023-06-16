# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name user_agent.py
@create->time 2023/6/6-14:44
@desc->
++++++++++++++++++++++++++++++++++++++ """
import random

UserAgentPC = {
    "safari 5.1 – MAC": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "safari 5.1 – Windows": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "google chrome": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "firefox": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Opera": "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "sougo": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "360": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; 360se)",
    "tc": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)"
}


def get_ua_random():
    ua_keys = list(UserAgentPC.keys())
    ua_keys_len = len(ua_keys)
    one_random_index = random.randint(0, ua_keys_len)
    ua_key = ua_keys[one_random_index]
    ua_value = UserAgentPC[ua_key]
    return ua_value
