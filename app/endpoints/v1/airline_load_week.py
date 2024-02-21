

from fastapi import APIRouter

from app.database import openConnection, closeConnection
 
router = APIRouter()

@router.get("/v1/airlines/{flight_no}/load-week")
async def departures(flight_no):
    sql = f"""  
SELECT flight_no, day, ROUND(CAST(SUM(load) as decimal) / SUM(capacity) * 100, 2)

FROM (
	SELECT f.flight_no, capacity_in_aircrafts.capacity, load_in_flight.load, EXTRACT(DOW FROM f.scheduled_departure) as day
	
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
) subquery

GROUP BY day, flight_no

ORDER BY day
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    days = cur.fetchall()
    closeConnection(cur) 
    result = {
        'flight_no': days[0][0],
        'sunday': days[0][2],
        'monday': days[1][2],
        'tuesday': days[2][2],
        'wednesday': days[3][2],
        'thursday': days[4][2],
        'friday': days[5][2],
        'saturday': days[6][2]
    }
    
    return {"result": result}
