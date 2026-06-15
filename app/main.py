from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.config.config import app_config
from app.utils.utils import log_registered_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=app_config.app_name, lifespan=log_registered_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=app_config.api_v1_prefix.global_prefix)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
