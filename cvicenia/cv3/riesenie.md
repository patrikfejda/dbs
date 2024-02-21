1. Napíšte SELECT, ktorý vráti mená a dátumy registrácie všetkých programátorov. 
 
```sql
SELECT name, signed_in_at FROM programmers
```


2. Napíšte SELECT, ktorý vráti mená a dátumy registrácie všetkých programátorov, ktorých mená 
začínajú na písme no R. 

```sql
SELECT name, signed_in_at FROM programmers WHERE name like 'R%'
```
 
3. Napíšte SELECT, ktorý vráti meno a dátum registrácie najnovšieho programátora, ktorého meno 
začína na písmeno R. Hint: limit. 

```sql
SELECT name, signed_in_at FROM programmers WHERE name like 'R%' ORDER BY signed_in_at desc LIMIT 1
```
 
4. Napíšte SELECT, ktorý vráti mená všetkých programátorov, ktorí majú meno kratšie ako 12 
znakov. 

```sql
SELECT name, signed_in_at from programmers where LENGTH(name) < 12
```
 
5. Napíšte SELECT, ktorý vráti mená všetkých programátorov, pričom tí, ktorí majú meno dlhšie 
ako 12 znakov ho budú mať skrátené na 12 znakov.   

```sql
SELECT SUBSTRING(name,1,12), signed_in_at from programmers
```
 
6. Napíšte SELECT, ktorý vráti mená všetkých programátorov vypísané naopak a veľkými 
písmenami. 

```sql
SELECT UPPER(REVERSE(name)) from programmers
```
 
7. Napíšte SELECT, ktorý vráti len prvé slovo z mien všetkých programátorov.   

```sql
TODO OPYTAT SA
```
 
1. Napíšte SELECT, ktorý vráti mená a dátumy registrácie všetkých programátorov, ktorí sa 
zaregistrovali v roku 2016. 

```sql
TODO OPYTAT SA
```
 
1. Napíšte SELECT, ktorý vráti mená a dátumy registrácie všetkých programátorov, ktorí sa 
zaregistrovali vo februári roku 2016. 

```sql
SELECT name, signed_in_at FROM programmers WHERE CAST(signed_in_at as VarChar) like '2016-02%'
```
 
10. Napíšte SELECT, ktorý vráti mená všetkých programátorov a počet dní medzi dátumom ich 
registrácie a prvým aprílom 2016S usporiadaný od najmenšieho po najväčší. 

```sql
TODO OPYTAT SA
```
 
11. Napíšte SELECT, ktorý vráti label všetkých jazykov, ktoré majú aspoň jeden projekt. 

```sql
SELECT languages.label from projects JOIN languages ON projects.language_id = languages.id GROUP BY languages.label
```
 
12. Napíšte SELECT, ktorý vráti label všetkých jazykov, ktoré majú aspoň jeden projekt, ktorý začal 
v roku 2014. 

```sql
SELECT languages.label from projects JOIN languages ON projects.language_id = languages.id WHERE CAST(projects.created_at as VarChar) LIKE '2014%' GROUP BY languages.label
```
 
13. Napíšte SELECT, ktorý vráti mená všetkých projektov, na ktorých sa programuje v jazykoch 
ruby alebo python (Hint: IN). 

```sql
SELECT projects.name, languages.label from projects JOIN languages ON projects.language_id = languages.id WHERE languages.label IN ('python', 'ruby')
```
 
14. Napíšte SELECT, ktorý vráti mená všetkých python programátorov. 

```sql
SELECT programmers.name FROM projects_programmers JOIN projects ON projects_programmers.project_id = projects.id JOIN programmers ON projects_programmers.project_id = projects.id JOIN languages ON projects.language_id = languages.id WHERE languages.label IN ('python') GROUP BY programmers.name
```
 
15. Napíšte SELECT, ktorý vráti mená všetkých python programátorov, ktorí sú vlastníkmi (hoc aj 
nepython) projektu 

TODO toto vrati iba python programatorov, ktory su vlastnikmi python projektov

```sql
SELECT programmers.name, projects.name, projects_programmers.owner, languages.label FROM projects_programmers JOIN projects ON projects_programmers.project_id = projects.id JOIN programmers ON projects_programmers.project_id = projects.id JOIN languages ON projects.language_id = languages.id WHERE languages.label IN ('python') AND projects_programmers.owner IS TRUE
```
