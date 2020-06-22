from typing import Dict

from fastapi import APIRouter, Request, status
from fastapi.responses import UJSONResponse

from brandenburg.models.batch import BatchModel
from brandenburg.services.batch import BatchService
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    "/import/push/", tags=["import"], status_code=201, responses={201: {"status": "OK", "message": "Batch Accepted!"}}
)
async def import_data(batch: BatchModel, request: Request):
    logger.info(f"request: X, headers: {dict(request.headers)}, ip: {request.client.host}")
    result, processed = await BatchService.execute(batch, "import_push")
    return UJSONResponse(status_code=status.HTTP_201_CREATED, content={"status": "OK", "message": "Batch Accepted!"})
