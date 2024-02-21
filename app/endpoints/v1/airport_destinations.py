
from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v1/airports/{airport}/destinations")
async def departures(airport):
    sql = f"""  
SELECT f.arrival_airport

FROM bookings.flights f

WHERE departure_airport = '{airport}'

GROUP BY f.arrival_airport
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    
    aiports = cur.fetchall()
    closeConnection(cur)
    results = [x[0] for x in aiports]
    
    return {"results": results}
