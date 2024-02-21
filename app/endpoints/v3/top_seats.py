
from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v3/airlines/{flight_no}/top_seats")
async def topseats(flight_no, limit):

    sql = f"""  
SELECT VERSION();
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    res = cur.fetchall()
    closeConnection(cur)
    
    return {"results": "not implemented"}
