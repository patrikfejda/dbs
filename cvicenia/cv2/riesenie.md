1. Vypíšte všetky mená hráčov
Pozn. Bez dátumu narodenia

```sql
SELECT firstname, lastname FROM players;
```

2. Vypíšte názvy tímov, ktorých salary je väčší ako 70000

```sql
SELECT name FROM teams WHERE salary > 70000;
```

3. Vypíšte názvy tímov, ktorých salary je väčší ako 70000 a meno majiteľa je „Dusan“

```sql
SELECT name FROM teams WHERE salary > 70000 and owner = 'Dusan';
```

4. Vypíšte mena a priezviska hráčov s počtom odohratých zápasov pre jednotlivé sezóny.
Ak hráč neodohral žiadnu sezónu tak sa vo výpise nezobrazí a v prípade, že hráč
nastupoval v rámci rovnakej sezóny za viacero klubov, tak to považujte ako dve
rozdielne sezóny (nezaoberáte sa agregáciou daných záznamov do jedného).

```sql
SELECT firstname, lastname, games, season_id FROM players INNER JOIN player_statistics ON players.id = player_statistics.player_id;
```

5. Vypíšte mena hráčov aj s názvom sezóny, v ktorých odohrali nejaký zápas.

```sql
SELECT firstname, lastname, name FROM player_statistics INNER JOIN seasons ON player_statistics.season_id = seasons.id INNER JOIN players ON player_statistics.player_id = players.id
```

6. Vypíšte mena hráčov, názov sezóny a počet bodov (góly + asistencie) pre jednotlivých
hráčov, ktoré dosiahli v jednotlivých sezónach. Počet bodov pomenujte názvom
„points“.

```sql
SELECT firstname, lastname, name, goals, assists, goals + assists AS points FROM player_statistics INNER JOIN seasons ON player_statistics.season_id = seasons.id INNER JOIN players ON player_statistics.player_id = players.id
```

7. Úlohu 6 uskutočnite pre všetkých hráčov bez ohľadu na to ci odohrali nejakú sezónu.
Ak neodohrali žiadnu sezónu v stĺpci points uveďte 0 a v stĺpci s názvom sezóna- „no
season“

```sql
SELECT firstname, lastname,
CASE
    WHEN name IS NULL THEN 'no-season'
    ELSE name
END,
CASE
    WHEN goals IS NULL THEN 0
    WHEN assists IS NULL THEN 0
    ELSE goals + assists
END AS points FROM player_statistics FULL JOIN seasons ON player_statistics.season_id = seasons.id FULL JOIN players ON player_statistics.player_id = players.id
```

8. Vypíšte mena hráčov s názvami tímov ,za ktoré hrali. V prípade ze hráč nehral za
žiadny tím tak sa vo výsledku neobjaví.

```sql
SELECT firstname, lastname, teams.name FROM player_statistics INNER JOIN players ON players.id = player_statistics.player_id JOIN teams ON teams.id = player_statistics.team_id 
```

9. Výsledok z 8 úlohy zoraďte podľa názvu tímu

```sql
SELECT firstname, lastname, teams.name FROM player_statistics INNER JOIN players ON players.id = player_statistics.player_id JOIN teams ON teams.id = player_statistics.team_id 
ORDER BY teams.name
```

10. Vypíšte hráčov, ktorý neodohrali žiadnu sezónu.

```sql
SELECT firstname, lastname FROM players JOIN player_statistics ON players.id = player_statistics.player_id WHERE player_statistics.id IS NULL
```

11. Vypíšte mena hráčov s počtom bodov, gólov, asistencii, vypočítajte štatistiku bod na
zápas (počet bodov / počet zápasov), +/- body a to všetko pre sezónu „2019/2020“.
Výsledok zoraďte podľa počtu bodov zostupne a v prípade zhody použite druhy
parameter počet gólov.

```sql
SELECT firstname, lastname, name, goals, assists, games, goals + assists AS points, (goals + assists) / games as points_per_game, seasons.name FROM player_statistics INNER JOIN seasons ON player_statistics.season_id = seasons.id INNER JOIN players ON player_statistics.player_id = players.id WHERE seasons.name = '2019-2020' ORDER BY points_per_game DESC
```

12. Vypíšte všetkých hráčov, ktorý hrali za klub, ktorý nesie v názve „Arizona“. Vo výsledku
uveďte meno hráča, počet bodov a sezónu v ktorej hral za daný klub. Výsledok zoraďte
podľa názvu sezóny.

```sql
SELECT player_id, players.firstname, players.lastname, teams.name FROM player_statistics JOIN teams ON teams.id = team_id JOIN players on players.id = player_id
WHERE teams.name LIKE '%Arizona%'
```

13. Vytvorte nového hráča s menom „Peter Forsberg“ s dátumom narodenia 20 Júla 1973
a id . Pre daného hráča vytvorte štatistiku pre sezónu 2000/2001 so štatistikami:
• Počet zápasov 73, gólov 27, asistencii 62, +/- 0, trestných minút 54. Danú
sezónu odohral za klub Colorado Avalanche. V prípade, že v DB chýba nejaký
parameter, tak je ho potrebné doplniť do správnej tabuľky

```sql
```

14. Aktualizujte štatistiku +/- pre Petra Forsberga na hodnotu 23.

```sql
```

15. Vymažte hráča Petra Forsberga z DB


```sql
```