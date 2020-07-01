from fastapi import APIRouter, Request, status
from fastapi.responses import UJSONResponse

from brandenburg.models.notify import NotifyModel
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    "/notify/", status_code=202, responses={202: {"status": "OK", "message": "Notification Accepted!"}}
)
async def create_notification(notify: NotifyModel, request: Request):
    logger.info(
        f"""request: {request.json()}, headers: {dict(request.headers)},  token: {token}, ip:
                {request.client.host}"""
    )

    return {"status": "OK"}
