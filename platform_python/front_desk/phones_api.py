from fastapi import APIRouter
from fastapi.params import Form
from starlette.responses import HTMLResponse

from model.attribution_lookups.attribution_lookups_phone import AttributionLookupsPhone
from base.c_logger import CLogger
from base.c_project import CProject
from starlette.requests import Request

logger = CLogger()

router = APIRouter(
    prefix="/phones",
    tags=["phones"],
    responses={404: {"description": "Not Found"}}
)

templates = CProject.get_template()


@router.get("/phone_local", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("query_phone_local.html", {"request": request})


@router.post("/query", response_class=HTMLResponse)
async def query_phone(request: Request, phone_number: str = Form(...)):
    alp = AttributionLookupsPhone(phone_number)
    phone_msg = alp.get_phone_json_msg()
    return templates.TemplateResponse("query_result_phone_local.html", {"request": request, "phone_msg": phone_msg})
