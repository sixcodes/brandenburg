# Third party imports
from fastapi import APIRouter, Request, status
from fastapi.responses import ORJSONResponse

# Local application imports
from brandenburg.models.lead import LeadModel
from brandenburg.services.lead import LeadService
from brandenburg.toolbox.funcs import Funcs
from brandenburg.toolbox.logger import logger

router = APIRouter()


@router.get("/leads/token/")
async def get_lead_token(request: Request):
    """
    Used to create a unique token valid for a few minutes only.
    """
    token: str = await Funcs.generate_token(request.client.host)
    await logger.info(f"""headers: {dict(request.headers)}, ip: {request.client.host}, token: {token}""")
    return {"token": token}


@router.post(
    "/leads/{token}/",
    status_code=201,
    responses={201: {"status": "OK", "message": "Batch Accepted!"}},
)
async def create_lead(lead: LeadModel, request: Request, token: str):
    """
    It expected the data from the landing page.
    """
    await logger.info(
        f"""request: {await request.json()}, headers: {dict(request.headers)},  token: {token}, ip:
                {request.client.host}"""
    )
    result, processed = await LeadService.execute(str(token), lead)
    await logger.info(f"response: {result}, processed: {processed}")
    if processed:
        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"status": "ok", "message": "Batch Accepted!"},
        )
    return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=result)
