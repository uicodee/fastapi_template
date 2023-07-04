from fastapi import FastAPI
from .authentication import router as authentication_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=authentication_router,
        tags=["Authentication"]
    )
