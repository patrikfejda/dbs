

from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()


@router.get("/v1/bookings/{booking_id}")
async def agetBookingDetail(booking_id):
    sql = f"""
SELECT b.book_ref, b.book_date, t.ticket_no, t.passenger_id, t.passenger_name, bp.boarding_no, f.flight_no, bp.seat_no, f.aircraft_code, f.arrival_airport, f.departure_airport, f.scheduled_arrival, f.scheduled_departure

FROM bookings.tickets t

JOIN bookings.bookings b ON b.book_ref = t.book_ref 

JOIN bookings.boarding_passes bp ON bp.ticket_no = t.ticket_no

JOIN bookings.flights f ON f.flight_id = bp.flight_id

WHERE t.book_ref = '{booking_id}'

ORDER BY t.ticket_no, bp.boarding_no;    
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    tickets = cur.fetchall()
    closeConnection(cur)
    result = {
        "id": tickets[0][0],
        "book_date": tickets[0][1],
        "boarding_passes": []
    }
    for ticket in tickets:
        result['boarding_passes'].append({
            "id": ticket[2],
            "passenger_id": ticket[3],
            "passenger_name": ticket[4],
            "boarding_no": ticket[5],
            "flight_no": ticket[6],
            "seat": ticket[7],
            "aircraft_code": ticket[8],
            "arrival_airport": ticket[9],
            "departure_airport": ticket[10],
            "scheduled_arrival": ticket[11],
            "scheduled_departure": ticket[12]
        })

    return {"result": result}
