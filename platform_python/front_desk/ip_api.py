# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name ip_api.py
@create->time 2023/3/16-19:03
@desc->
++++++++++++++++++++++++++++++++++++++ """
from fastapi import APIRouter
from model.attribution_lookups.attribution_lookups_ip import AttributionLookupsIp
from base.c_logger import CLogger

logger = CLogger()

router = APIRouter(
    prefix="/ip",
    tags=["ip"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/city/{ip}")
async def get_city(ip: str):
    ali = AttributionLookupsIp(ip)
    logger.info("正在查询[{0}]所在城市！".format(ip))
    return ali.get_city_piny()


@router.get("/region/{ip}")
async def get_region(ip: str):
    ali = AttributionLookupsIp(ip)
    logger.info("正在查询[{0}]所在省份！".format(ip))
    return ali.get_region_piny()
