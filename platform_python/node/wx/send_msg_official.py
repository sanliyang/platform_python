# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name send_msg_official.py
@create->time 2023/5/6-14:19
@desc->
++++++++++++++++++++++++++++++++++++++ """
import threading
from threading import Timer
import requests
from c_json import CJson
from c_result import CResult
from node.base.node_base import NodeBase


class MyTimer:

    def __init__(self, expires_time):
        self.expires_time = expires_time
        t = threading.Thread(target=self.timer_obj)
        t.start()

    def timer_obj(self):
        while True:
            timer = Timer(1, self.countdown)
            timer.start()
            timer.join()
            if self.expires_time == 0:
                break

    def countdown(self):
        if self.expires_time is not None:
            self.expires_time -= 1

    def get_expires_time(self):
        return self.expires_time


class SendMsgOfficial(NodeBase):
    def __init__(self):
        super().__init__()
        self.access_token = None
        self.expires_time = None
        self.my_timer = None

    def help(self):
        return '''
                算法名称: 微信公众号推文算法
                分属类别：wx
                算法作用：微信公众号发送推文给所有关注的用户
                算法接收参数
                {
                    "input": [],
                    "output": [],
                    "params": {
                        "city": "xxxxxxxx"
                    }
                }
                '''

    def check_params(self):
        result = super().check_params()
        if CResult.result_faild(result):
            return result

    def get_access_token(self):
        appid = "xxxxxxxxxx"
        secret = "xxxxxxxxxxxx"
        resp = requests.get(
            url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(
                appid,
                secret
            ))
        if resp.status_code == 200:
            access_token_config = resp.text
            print(access_token_config)
            cj = CJson()
            cj.load(access_token_config)

            self.access_token = cj.json_path_one("access_token")
            self.expires_time = cj.json_path_one("expires_in")
            print(self.expires_time)

            self.my_timer = MyTimer(self.expires_time)

    def get_all_open_id(self):
        next_openid = ''
        print(self.access_token)
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (
            self.access_token, next_openid)
        ans = requests.get(url_openid)
        print(ans.text)
        cj = CJson()
        cj.load(ans.content)
        open_ids = cj.json_path_one('data.openid')
        print(open_ids)
        return open_ids

    def do_some_thing(self):
        ...

    def run(self):
        result = super().run()
        if CResult.result_faild(result):
            return result
        self.get_access_token()
        flag = self.my_timer.get_expires_time()
        if flag > 0:
            print("aa")
            print(flag)
            self.get_all_open_id()


if __name__ == '__main__':
    smo = SendMsgOfficial()
    smo.run_test(
        '''
        {
            "input": [],
            "output": [],
            "params": {
                "city": "xxxxxxxx"
            }
        }
        '''
    )
