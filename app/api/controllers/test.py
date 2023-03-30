from fastapi import APIRouter


router = APIRouter()


@router.get(
    path="/ping",
    description="Test API available"
)
async def ping():
    return {"ping": "pong"}
