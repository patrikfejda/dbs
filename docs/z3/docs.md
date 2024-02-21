---
title: "Flights SQL"
subtitle: "Zadanie č. 3 z Predmetu Databázové systémy"
author: [Patrik Fejda]
date: "25.3.2023"
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
| **Úloha**        | Zadanie č. 3                                   |
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

Táto dokumentácia popisuje implementáciu HTTP end-pointov pre projekt zo Zadania 3.
Aplikácia číta dáta z datasetu flights.sql.
Implementácia sa uskutočňuje pomocou čistých SQL dopytov.
Časy v odpovediach budú vo formáte ISO8601 v UTC.

# **Endpointy**



## Endpoint 1 (2b)

Pre vybrané lietadlo vyberte sedadlo, ktoré bolo najčastejšie vybrané ako k-te v poradí tj.
musíte vedieť, ktoré sedadlo bolo vybrané najčastejšie ako prvé, druhé, tretie atď. V odpovedí
je vrátené označenie sedadla a počet jeho výberu na k-tom mieste.

Požiadavka: GET `/v3/aircrafts/{aircraft_code}/seats/{seat_choice}`

Príklad: GET `/v3/aircrafts/SU9/seats/2`

SQL Prompt: 

``` sql
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

```

Príklad odpovede:  

```json
{
    "result": {
        "seat": "19A",
        "count": 679
    }
}
```


---


## Endpoint 2 (2b)

Pre zadaný booking vypočítajte, koľko strávil pasažier spolu času vo vzduchu, na konci
každého letu tj. ak v rámci bookingu letel pasažier 5 letov a každý trval hodinu tak na konci
prvého letu strávil hodinu vo vzduchu, na konci druhého dve hodiny atď.
Primárne zoradenie je podľa ticket_no od najmenšieho po najväčšie a v rámci zoznamu letov,
je nutné dodržať poradie ako jednotlivé lety boli uskutočnené.

Požiadavka: GET `/v3/air-time/{book_ref}`

Príklad: GET `/v3/air-time/8D344B`

SQL Prompt: 

``` sql
SELECT 

x.ticket_no, x.passenger_name, x.departure_airport, x.arrival_airport, 

-- FLIGHT TIME V SEKUNDACH PREVEDENY NA HH:MM:SS
TO_CHAR((ROUND((x.flight_time_raw)) || ' second')::interval, 'FMHH24:MI:SS') AS flight_time,
-- THIS IS WHERE THE MAGIC HAPPENS
-- GROUPNEM SI PODLA PASSENGER NAME A ZORADIME OD NAJSTARSIEHO TICKETU
-- NASLEDNE VRAMCI DANYCH TICKETOV VYPOCITAME SUMU FLIGHT TIME RAW SEBA + PREDCHADZAJUCICH A NAFORMATUJEME NA HH:MM:SS
TO_CHAR((ROUND((SUM(x.flight_time_raw) OVER (PARTITION BY x.passenger_name ORDER BY x.passenger_name, x.actual_departure))) || ' second')::interval, 'FMHH24:MI:SS') AS total_time


FROM 
(
    -- VYTIAHNEM SI POLCIKA A FLIGHT TIME V SEKUNDACH
	SELECT 
	t.ticket_no, t.passenger_name, f.departure_airport, f.arrival_airport, f.actual_departure, EXTRACT(epoch FROM f.actual_arrival) - EXTRACT(epoch FROM f.actual_departure) AS flight_time_raw
	
    -- JOINNEM SI BOOKINGS, TICKETS A FLIGHTS
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
```

Príklad odpovede:  

```json
{
    "results": [
        {
            "ticket_no": "0005433589556",
            "passenger_name": "ALEKSANDR KISELEV",
            "flights": [
                {
                    "departure_airport": "SVO",
                    "arrival_airport": "LED",
                    "flight_time": "0:50:00",
                    "total_time": "0:50:00"
                },
                {
                    "departure_airport": "LED",
                    "arrival_airport": "IKT",
                    "flight_time": "5:54:00",
                    "total_time": "6:44:00"
                },
                {
                    "departure_airport": "IKT",
                    "arrival_airport": "LED",
                    "flight_time": "5:47:00",
                    "total_time": "12:31:00"
                },
                {
                    "departure_airport": "LED",
                    "arrival_airport": "SVO",
                    "flight_time": "0:51:00",
                    "total_time": "13:22:00"
                }
            ]
        },
        {
            "ticket_no": "0005433589557",
            "passenger_name": "DENIS FEDOROV",
            "flights": [
                {
                    "departure_airport": "SVO",
                    "arrival_airport": "LED",
                    "flight_time": "0:50:00",
                    "total_time": "0:50:00"
                },
                {
                    "departure_airport": "LED",
                    "arrival_airport": "IKT",
                    "flight_time": "5:54:00",
                    "total_time": "6:44:00"
                },
                {
                    "departure_airport": "IKT",
                    "arrival_airport": "LED",
                    "flight_time": "5:47:00",
                    "total_time": "12:31:00"
                },
                {
                    "departure_airport": "LED",
                    "arrival_airport": "SVO",
                    "flight_time": "0:51:00",
                    "total_time": "13:22:00"
                }
            ]
        }
    ]
}
```


---




## Endpoint 3 (2b)

