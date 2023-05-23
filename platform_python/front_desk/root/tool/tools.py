# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name tools.py
@create->time 2023/5/23-13:43
@desc->
++++++++++++++++++++++++++++++++++++++ """
from fastapi import APIRouter
from fastapi.params import Form
from starlette import requests
from starlette.responses import HTMLResponse

from base.c_mysql import CMysql
from model.attribution_lookups.attribution_lookups_phone import AttributionLookupsPhone
from base.c_logger import CLogger
from base.c_project import CProject
from starlette.requests import Request

logger = CLogger()
cm = CMysql()

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
    responses={404: {"description": "Not Found"}}
)

templates = CProject.get_template()


@router.get("/root", response_class=HTMLResponse)
async def home(request: Request):
    tools_type = []
    all_tools_type = cm.fetchall(
        '''
        select tool_type from python_platform.tools group by tool_type
        '''
    )
    for tool_type in all_tools_type:
        tools_type_dict = dict()
        tools_type_dict["tool_type"] = tool_type[0]
        tools_type_dict["tool_list"] = []
        tools_msg = cm.fetchall(
            '''
            select tool_name, tool_route from python_platform.tools where tool_type =:tool_type
            ''', {
                "tool_type": tool_type[0]
            }
        )

        for tool_msg in tools_msg:
            tool_dict = dict()
            tool_dict["name"] = tool_msg[0]
            tool_dict["route"] = tool_msg[1]

            tools_type_dict["tool_list"].append(tool_dict)
        tools_type.append(tools_type_dict)
    return templates.TemplateResponse("tools.html", {"request": request, "tools_type": tools_type})
