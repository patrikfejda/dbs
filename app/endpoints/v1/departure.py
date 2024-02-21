
from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v1/departures")
async def departures(airport, day):
    daysReplace = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "0"
    }
    day = daysReplace[day]

    sql = f"""  
SELECT f.flight_id, f.flight_no, f.scheduled_departure

FROM bookings.flights_v f

WHERE departure_airport = '{airport}' AND EXTRACT(DOW FROM scheduled_departure) = '{day}' AND f.actual_departure IS NULL

ORDER BY scheduled_departure, flight_id
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    
    departures = cur.fetchall()
    closeConnection(cur)
    results = []
    for departure in departures:
        results.append({
            "flight_id": departure[0],
            "flight_no": departure[1],
            "scheduled_departure": departure[2]
        })


    return {"results": results}
