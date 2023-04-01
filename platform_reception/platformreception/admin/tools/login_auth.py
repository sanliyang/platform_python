# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_reception
@editor->name Sanliy
@file->name login_auth.py
@create->time 2023/3/30-9:55
@desc->
++++++++++++++++++++++++++++++++++++++ """
from ..models import Session_Reception


class LoginAuth:

    def __init__(self):
        ...

    @classmethod
    def add_session(cls, session_id, session_data, expire_date):
        sr = Session_Reception(session_id=session_id, session_data=session_data, expire_data=expire_date)
        sr.save()

    @classmethod
    def get_session(cls, session_id):
        try:
            session_result = Session_Reception.objects.get(session_id=session_id)
            session_data = session_result.session_data
        except:
            session_data = None
        return session_data
