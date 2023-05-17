# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name get_weather.py
@create->time 2023/5/17-15:49
@desc->
++++++++++++++++++++++++++++++++++++++ """
import requests

from base.c_config import CConfig
from base.c_project import CProject


class CatchWeather:

    def __init__(self):
        cc = CConfig(CProject.config_path())
        self.weather_url = cc.get_value('weather', 'weather_url')
        self.weather_user = cc.get_value('weather', 'weather_user')
        self.weather_pass = cc.get_value('weather', 'weather_pass')

    def get_weather(self, area):
        response = requests.get(url=self.weather_url, params={
            "appid": self.weather_user,
            "appsecret": self.weather_pass,
            "city": area,
            "unescape": 1
        })
        return response
