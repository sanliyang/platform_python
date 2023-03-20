from fastapi import FastAPI, Request
from base.c_time import CTime
from base.c_logger import CLogger
from api import phones_api
from api import ip_api

logger = CLogger()

app = FastAPI()

app.include_router(phones_api.router)
app.include_router(ip_api.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to FastApi"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info(f"当前请求的请求头信息是:{request.headers}")
    logger.info(f"当前请求的ip地址是:{request.client.host}")
    logger.info(f"当前请求的端口号是:{request.client.port}")
    start_time = CTime.get_now_time()
    response = await call_next(request)
    process_time = CTime.get_now_time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
