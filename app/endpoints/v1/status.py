from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v1/status")
async def healthcheck():
    sql = "SELECT version();"
    cur = openConnection()
    cur.execute(
        sql
    )
    version = cur.fetchone()[0]
    return {"version": version}
