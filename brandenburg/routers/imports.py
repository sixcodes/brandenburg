from typing import Dict

from fastapi import APIRouter, Request, status, UploadFile, File, BackgroundTasks
from fastapi.responses import UJSONResponse

from brandenburg.models.batch import BatchModel
from brandenburg.services.batch import BatchService
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    "/import/push/", tags=["import"], status_code=201, responses={201: {"status": "OK", "message": "Batch Accepted!"}}
)
async def import_push(batch: BatchModel, request: Request):
    logger.info(f"request: X, headers: {dict(request.headers)}, ip: {request.client.host}")
    result, processed = await BatchService.execute(batch, "import_push")
    return UJSONResponse(status_code=status.HTTP_201_CREATED, content={"status": "OK", "message": "Batch Accepted!"})


@router.post("/import/batch/", tags=["import"], status_code=201)
async def import_batch(batch: BatchModel, request: Request):
    """
    Pushes a record or multiple records for a specified table to lake.
    Each request to this endpoint may only contain data for a single table structure.

    When data for a table is pushed for the first time,
    the function/lambda will create the table in the destination in the specified schema mapping
    field.
    
    """
    return {}


@router.post("/import/file/", status_code=202, responses={202: {"status": "ok"}})
async def import_file(name: str, hash: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    background_tasks.add_task(BatchService.upload, name, file.filename, file.file, hash)
    # TODO: Create a hash from hash parameter and return it to be checked from requested
    logger.info("File was sent to background task.")
    return UJSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"status": "ok", "message": "File accepted"})
