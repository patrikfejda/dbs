

from fastapi import APIRouter

from app.database import openConnection, closeConnection


router = APIRouter()


@router.get("/v1/flights/late-departure/{delay}")
async def agetBookingDetail(delay):
    cur = openConnection()
    sql = f"""    
SELECT flight_id, flight_no, delay

FROM (
    SELECT flight_id, flight_no, scheduled_departure, actual_departure, ROUND((EXTRACT(epoch FROM f.actual_departure) - EXTRACT(epoch FROM f.scheduled_departure))/60) delay
    FROM bookings.flights f
) subquery

WHERE delay > '{delay}' 

ORDER BY delay DESC, flight_id
    """
    cur.execute(
        sql
    )
    flights = cur.fetchall()
    closeConnection(cur)
    results = []
    for flight in flights:
        results.append(
            {"flight_id": flight[0], "flight_no": flight[1], "delay": flight[2]}
        )
    return {"results": results}
