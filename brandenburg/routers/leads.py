from typing import Dict

from fastapi import APIRouter, Request, status
from fastapi.responses import UJSONResponse

from brandenburg.models.lead import LeadModel
from brandenburg.services.lead import LeadService
from brandenburg.toolbox.funcs import Funcs
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)
router = APIRouter()


@router.get("/leads/token/")
async def get_lead_token(request: Request):
    token: str = await Funcs.generate_token(request.client.host)
    logger.info(f"""headers: {dict(request.headers)}, ip: {request.client.host}, token: {token}""")
    return {"token": token}


@router.post("/leads/{token}/", status_code=201, responses={201: {"status": "OK", "message": "Batch Accepted!"}})
async def create_lead(lead: LeadModel, request: Request, token: str):
    logger.info(
        f"""request: {request.json()}, headers: {dict(request.headers)},  token: {token}, ip:
                {request.client.host}"""
    )
    result, processed = await LeadService.execute(str(token), lead)
    logger.info(f"response: {result}, processed: {processed}")
    if processed:
        return UJSONResponse(
            status_code=status.HTTP_201_CREATED, content={"status": "ok", "message": "Batch Accepted!"}
        )
    return UJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=result)
