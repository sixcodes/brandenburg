from functools import lru_cache

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from brandenburg.auth import get_fast_auth
from brandenburg.config import settings
from brandenburg.routers import imports, leads, notify
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.logger import log

# from fastapi.security import OAuth2PasswordBearer


logger = log.get_logger(__name__)


tags_metadata = [
    {
        "name": "leads",
        "description": "Service to collect leads through our landing pages then it should be used in the marketing campaigns.",
    },
    {"name": "import", "description": "Service to import data in lambda architecture."},
    {"name": "notify", "description": "Service to notify client using email, whatsapp or sms."},
]


app = FastAPI(
    debug=settings.DEBUG,
    title="Brandenburg API",
    version="0.1.0",
    description="""This is a message hub that allows decoupling your messages using a streaming approach.
    It is a simple API restful that receives your message then it uses serverless to connect to a service
    to process your message in an async approach. These connectors we called tubes.""",
    redoc_url="/docs",
    docs_url=None,
)
app.openapi_tags = tags_metadata
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


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

if settings.NAMESPACE.lower() in ("stg", 'prod'):
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(leads.router, prefix="/v1", tags=["leads"], responses={404: {"description": "Not found"}})

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
    logger.info(f"Check all topics on {settings.PROVIDER}")
    ProviderStrategy(settings.PROVIDER)._strategy.create_topics(
        [f"{topic}_{settings.NAMESPACE}" for topic in settings.TOPICS]
    )
    logger.info("creating auth users")
    # await create_users() # FIXME: remove it


@app.on_event("shutdown")
async def shutdown_event():
    from brandenburg.toolbox._backends.redis import RedisBackend

    cache = await RedisBackend(settings.REDIS_URL).get_instance()
    await cache.disconnect()
    logger.debug("================>III Shutting down")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
