# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name ip_api.py
@create->time 2023/3/16-19:03
@desc->
++++++++++++++++++++++++++++++++++++++ """
from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse

from base.c_config import CConfig
from base.c_project import CProject
from base.c_json import CJson
from model.attribution_lookups.attribution_lookups_ip import AttributionLookupsIp
from base.c_logger import CLogger

logger = CLogger()

templates = CProject.get_template()

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


@router.get("/ip_local", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("query_ip_local.html", {"request": request})


@router.post("/query", response_class=HTMLResponse)
async def query_phone(request: Request, ip_number: str = Form(...)):
    print("aaaaaaa")
    # 获取百度ak
    cc = CConfig(CProject.config_path())
    baidu_ak = cc.get_value('ip', 'baidu_ak')
    print(baidu_ak)
    print(ip_number)
    ali = AttributionLookupsIp(ip_number)
    lon = ali.get_longitude()
    lat = ali.get_latitude()
    print(lon, lat)
    resp = ali.get_detail_json_msg(baidu_ak, lon, lat)
    cj = CJson()
    cj.load(resp)
    ip_msg = cj.json_path_one("result")
    print(ip_msg)
    return templates.TemplateResponse(
        "query_result_ip_local.html",
        {"request": request, "ip_msg": ip_msg, "ip_num": ip_number}
    )
