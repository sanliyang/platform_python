# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name product_line.py
@create->time 2023/5/30-9:33
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
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not Found"}}
)

templates = CProject.get_template()


@router.get("/lines", response_class=HTMLResponse)
async def home(request: Request):
    all_nodes_msg = cm.fetchall(
        '''
        select node_id, node_zh_name, node_type from python_platform.do_nodes
        '''
    )
    all_nodes_dequeue = []
    for one_nodes in all_nodes_msg:
        one_nodes_msg = {}
        one_nodes_msg["node_id"] = one_nodes[0]
        one_nodes_msg["one_node_zh_name"] = one_nodes[1]
        one_nodes_msg["onde_node_type"] = one_nodes[2]
        all_nodes_dequeue.append(one_nodes_msg)
    return templates.TemplateResponse("product_lines.html", {"request": request, "all_nodes_msg": all_nodes_dequeue})
