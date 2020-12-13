# Third party imports
from fastapi import APIRouter, Request, status
from fastapi.responses import UJSONResponse

# Local application imports
from brandenburg.models.notify import NotifyModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    "/notify/", status_code=202, responses={202: {"status": "OK", "message": "Notification Accepted!"}},
)
async def create_notification(notify: NotifyModel, request: Request):
    logger.info(
        f"""request: {await request.json()}, headers: {dict(request.headers)}, ip:
                {request.client.host}"""
    )
    await PublisherService.publish(notify.dict(), notify.by)
    return {"status": "OK", "message": "Notification Accepted!"}
