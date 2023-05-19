from fastapi import APIRouter, Form
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


@router.post("/index")
async def index(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/group")
async def group(request: Request):
    return templates.TemplateResponse("admin_group.html", {"request": request})


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    print(username, password)
    # 这里编写检查用户和密码的逻辑， 检查通过就可以重定向到admin的首页， 检查不通过重定向到 login界面
    result = check_user(username, password)
    if result:
        url = router.url_path_for("index")
        return RedirectResponse(url=url)


def check_user(username, password):
    password_db = cm.fetchone(
        '''
        select password from python_platform.user where username =:username
        ''', {
            "username": username
        }
    )
    if password_db == password:
        return True
    else:
        return False


@router.get("/auth")
async def auth(request: Request):
    return templates.TemplateResponse("admin_auth.html", {"request": request})


@router.get("/user")
async def control_user(request: Request):
    return templates.TemplateResponse("admin_control_user.html", {"request": request})
