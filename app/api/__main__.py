import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import controllers, dependencies
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
    dependencies.setup(app, pool, settings)
    controllers.setup(app)
    return app


if __name__ == '__main__':
    uvicorn.run(
        "app.api.__main__:main",
        host="0.0.0.0",
        port=15400,
        reload=True
    )
