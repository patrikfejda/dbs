
from fastapi import APIRouter

from app.database import openConnection, closeConnection
from collections import defaultdict

 
router = APIRouter()

@router.get("/v3/air-time/{book_ref}")
async def airtime(book_ref):

    sql = f"""  
SELECT 

x.ticket_no, x.passenger_name, x.departure_airport, x.arrival_airport, 

TO_CHAR((ROUND((x.flight_time_raw)) || ' second')::interval, 'FMHH24:MI:SS') AS flight_time,
TO_CHAR((ROUND((SUM(x.flight_time_raw) OVER (PARTITION BY x.passenger_name ORDER BY x.passenger_name, x.actual_departure))) || ' second')::interval, 'FMHH24:MI:SS') AS total_time


FROM 
(
	SELECT 
	t.ticket_no, t.passenger_name, f.departure_airport, f.arrival_airport, f.actual_departure, EXTRACT(epoch FROM f.actual_arrival) - EXTRACT(epoch FROM f.actual_departure) AS flight_time_raw
	
	FROM bookings.bookings as b
	
	JOIN bookings.tickets as t
	ON t.book_ref = b.book_ref
	
	JOIN bookings.ticket_flights as tf
	ON tf.ticket_no = t.ticket_no
	
	JOIN bookings.flights as f
	ON f.flight_id = tf.flight_id
	
	WHERE b.book_ref = '{book_ref}'

) x

ORDER BY x.ticket_no ASC
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    
    flights = cur.fetchall()
    closeConnection(cur)
    
    grouped_data = defaultdict(list)

    for item in flights:
        key = (item[0], item[1])
        flight = {
            'departure_airport': item[2],
            'arrival_airport': item[3],
            'flight_time': item[4],
            'total_time': item[5]
        }
        grouped_data[key].append(flight)

    results = []
    for key, flights in grouped_data.items():
        ticket_no, passenger_name = key
        results.append({
            'ticket_no': ticket_no,
            'passenger_name': passenger_name,
            'flights': flights
        })


    return {"results": results}
