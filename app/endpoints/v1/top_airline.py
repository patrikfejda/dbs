

from fastapi import APIRouter

from app.database import openConnection, closeConnection


router = APIRouter()


@router.get("/v1/top-airlines")
async def agetBookingDetail(limit):
    sql = f"""  
SELECT flight_no, passenger_count

FROM (
  SELECT f.flight_no, COUNT(*) passenger_count
  FROM bookings.flights f
  JOIN bookings.boarding_passes bp ON bp.flight_id = f.flight_id
  
  WHERE f.status = 'Arrived'
  
  GROUP BY f.flight_no
) subquery
ORDER BY passenger_count DESC, flight_no

LIMIT {limit}
    """
    cur = openConnection()
    cur.execute(
        sql
    )
    
    airlines = cur.fetchall()
    closeConnection(cur)
    results = []
    for airline in airlines:
        results.append({
            "flight_no": airline[0],
            "count": airline[1]
        })
    
    return {"results": results}
