from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.core.config import routes
from app.utils.utils import log_registered_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OZON", lifespan=log_registered_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=routes.prefix)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
