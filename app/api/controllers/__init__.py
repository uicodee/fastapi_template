from fastapi import FastAPI
from .test import router as test_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=test_router,
        tags=["test"]
    )
