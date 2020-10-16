import logging

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse

from app.controllers import animals
from app.core import config

logging.root.setLevel("INFO")


def create_app():
    fast_app = FastAPI(
        debug=False,
        title="{{cookiecutter.project_name}} API Document",
        servers=[
            {"url": "http://localhost:8000", "description": "Developing environment"},
        ],
        default_response_class=JSONResponse,
    )
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_app.add_middleware(ServerErrorMiddleware, debug=(config.settings.env == "local"))
    fast_app.add_middleware(GZipMiddleware)
    fast_app.include_router(animals.router)
    return fast_app


app = create_app()

if config.settings.env != "local":  # pragma: no cover
    sentry_sdk.init(dsn=config.settings.sentry_dsn, environment=config.settings.env)
    app.add_middleware(SentryAsgiMiddleware)