Pre vybranú linku vypíšte sedadlá, ktoré boli najviac po sebe zarezervované spolu s počtom
po sebe neprerušených rezervácií a tiež s číslami letov, ktoré tvoria danú postupnosť. V rámci
výstupu sa môže dané sedadlo vyskytnúť viackrát. Úspešnú rezerváciu považujte aj let, ktorý
bol zrušený alebo len naplánovaný.

Po sebe idúcimi rezerváciami sa rozumie, že ak sedadlo bolo zarezervované pre prvý let aj
druhý let, ale v treťom lete nebolo zarezervované let, tak táto postupnosť je o veľkosti 2 a id
letov je 1 a 2.

Počet vrátených po sebe neprerušených rezervácií je určený parametrom limit, kde uvedená
hodnota, znamená koľko sérií vrátených endpointov.
Zoradenie v rámci odpovede je primárne podľa počtu po sebe idúcich rezervácií od
najväčšieho po najmenšie a následne podľa čísla sedadla (od najmenšieho po najväčšie).

V prípade rovnosti týchto dvoch parametrov je zoradenie podľa najmenšieho čísla letu
(flight_id). Zoradenie čísla letov je od najmenšieho po najväčšie.

Pri realizovaní tejto úlohy nie je možné použiť rekurziu.

Požiadavka: GET `/v3/airlines/{flight_no}/top_seats?limit={limit}`

Príklad: GET `/v3/airlines/PG0019/top_seats?limit=5`

SQL Prompt: 

``` sql
not implemented
```

Príklad odpovede:  

```json
not implemented
```

---

## Endpoint 4 (2b)

Pre vybraný typ lietadla vypíšte pre každý mesiac najúspešnejší deň v danom mesiaci
z pohľadu príjmu (suma za všetky letenky v daný deň). V rámci výpočtu príjmu sa berú iba
lietadla, ktoré skutočne odleteli ( majú vyplnený atribút actual_departure). Mesiac, pre ktorý
bol uskutočnený výpočet uvádzajte v tvare rok-mesiac napr. 2015-10.

Záznamy v odpovedi sú zoradené od najväčšieho príjmu po najmenší. Sekundárne zoradenie
je podľa mesiaca.


Požiadavka: GET `/v3/aircrafts/{aircraft_code}/top-incomes`

Príklad: GET `/v3/aircrafts/773/top-incomes`

SQL Prompt: 

``` sql
SELECT 	
	ROUND(amount),
	date_month,
	date_day

FROM (
	SELECT 
	date_month,
	date_day,
	amount,
	-- "ZORADIM" PRIDANIM ROW_NUMBER() OD MAX AMOUNT PO MIX AMOUNT
    ROW_NUMBER() OVER (PARTITION BY date_month ORDER BY amount DESC) AS row_number

	
	FROM (
        -- VRATIM DEN, MESIAC A SUMU ZA DEN
		SELECT TO_CHAR(f.flight_date, 'FMDD') as date_day, TO_CHAR(f.flight_date, 'YYYY-FMMM') AS date_month, SUM(tf.amount) as amount
	
		FROM 
		(
            -- SPRAVIM SI SUBSELECT NA ODLETENE LIETADLA Z AIRCRAFT KODOM URCENYM
            -- DA MI TO DATUM A FLIGHT_ID
			SELECT DATE(f.actual_departure) as flight_date, f.flight_id
			FROM bookings.flights as f	
			WHERE f.aircraft_code = '{aircraft_code}' AND f.actual_departure IS NOT NULL
		) as f
		
        -- JOINNEM KVOLI AMOUNT
		JOIN bookings.ticket_flights as tf
		ON tf.flight_id = f.flight_id
		
		
		GROUP BY f.flight_date
	) as day_amount

    ORDER BY amount DESC, date_month
) as subquery


-- TU SI VYBERIEM ZE CHCEM LEN TIE NAJZISKOVEJSIE VRAMCI SVOJEJ GROUP (VRAMCI DNA)
WHERE row_number = 1

```

Príklad odpovede:  

```json
{
    "results": [
        {
            "total_amount": 77115500,
            "month": "2016-9",
            "day": "23"
        },
        {
            "total_amount": 76521900,
            "month": "2017-1",
            "day": "11"
        },
        {
            "total_amount": 76199700,
            "month": "2017-2",
            "day": "27"
        },
        {
            "total_amount": 75943500,
            "month": "2017-4",
            "day": "3"
        },
        {
            "total_amount": 75890300,
            "month": "2017-6",
            "day": "11"
        },
        {
            "total_amount": 75829900,
            "month": "2017-8",
            "day": "11"
        },
        {
            "total_amount": 75793200,
            "month": "2016-11",
            "day": "20"
        },
        {
            "total_amount": 75743700,
            "month": "2017-7",
            "day": "16"
        },
        {
            "total_amount": 75490700,
            "month": "2017-3",
            "day": "25"
        },
        {
            "total_amount": 75241400,
            "month": "2016-10",
            "day": "3"
        },
        {
            "total_amount": 75161400,
            "month": "2017-5",
            "day": "15"
        },
        {
            "total_amount": 74862000,
            "month": "2016-12",
            "day": "2"
        },
        {
            "total_amount": 74523600,
            "month": "2016-8",
            "day": "29"
        }
    ]
}
```


---

