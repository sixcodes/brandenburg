from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from brandenburg.config import settings
from brandenburg.routers import imports, leads
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


def custom_openapi(openapi_prefix: str):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Brandenburg Tor API",
        version="0.1.0",
        description="This is ",
        routes=app.routes,
        openapi_prefix=openapi_prefix,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": ".png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = custom_openapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# README: CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_HOSTS.split(","),
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(leads.router, prefix="/v1", tags=["leads"], responses={404: {"description": "Not found"}})

app.include_router(
    imports.router,
    prefix="/v1",
    tags=["import"],
    # dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@app.on_event("startup")
async def startup_event():
    # TODO: Move PUBSUB/SQS connection to here
    logger.info(f"Check all topics on {settings.PROVIDER}")
    ProviderStrategy(settings.PROVIDER)._strategy.create_topics(
        [f"{topic}_{settings.NAMESPACE}" for topic in settings.TOPICS.split(",")]
    )
