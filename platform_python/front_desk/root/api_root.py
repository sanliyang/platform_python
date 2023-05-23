from fastapi import FastAPI
from base.c_time import CTime
from base.c_logger import CLogger
from front_desk import phones_api
from front_desk import ip_api
from front_desk import weather_api
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from base.c_file import CFile
from base.c_project import CProject
from front_desk.admin import admin
from starlette_session import SessionMiddleware
from front_desk.api import admin_user_api
from front_desk.root.tool import tools

logger = CLogger()

app = FastAPI()

app.include_router(phones_api.router)
app.include_router(ip_api.router)
app.include_router(weather_api.router)
app.include_router(admin.router)
app.include_router(admin_user_api.router)
app.include_router(tools.router)

app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    cookie_name="username",
)

app.mount("/static", StaticFiles(directory=CFile.path_join(CProject.project_path(), "static")), name="static")

templates = CProject.get_template()


@app.get("/", tags=["root"])
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    logger.info(f"当前请求的请求头信息是:{request.headers}")
    logger.info(f"当前请求的ip地址是:{request.client.host}")
    logger.info(f"当前请求的端口号是:{request.client.port}")
    start_time = CTime.get_now_time()
    response = await call_next(request)
    process_time = CTime.get_now_time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Server"] = "platform_python"
    return response
