from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.exceptions.handlers import register_exception_handlers
from app.api.router import api_router
from app.core.config import routes
from app.core.logger.logging import setup_logging
from app.utils.utils import log_registered_routes
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import app_config


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=app_config.name, lifespan=log_registered_routes)

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=routes.prefix)

    # app.mount("/static", StaticFiles(directory="app/static"), name="static")

    return app


app = create_app()
