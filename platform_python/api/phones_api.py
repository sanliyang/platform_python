from fastapi import APIRouter
from model.attribution_lookups.attribution_lookups_phone import AttributionLookupsPhone
from base.c_logger import CLogger

logger = CLogger()

router = APIRouter(
    prefix="/phones",
    tags=["phones"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/msg/{phone_number}")
async def get_msg(phone_number: str):
    gpl = AttributionLookupsPhone(phone_number)
    logger.info("正在查询[{0}]的详细信息！".format(phone_number))
    return gpl.get_phone_json_msg()
