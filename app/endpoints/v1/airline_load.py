
from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v1/airlines/{flight_no}/load")
async def departures(flight_no):
    sql = f"""
SELECT f.flight_id, capacity_in_aircrafts.capacity, load_in_flight.load, ROUND(CAST(load_in_flight.load as decimal) / capacity_in_aircrafts.capacity * 100, 2) percentage_load

FROM bookings.flights f

JOIN (
	SELECT s.aircraft_code, COUNT(s.seat_no) capacity
	FROM bookings.seats s
	GROUP BY s.aircraft_code
) capacity_in_aircrafts
ON f.aircraft_code = capacity_in_aircrafts.aircraft_code

JOIN (
	SELECT tf.flight_id, COUNT(tf.ticket_no) load
	FROM bookings.ticket_flights tf
	GROUP BY tf.flight_id
) load_in_flight
ON f.flight_id = load_in_flight.flight_id

WHERE f.flight_no = '{flight_no}'
    """

    cur = openConnection()
    cur.execute(
        sql
    )
    
    flights = cur.fetchall()
    closeConnection(cur)
    results = []
    for flight in flights:
        results.append(
            {"id": flight[0], "aircraft_capacity": flight[1], "load": flight[2], "percentage_load": 100 if flight[3] == 100 else flight[3]}
        )
    
    return {"results": results}

