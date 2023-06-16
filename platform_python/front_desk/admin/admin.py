from fastapi import APIRouter, Form, status
from base.c_logger import CLogger
from base.c_project import CProject
from base.c_mysql import CMysql
from starlette.requests import Request
from starlette.responses import RedirectResponse

logger = CLogger()
cm = CMysql()

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)

templates = CProject.get_template()


@router.get("/index", name="admin_index")
async def index(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin.html", {"request": request, "username": username})


@router.get("/group", name="admin_group")
async def group(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_group.html", {"request": request, "username": username})


@router.get("/", name="admin_get_login")
async def login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/", name="admin_post_login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    print(username, password)
    # 这里编写检查用户和密码的逻辑， 检查通过就可以重定向到admin的首页， 检查不通过重定向到 login界面
    result = check_user(username, password)
    if result:
        url = router.url_path_for("admin_index")
        request.session["username"] = username
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    url = router.url_path_for("admin_get_login")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


def check_user(username, password):
    password_db = cm.fetchone(
        '''
        select password from python_platform.user where username =:username
        ''', {
            "username": username
        }
    )
    if password_db[0] == password:
        return True
    else:
        return False


@router.get("/auth", name="admin_auth")
async def auth(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_auth.html", {"request": request, "username": username})


@router.get("/user", name="admin_user")
async def user(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    users_msg = cm.fetchall(
        '''
        select user_id, username, role, email from python_platform.user
        '''
    )
    return templates.TemplateResponse("admin_user.html", {"request": request, "username": username, "users_msg": users_msg})


@router.get("/product", name="admin_product")
async def product(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_product.html", {"request": request, "username": username})


@router.get("/order", name="admin_order")
async def order(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_order.html", {"request": request, "username": username})


@router.get("/report", name="admin_report")
async def report(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_report.html", {"request": request, "username": username})


@router.get("/setting", name="admin_setting")
async def setting(request: Request):
    if "username" not in request.session:
        url = router.url_path_for("admin_get_login")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    username = request.session["username"]
    return templates.TemplateResponse("admin_setting.html", {"request": request, "username": username})


@router.get("/quit")
async def admin_quit(request: Request):
    request.session.pop("username")
    url = router.url_path_for("admin_get_login")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
