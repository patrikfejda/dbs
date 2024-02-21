from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/v1/hello")
async def hello():
    return {
        'hello': settings.NAME
    }
