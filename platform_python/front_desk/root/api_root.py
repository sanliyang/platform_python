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

logger = CLogger()

app = FastAPI()

app.include_router(phones_api.router)
app.include_router(ip_api.router)
app.include_router(weather_api.router)

app.mount("/static", StaticFiles(directory=CFile.path_join(CProject.project_path(), "static")), name="static")

templates = CProject.get_template()


@app.get("/", tags=["root"])
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/admin", tags=["admin"])
async def root(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    logger.info(f"当前请求的请求头信息是:{request.headers}")
    logger.info(f"当前请求的ip地址是:{request.client.host}")
    logger.info(f"当前请求的端口号是:{request.client.port}")
    start_time = CTime.get_now_time()
    response = await call_next(request)
    process_time = CTime.get_now_time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["server"] = "platform_python"
    return response
