# Create your views here.
import base64
import datetime
import uuid
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Session_Reception
from .tools.login_auth import LoginAuth


def index(request: WSGIRequest):
    return render(request, 'admin/admin.html')


def post(request: WSGIRequest):
    try:
        session_id = request.COOKIES.get("sessionid")
        session_result = Session_Reception.objects.get(session_id=session_id)
        return HttpResponse(request, {'status': 'success'})
    except:
        # 判断用户名和密码 用户是否是已注册的用户，以及用户的密码是否正确
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        try:
            result = User.objects.get(username=username)
        except:
            return HttpResponse(request, {'status': 'error'})
        if result.password == password:
            request.COOKIES.__setitem__("session_id", uuid.uuid4().hex)
            # 将这个session写到数据库中
            session_data = base64.b64encode(username.encode("utf-8"))
            LoginAuth.add_session(request.COOKIES.get("session_id"), session_data, datetime.datetime.now())
            response = HttpResponse(request, {'status': 'success', 'msg': 'test'})
            response.set_cookie("sessionid", request.COOKIES.get("session_id"), max_age=3600)
            return response
        else:
            return HttpResponse(request, {'status': 'error'})


def control(request: WSGIRequest):
    session_id = request.COOKIES.get("sessionid")
    # 这里需要对来的请求进行判断，是否是已经登录的成员，只有登录的成员才可以看到这页面 使用session进行检查
    usrname_base64 = LoginAuth.get_session(session_id)
    if usrname_base64 is None:
        return redirect("/admin/index")
    username = base64.b64decode(eval(usrname_base64)).decode("utf-8")
    return render(request, 'admin/admin_control.html', {"username": username})
