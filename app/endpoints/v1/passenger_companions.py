


from fastapi import APIRouter

from app.database import openConnection, closeConnection


router = APIRouter()


@router.get("/v1/passengers/{passenger_id}/companions")
async def agetBookingDetail(passenger_id):
    sql = f"""  
SELECT t.passenger_id, t.passenger_name, COUNT(*) flights_count, ARRAY_AGG(tf.flight_id ORDER BY tf.flight_id) common_flights

FROM 
(
	SELECT f.flight_id
	FROM bookings.tickets t
	
    JOIN bookings.ticket_flights tf ON tf.ticket_no = t.ticket_no
	
    JOIN bookings.flights f ON tf.flight_id = f.flight_id
	
    WHERE t.passenger_id = '{passenger_id}'
) commons_flights

JOIN bookings.ticket_flights tf ON tf.flight_id = commons_flights.flight_id

JOIN bookings.tickets t ON tf.ticket_no = t.ticket_no

WHERE t.passenger_id != '{passenger_id}'

GROUP BY t.passenger_name, t.passenger_id

ORDER BY flights_count desc, t.passenger_id
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    
    companions = cur.fetchall()
    closeConnection(cur)

    results = []
    for companion in companions:
        results.append({
            "flights": companion[3],
            "flights_count": companion[2],
            "id": companion[0],
            "name": companion[1],
        })

    return {"results": results}
