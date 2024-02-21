---
title: "Flights SQL"
subtitle: "Zadanie č. 2 z Predmetu Databázové systémy"
author: [Patrik Fejda]
date: "7.3.2023"
keywords: [Markdown, Example]
titlepage: true
titlepage-color: "423f3b"
titlepage-text-color: "FFFAFA"
titlepage-rule-color: "FFFAFA"
titlepage-rule-height: 2
---
\pagebreak
# **Informácie o práci**

|                  |                                                |
| ---------------- | ---------------------------------------------- |
| **Názov**        | Flights SQL                                    |
| **Úloha**        | Zadanie č. 2                                   |
| **Autor**        | Patrik Fejda                                   |
| **Univerzita**   | Slovenská technická univerzita v Bratislave    |
| **Fakulta**      | Fakulta informatiky a informačných technológií |
| **Predmet**      | DBS_B - Databázové systémy                     |
| **Rok**          | 2022/2023 Letný semester                       |
| **Cvičiaci**     | Ing. Martin Binder                             |
| **Prednášajúci** | Ing. Rastislav Bencel, PhD.                    |
| **Skupina**      | Pondelok 16:00                                 |

\pagebreak

# **Úvod**

Táto dokumentácia popisuje implementáciu HTTP end-pointov pre projekt zo Zadania 2. 
Aplikácia číta dáta z datasetu flights.sql. 
Implementácia sa uskutočňuje pomocou čistých SQL dopytov.
Časy v odpovediach budú vo formáte ISO8601 v UTC. 

# **Endpointy**



## Endpoint - zoznam spolucestujúcich (1b)

Pre konkrétneho pasažiera identifikovaného pomocou passenger_id je potrebné vrátiť
všetkých spolucestujúcich, ktorý kedy s ním cestovali. Pri spolucestujúcich je potrebné uviesť
aj čísla letov (flight_id), na ktorých boli spolucestujúci.
Jednotlivé nájdené záznamy je potrebné zoradiť podľa počtu spoločných letov od najväčšieho
po najmenšie a sekundárne zoradenie je podľa id spolucestujúceho ( passenger_id) od
najmenšieho po najväčšieho.

Požiadavka: GET `/v1/passengers/{passenger_id}/companions`

Príklad: GET `v1/passengers/5260%20236351/companions`

SQL Prompt: 

``` sql
-- dostanem tabulku
-- id, meno, flight_id
-- spocitam flights_count a agregatnem zoznam letov
SELECT t.passenger_id, t.passenger_name, COUNT(*) flights_count, ARRAY_AGG(tf.flight_id ORDER BY tf.flight_id) common_flights

-- subselect mi vrati vsetky lety daneho pasaziera
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

-- pomoocou joinu cez m2m table som dostal vsetky tickety na dane flights

-- sama sebe nie si spolucestujuci
WHERE t.passenger_id != '{passenger_id}'

-- group podla pasaziera
GROUP BY t.passenger_name, t.passenger_id

ORDER BY flights_count desc, t.passenger_id

```

Príklad odpovede:  

```json
{
    "results": [
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "0725 420471",
            "name": "VLADIMIR BARANOV"
        },
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "0775 008320",
            "name": "YURIY GRIGOREV"
        },
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "7138 903879",
            "name": "ALEKSEY KUZMIN"
        },
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "9100 378405",
            "name": "YURIY VASILEV"
        },
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "9560 954090",
            "name": "LYUDMILA OSIPOVA"
        },
        {
            "flights": [
                36747,
                99516
            ],
            "flights_count": 2,
            "id": "9855 258848",
            "name": "OLEG BONDARENKO"
        },
        {
            "flights": [
                36747
            ],
            "flights_count": 1,
            "id": "0061 348750",
            "name": "EVGENIYA MOROZOVA"
        },
        {
            "flights": [
                36747
            ],
            "flights_count": 1,
            "id": "0377 367514",
            "name": "SERGEY SMIRNOV"
        },
        ...
    ]
}
```


