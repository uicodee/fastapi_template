from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import load_config
from app.infrastructure.database.factory import create_pool, make_connection_string


def main() -> FastAPI:
    settings = load_config()
    app = FastAPI(
        docs_url="/docs",
        version="1.0.0"
    )
    pool = create_pool(url=make_connection_string(settings=settings))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
