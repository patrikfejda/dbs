from fastapi import APIRouter

router = APIRouter()

@router.get("/v1/health")
async def healthcheck():
    return {"status": 200, "message": "Alive never before."}