---

## Endpoint - detail letu (0,5b)

Pre zvolenú rezerváciu (book_ref), vráti jej kompletný detail. Jednotlivé atribúty sú ukázané
v ukážkovej odpovedi. Položky v boarding_passes zoradte podľa id a boardning_no.

Požiadavka: GET `/v1/bookings/:booking_id`

Príklad: GET `/v1/bookings/000067`


SQL Prompt: 

``` sql
-- zoberiem potrebne stlpce z boarding_passes, flights a tickets
SELECT b.book_ref, b.book_date, t.ticket_no, t.passenger_id, t.passenger_name, bp.boarding_no, f.flight_no, bp.seat_no, f.aircraft_code, f.arrival_airport, f.departure_airport, f.scheduled_arrival, f.scheduled_departure

-- tickets joinem s boarding_passes a flights
FROM bookings.tickets t

JOIN bookings.bookings b ON b.book_ref = t.book_ref 

JOIN bookings.boarding_passes bp ON bp.ticket_no = t.ticket_no

JOIN bookings.flights f ON f.flight_id = bp.flight_id

WHERE t.book_ref = '{booking_id}'

ORDER BY t.ticket_no, bp.boarding_no;
```


Príklad odpovede:  

```json
{
    "result": {
        "id": "000067",
        "book_date": "2016-08-11T18:36:00+00:00",
        "boarding_passes": [
            {
                "id": "0005434482035",
                "passenger_id": "1361 389085",
                "passenger_name": "ANNA CHERNOVA",
                "boarding_no": 8,
                "flight_no": "PG0156",
                "seat": "2A",
                "aircraft_code": "CR2",
                "arrival_airport": "NJC",
                "departure_airport": "LED",
                "scheduled_arrival": "2016-08-24T15:30:00+00:00",
                "scheduled_departure": "2016-08-24T11:55:00+00:00"
            },
            {
                "id": "0005434482035",
                "passenger_id": "1361 389085",
                "passenger_name": "ANNA CHERNOVA",
                "boarding_no": 8,
                "flight_no": "PG0157",
                "seat": "5D",
                "aircraft_code": "CR2",
                "arrival_airport": "LED",
                "departure_airport": "NJC",
                "scheduled_arrival": "2016-08-29T15:25:00+00:00",
                "scheduled_departure": "2016-08-29T11:50:00+00:00"
            },
            {
                "id": "0005434482036",
                "passenger_id": "8193 811215",
                "passenger_name": "MAKSIM BORISOV",
                "boarding_no": 6,
                "flight_no": "PG0157",
                "seat": "22D",
                "aircraft_code": "CR2",
                "arrival_airport": "LED",
                "departure_airport": "NJC",
                "scheduled_arrival": "2016-08-29T15:25:00+00:00",
                "scheduled_departure": "2016-08-29T11:50:00+00:00"
            },
            {
                "id": "0005434482036",
                "passenger_id": "8193 811215",
                "passenger_name": "MAKSIM BORISOV",
                "boarding_no": 7,
                "flight_no": "PG0156",
                "seat": "1C",
                "aircraft_code": "CR2",
                "arrival_airport": "NJC",
                "departure_airport": "LED",
                "scheduled_arrival": "2016-08-24T15:30:00+00:00",
                "scheduled_departure": "2016-08-24T11:55:00+00:00"
            }
        ]
    }
}
```


---

## Endpoint - neskoré odlety (0,5b)

Endpoint vráti všetky odlety, ktoré meškali minimálne X minút (podľa vstupu). Výsledok
zoraďte podľa dĺžky meškania od najväčšieho po najmenšie (v prípade zhody použite
flight_id).

Požiadavka: GET `/v1/flights/late-departure/:delay`

Príklad: GET `/v1/flights/late-departure/270`



SQL Prompt: 

