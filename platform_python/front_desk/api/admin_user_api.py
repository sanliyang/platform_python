# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name admin_user_api.py
@create->time 2023/5/22-16:40
@desc->
++++++++++++++++++++++++++++++++++++++ """

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from base.c_logger import CLogger
from base.c_mysql import CMysql

logger = CLogger()

router = APIRouter(
    prefix="/admin/user",
    tags=["admin_user"],
    responses={404: {"description": "Not Found"}}
)
cm = CMysql()


@router.get("/delete/{username}", name="delete_user")
async def delete(request: Request, username: str):
    try:
        cm.execute(
            '''
            delete from python_platform.user where username =:username
            ''', {
                "username": username
            }
        )

    except:
        ...
    url = "/admin/user"
    return RedirectResponse(url=url)
