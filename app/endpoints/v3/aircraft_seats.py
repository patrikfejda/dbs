from fastapi import APIRouter

from app.database import openConnection, closeConnection


router = APIRouter()


@router.get("/v3/aircrafts/{aircraft_code}/seats/{seat_choice}")
async def seats(aircraft_code, seat_choice):

    sql = f"""  

SELECT seat_no, COUNT(*)
FROM (
    
    -- POUZIVAM DENSE RANK A NIE RANK, LEBO NECHCEM MAT PRAZDNE RANKY, AKO JE TO V RANK
    SELECT flight_id, seat_no, DENSE_RANK() OVER (PARTITION BY flight_id ORDER BY book_date) AS seat_rank
    
    -- DOSTANME TABULKU KDE MAM LET, SEDADLO A KEBY BOLO SEDADLO BOOKNUTE
    FROM (
        SELECT f.flight_id, bp.seat_no, b.book_date

        -- TOTO ROBIM AKO SUBSELECT ABY SOM NEMUSEL KAZDY LET JOINNOVAT, IBA TIE KTORE SU PRE DANU LETADLO
        FROM (
            SELECT f.flight_id
            FROM bookings.flights as f
            WHERE f.aircraft_code = '{aircraft_code}'
        ) AS f

        -- JOINNEM SI TO S BP, T, B
        -- POUZIVAM BP A NIE TF KVOLI SEAT_NO
        JOIN bookings.boarding_passes as bp
        ON bp.flight_id = f.flight_id

        JOIN bookings.tickets as t
        ON t.ticket_no = bp.ticket_no

        JOIN bookings.bookings as b
        ON t.book_ref = b.book_ref

    ) AS subquery
) AS subquery

-- TU UZ SI LEN VYBERIEM DANY SEAT CHOICE
WHERE seat_rank = {seat_choice}
-- ORDERNEM OD NAJVIAC BOOKNUTYCH A VYBERIEM PRVY
GROUP BY seat_no
ORDER BY COUNT(*) DESC
LIMIT 1;

    """
    cur = openConnection()
    cur.execute(sql)

    seat = cur.fetchall()
    closeConnection(cur)
    result = {"seat": seat[0][0], "count": seat[0][1]}

    return {"result": result}
