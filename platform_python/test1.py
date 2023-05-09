# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name test1.py
@create->time 2023/4/1-14:45
@desc->
++++++++++++++++++++++++++++++++++++++ """
import importlib
from node.weather.get_weather import GetWeather

gw = importlib.import_module("node.weather.get_weather")

myclass = getattr(gw, "GetWeather")


print(myclass.run_test(
    '''
        {
            "input": [],
            "output": [],
            "params": {
                "city": "郑州"
            }
        }
    '''
))
