# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name weather_api.py
@create->time 2023/5/17-15:43
@desc->
++++++++++++++++++++++++++++++++++++++ """
from fastapi import APIRouter
from model.weather.catch_weather import CatchWeather
from base.c_logger import CLogger

logger = CLogger()

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/{area}")
async def get_weather(area: str):
    cw = CatchWeather()
    logger.info("正在查询[{0}]的天气情况".format(area))
    area_weather = cw.get_weather(area)
    return area_weather.text
