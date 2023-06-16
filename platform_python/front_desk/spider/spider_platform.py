# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name spider_platform.py
@create->time 2023/5/30-11:12
@desc->
++++++++++++++++++++++++++++++++++++++ """
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from base.c_mysql import CMysql
from base.c_logger import CLogger
from base.c_project import CProject
from starlette.requests import Request

logger = CLogger()
cm = CMysql()

router = APIRouter(
    prefix="/spider",
    tags=["spider"],
    responses={404: {"description": "Not Found"}}
)

templates = CProject.get_template()


@router.get("/index", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("spider_index.html", {"request": request})
