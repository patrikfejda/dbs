
from fastapi import APIRouter

from app.database import openConnection, closeConnection

 
router = APIRouter()

@router.get("/v3/aircrafts/{aircraft_code}/top-incomes")
async def seats(aircraft_code):

    sql = f"""  
SELECT 	
	ROUND(amount),
	date_month,
	date_day

FROM (
	SELECT 
	date_month,
	date_day,
	amount,
	ROW_NUMBER() OVER (PARTITION BY date_month ORDER BY amount DESC) AS row_number
	
	FROM (
		SELECT TO_CHAR(f.flight_date, 'FMDD') as date_day, TO_CHAR(f.flight_date, 'YYYY-FMMM') AS date_month, SUM(tf.amount) as amount
	
		FROM 
		(
			SELECT DATE(f.actual_departure) as flight_date, f.flight_id
			FROM bookings.flights as f	
			WHERE f.aircraft_code = '{aircraft_code}' AND f.actual_departure IS NOT NULL
		) as f
		
		JOIN bookings.ticket_flights as tf
		ON tf.flight_id = f.flight_id
		
		
		GROUP BY f.flight_date
	) as day_amount

    ORDER BY amount DESC, date_month
) as subquery

WHERE row_number = 1
    """
    
    cur = openConnection()
    cur.execute(
        sql
    )
    
    days = cur.fetchall()
    closeConnection(cur)

    results = []
    for day in days:
        results.append({
            "total_amount": day[0],
            "month": day[1],
            "day": day[2]
        })

    return {"results": results}




"""
SELECT seat_no, COUNT(*) as choice_count

FROM (

	SELECT * 
	
	FROM (
		SELECT flight_idx, book_date, seat_no, ROW_NUMBER() OVER (PARTITION BY flight_idx ORDER BY book_date) AS row_number
		
		FROM (
		
			SELECT f.flight_id as flight_idx, *
			FROM (
				SELECT f.aircraft_code, f.flight_id
			
				FROM bookings.flights as f
				
				WHERE f.aircraft_code = 'SU9'
			) AS f
			
			JOIN bookings.boarding_passes as bp
			ON bp.flight_id = f.flight_id
			
			JOIN bookings.tickets as t
			ON t.ticket_no = bp.ticket_no
			
			JOIN bookings.bookings as b
			ON t.book_ref = b.book_ref    
		
		) subselect
	) subselect	
	WHERE row_number = 2
) subselect

GROUP BY seat_no

ORDER BY choice_count DESC

"""



"""
	SELECT seat_no, COUNT(*) as choice_count

FROM (

	SELECT * 
	
	FROM (
		SELECT flight_idx, book_date, seat_no, ROW_NUMBER() OVER (PARTITION BY flight_idx ORDER BY book_date) AS row_number
		
		FROM (
		
			SELECT f.flight_id as flight_idx, *
			FROM (
				SELECT f.aircraft_code, f.flight_id
			
				FROM bookings.flights as f
				
				WHERE f.aircraft_code = 'SU9'
			) AS f
			
			JOIN bookings.boarding_passes as bp
			ON bp.flight_id = f.flight_id
			
			JOIN bookings.tickets as t
			ON t.ticket_no = bp.ticket_no
			
			JOIN bookings.bookings as b
			ON t.book_ref = b.book_ref    
		
		) subselect
	) subselect	
	WHERE row_number = 2
) subselect

GROUP BY seat_no

ORDER BY choice_count DESC
	
	
"""