``` sql
SELECT flight_id, flight_no, delay

-- pouzijem subquery, kvoli performance a WHERE
FROM (
    -- delat pocitam ako rozdiel medzi actual_departure a scheduled_departure (pouzivam 1.1.1970)
    SELECT flight_id, flight_no, scheduled_departure, actual_departure, ROUND((EXTRACT(epoch FROM f.actual_departure) - EXTRACT(epoch FROM f.scheduled_departure))/60) delay
    FROM bookings.flights f
) subquery

WHERE delay > '{delay}' 

ORDER BY delay DESC, flight_id
```


Príklad odpovede:  

```json
{
    "results": [
        {
            "flight_id": 157571,
            "flight_no": "PG0073",
            "delay": 303
        },
        {
            "flight_id": 186524,
            "flight_no": "PG0040",
            "delay": 284
        },
        {
            "flight_id": 126166,
            "flight_no": "PG0533",
            "delay": 282
        },
        {
            "flight_id": 56731,
            "flight_no": "PG0132",
            "delay": 281
        },
        {
            "flight_id": 102938,
            "flight_no": "PG0531",
            "delay": 281
        },
        {
            "flight_id": 95155,
            "flight_no": "PG0589",
            "delay": 277
        },
        {
            "flight_id": 202435,
            "flight_no": "PG0560",
            "delay": 276
        },
        {
            "flight_id": 95821,
            "flight_no": "PG0590",
            "delay": 274
        },
        {
            "flight_id": 172649,
            "flight_no": "PG0201",
            "delay": 272
        },
        {
            "flight_id": 58561,
            "flight_no": "PG0114",
            "delay": 271
        }
    ]
}
```


---

## Endpoint - Linky, ktoré obslúžili najviac pasažierov (0,5b)

V rámci endpointu vráťte linky (flight_no), ktoré obslúžili najviac pasažierov. Počet
zobrazených záznamov je definovaný v rámci požiadavky. Výsledok je zoradený podľa count
a flight_no.

Požiadavka: GET `/v1/top-airlines?limit=:limit`

Príklad: GET `/v1/top-airlines?limit=20`



SQL Prompt: 

``` sql
SELECT flight_no, passenger_count

-- subquery vrati flight_no a pocet pasazerov (pocet bp)
FROM (
  SELECT f.flight_no, COUNT(*) passenger_count
  
  FROM bookings.flights f
  JOIN bookings.boarding_passes bp ON bp.flight_id = f.flight_id
  
  -- tento riadok mi trval asi 3 hodiny :)
  WHERE f.status = 'Arrived'
  
  GROUP BY f.flight_no
) subquery
ORDER BY passenger_count DESC, flight_no

LIMIT {limit}
```


Príklad odpovede:  

```json
{
    "results": [
        {
            "flight_no": "PG0222",
            "count": 124392
        },
        {
            "flight_no": "PG0225",
            "count": 121812
        },
        {
            "flight_no": "PG0223",
            "count": 120179
        },
        {
            "flight_no": "PG0226",
            "count": 117843
        },
        {
            "flight_no": "PG0224",
            "count": 117830
        },
        {
            "flight_no": "PG0013",
            "count": 112745
        },
        {
            "flight_no": "PG0277",
            "count": 101205
        },
        {
            "flight_no": "PG0412",
            "count": 100032
        },
        {
            "flight_no": "PG0278",
            "count": 98133
        },
        {
            "flight_no": "PG0413",
            "count": 96489
        },
        {
            "flight_no": "PG0208",
            "count": 74834
        },
        {
            "flight_no": "PG0209",
            "count": 72336
        },
        {
            "flight_no": "PG0220",
            "count": 65436
        },
        {
            "flight_no": "PG0221",
            "count": 63195
        },
        {
            "flight_no": "PG0470",
            "count": 62072
        },
        {
            "flight_no": "PG0529",
            "count": 61933
        },
        {
            "flight_no": "PG0227",
            "count": 60309
        },
        {
            "flight_no": "PG0530",
            "count": 60174
        },
        {
            "flight_no": "PG0561",
            "count": 59582
        },
        {
            "flight_no": "PG0562",
            "count": 56590
        }
    ]
}
```

