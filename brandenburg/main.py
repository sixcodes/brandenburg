from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from brandenburg.auth import get_fast_auth, create_users
from brandenburg.config import settings
from brandenburg.routers import imports, leads, notify
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.logger import log

# from fastapi.security import OAuth2PasswordBearer


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


app = FastAPI(debug=settings.DEBUG, title="Brandenburg API", redoc_url="/docs", docs_url=None)
app.openapi = custom_openapi
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
    allow_headers=["*"],
)


app.include_router(leads.router, prefix="/v1", tags=["Leads"], responses={404: {"description": "Not found"}})

app.include_router(
    imports.router,
    prefix="/v1",
    tags=["Import"],
    dependencies=[Depends(get_settings), Depends(get_fast_auth)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    notify.router,
    prefix="/v1",
    tags=["Notify"],
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
    await create_users()


@app.on_event("shutdown")
async def shutdown_event():
    from brandenburg.toolbox._backends.redis import RedisBackend

    cache = await RedisBackend(settings.REDIS_URL).get_instance()
    await cache.disconnect()
    logger.debug("================>III Shutting down")
