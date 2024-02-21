from fastapi import APIRouter

from app.endpoints.v1 import (
    hello,
    health,
    status,
    booking,
    flight_late,
    passenger_companions,
    top_airline,
    departure,
    airport_destinations,
    airline_load_week,
    airline_load,
)

from app.endpoints.v3 import (
    aircraft_seats,
    air_time,
    top_incomes,
    top_seats,
)

router = APIRouter()
router.include_router(hello.router, tags=["hello"])
router.include_router(health.router, tags=["health"])
router.include_router(status.router, tags=["hello"])
router.include_router(booking.router)
router.include_router(flight_late.router)
router.include_router(passenger_companions.router)
router.include_router(top_airline.router)
router.include_router(departure.router)
router.include_router(airport_destinations.router)
router.include_router(airline_load_week.router)
router.include_router(airline_load.router)
router.include_router(aircraft_seats.router)
router.include_router(air_time.router)
router.include_router(top_incomes.router)
router.include_router(top_seats.router)