## Endpoint – naplánované linky (0,5b)

Endpoint vráti naplánované lety (flight_id) spolu s informáciou, ku ktorej linke patri daný let
pre konkrétny deň v týždni a konkrétne letisko. V požiadavky sa používa číslo pre poradie
dňa v týždni a kód letiska pre označenie letiska. Výsledok zoraďte podľa
scheduled_departure od najbližších a v prípade zhody použite flight_id.

Požiadavka: GET `/v1/departures?airport=:airport&day=:day`

Príklad: GET `/v1/departures?airport=KJA&day=7`



SQL Prompt: 

``` sql
SELECT f.flight_id, f.flight_no, f.scheduled_departure

FROM bookings.flights_v f

-- posledna podmienka znamena ze let este neodletel
WHERE departure_airport = '{airport}' AND EXTRACT(DOW FROM scheduled_departure) = '{day}' AND f.actual_departure IS NULL

ORDER BY scheduled_departure, flight_id
```


Príklad odpovede:  

```json
{
    "results": [
        {
            "flight_id": 91972,
            "flight_no": "PG0689",
            "scheduled_departure": "2017-08-20T04:25:00+00:00"
        },
        {
            "flight_id": 90188,
            "flight_no": "PG0207",
            "scheduled_departure": "2017-08-20T04:35:00+00:00"
        },
        {
            "flight_id": 93328,
            "flight_no": "PG0352",
            "scheduled_departure": "2017-08-20T04:50:00+00:00"
        },
        {
            "flight_id": 92440,
            "flight_no": "PG0021",
            "scheduled_departure": "2017-08-20T05:25:00+00:00"
        },
        {
            "flight_id": 89840,
            "flight_no": "PG0548",
            "scheduled_departure": "2017-08-20T05:40:00+00:00"
        },
        {
            "flight_id": 94027,
            "flight_no": "PG0673",
            "scheduled_departure": "2017-08-20T06:10:00+00:00"
        },
        {
            "flight_id": 93327,
            "flight_no": "PG0351",
            "scheduled_departure": "2017-08-20T06:15:00+00:00"
        },
        {
            "flight_id": 90928,
            "flight_no": "PG0623",
            "scheduled_departure": "2017-08-20T07:00:00+00:00"
        },
        {
            "flight_id": 90211,
            "flight_no": "PG0206",
            "scheduled_departure": "2017-08-20T07:20:00+00:00"
        },
        {
            "flight_id": 92649,
            "flight_no": "PG0653",
            "scheduled_departure": "2017-08-20T08:25:00+00:00"
        },
        {
            "flight_id": 91697,
            "flight_no": "PG0626",
            "scheduled_departure": "2017-08-20T08:35:00+00:00"
        },
        {
            "flight_id": 93831,
            "flight_no": "PG0501",
            "scheduled_departure": "2017-08-20T09:25:00+00:00"
        },
        {
            "flight_id": 91398,
            "flight_no": "PG0625",
            "scheduled_departure": "2017-08-20T10:10:00+00:00"
        },
        {
            "flight_id": 92130,
            "flight_no": "PG0689",
            "scheduled_departure": "2017-08-27T04:25:00+00:00"
        },
        {
            "flight_id": 90147,
            "flight_no": "PG0207",
            "scheduled_departure": "2017-08-27T04:35:00+00:00"
        }
        ...
    ]
}
```


---

## Endpoint - Vypíšte všetky destinácie zo zadaného letiska (0,5b)

Endpoint vráti všetky destinácie, ku ktorým je možné letieť zo zadaného letiska. Výsledky je
potrebné zoradiť podľa abecedy. V odpovedi sa vracajú kódy letiska.
Výsledky zoradte podľa abecety. Vrátte kódy letiska (bookings.flights.arrival_airport).

Požiadavka: GET `/v1/airports/:airport/destinations`

Príklad: GET `/v1/airports/VVO/destinations`


SQL Prompt: 

