# Standard library imports
from functools import lru_cache

# Third party imports
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local application imports
from brandenburg.auth import get_fast_auth
from brandenburg.config import settings
from brandenburg.routers import imports, leads, notify
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.logger import logger
from brandenburg import __version__
from brandenburg import cache

tags_metadata = [
    {
        "name": "leads",
        "description": "Service to collect leads through our landing pages then it should be used in the marketing campaigns.",
    },
    {
        "name": "import",
        "description": "Service to import data in lambda architecture.",
    },
    {
        "name": "notify",
        "description": "Service to notify client using email, whatsapp or sms.",
    },
]


app: FastAPI = FastAPI(
    debug=settings.DEBUG,
    title="Brandenburg API",
    version=__version__,
    description="""This is a message hub that allows decoupling your messages using a streaming approach.
    It is a simple API restful that receives your message then it uses serverless to connect to a service
    to process your message in an async approach. These connectors we called tubes.""",
    redoc_url="/docs",
    docs_url=None,
)
app.openapi_tags = tags_metadata


@lru_cache()
def get_settings():
    return settings


# README: CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],  # TODO: set the correctness headers only
)

if settings.NAMESPACE.lower() in ("stg", "prd"):
    # Third party imports
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(
    leads.router,
    prefix="/v1",
    tags=["leads"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    leads.router,
    prefix="/v1",
    tags=["leads"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    imports.router,
    prefix="/v1",
    tags=["import"],
    dependencies=[Depends(get_settings), Depends(get_fast_auth)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    notify.router,
    prefix="/v1",
    tags=["notify"],
    dependencies=[Depends(get_settings), Depends(get_fast_auth)],
    responses={404: {"description": "Not found"}},
)


@app.on_event("startup")
async def startup_event():
    # TODO: Move PUBSUB/SQS connection to here
    await logger.info(f"Check all topics on {settings.PROVIDER}")
    ProviderStrategy(settings.PROVIDER)._strategy.create_topics(
        [f"{topic}_{settings.NAMESPACE}" for topic in settings.TOPICS]
    )
    await cache.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await cache.disconnect()
    await logger.debug("================>III Shutting down")


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST_BIND, port=8000)