``` sql
-- toto je tak straight forward ze to nemusim vysvetlovat
SELECT f.arrival_airport

FROM bookings.flights f

WHERE departure_airport = '{airport}'

GROUP BY f.arrival_airport
```


Príklad odpovede:  

```json
{
    "results": [
        "IKT",
        "KHV",
        "VKO"
    ]
}
```

## Endpoint – vyťaženosť letov pre konkrétnu linku (1b)

Pre konkrétnu linku flight_no zistite vyťaženosť jednotlivých letov (flight_id). Výpočet
vyťaženosti uveďte v percentách so zaokrúhlením na dve desatinné miesta.
Zoradenie uskutočnite podľa id letu (flight_id) od najmenšieho po najväčšie.

Požiadavka: GET `/v1/airlines/:flight_no/load`

Príklad: GET `/v1/airlines/PG0242/load`



SQL Prompt: 

``` sql
-- percentage_load = load / capacity * 100
SELECT f.flight_id, capacity_in_aircrafts.capacity, load_in_flight.load, ROUND(CAST(load_in_flight.load as decimal) / capacity_in_aircrafts.capacity * 100, 2) percentage_load

FROM bookings.flights f

-- vypocitam capacitu lietadla cez spociatocne sedadiel
-- JOINNEM to s danym flight cez (flight > aircraft > count(seats))
JOIN (
	SELECT s.aircraft_code, COUNT(s.seat_no) capacity
	FROM bookings.seats s
	GROUP BY s.aircraft_code
) capacity_in_aircrafts
ON f.aircraft_code = capacity_in_aircrafts.aircraft_code

-- vypocitam load cez spocitanie ticketov
-- JOINNEM to s danym flight cez (flight > ticket_flights > count(ticket))
JOIN (
	SELECT tf.flight_id, COUNT(tf.ticket_no) load
	FROM bookings.ticket_flights tf
	GROUP BY tf.flight_id
) load_in_flight
ON f.flight_id = load_in_flight.flight_id

WHERE f.flight_no = '{flight_no}'
```


Príklad odpovede:  

```json
{
    "results": [
        {
            "id": 187636,
            "aircraft_capacity": 97,
            "load": 82,
            "percentage_load": 84.54
        },
        {
            "id": 187644,
            "aircraft_capacity": 97,
            "load": 80,
            "percentage_load": 82.47
        },
        {
            "id": 187479,
            "aircraft_capacity": 97,
            "load": 79,
            "percentage_load": 81.44
        },
        {
            "id": 187560,
            "aircraft_capacity": 97,
            "load": 92,
            "percentage_load": 94.85
        },
        {
            "id": 187744,
            "aircraft_capacity": 97,
            "load": 76,
            "percentage_load": 78.35
        }
        ...
    ]
}
```


---

## Endpoint - Priemerná vyťaženosť linky pre jednotlivé dni v týždni (0,5b)

Pre konkrétnu linku flight_no zistite priemernú vyťaženosť pasažiermi pre konkrétne dni
v týždni tj. pondelok, utorok.
Jednotlivé dni v rámci odpovede sú zoradené od pondelka do nedele.

Požiadavka: GET `/v1/airlines/:flight_no/load-week`
Priklad: GET `/v1/airlines/PG0242/load-week`



SQL Prompt: 

``` sql
SELECT flight_no, day, ROUND(CAST(SUM(load) as decimal) / SUM(capacity) * 100, 2)

-- predosle query som pouzil ako subquery (/load)
-- a pridal som tam day vypocitany z scheduled_departure
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

-- uz som si to len groupol a zoradil
GROUP BY day, flight_no

ORDER BY day
```


Príklad odpovede:  

```json
{
    "result": {
        "flight_no": "PG0242",
        "sunday": 82.88,
        "monday": 81.17,
        "tuesday": 82.66, # fixme
        "wednesday": 84.81,
        "thursday": 79.8,
        "friday": 82.25,
        "saturday": 80.25
    }
}
```
