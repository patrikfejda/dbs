1. Napíšte SELECT, ktorý vráti priemerný počet dní (zaokrlúhené na celé čísla), ktoré sú
všetci programátori registrovaní v našej databáze.

```sql
SELECT p.name, ROUND((EXTRACT(epoch FROM NOW()) - EXTRACT(epoch FROM p.signed_in_at))/60/60/24) as delay

FROM programmers as p

```

2. Napíšte SELECT, ktorý vráti celkový počet dní, ktoré sú ruby programátori registrovaní v našej
databáze.

```sql
SELECT p.name, ROUND((EXTRACT(epoch FROM NOW()) - EXTRACT(epoch FROM p.signed_in_at))/60/60/24) as delay

FROM programmers as p

JOIN projects_programmers AS pp
ON pp.project_id = p.id

JOIN projects as pj
ON pj.id = pp.project_id

JOIN languages as l
ON l.id = pj.language_id

WHERE l.label = 'ruby'
```
3. Napíšte SELECT, ktorý vráti meno projektu a počet programátorov, ktorí na ňom pracujú

```sql
SELECT pro.name, COUNT(pp.programmer_id)

FROM projects as pro

JOIN projects_programmers as pp
ON pp.project_id = pro.id

GROUP BY pro.name
```
4. Napíšte SELECT, ktorý vráti meno projektu a celkový počet dní, ktoré na ňom programátori
odrobili (predpokladajme, že od okamihu kedy sa pridali k projektu už na ňom robia každý
deň).

```sql
SELECT pro.name, SUM(ROUND((EXTRACT(epoch FROM NOW()) - EXTRACT(epoch FROM p.signed_in_at))/60/60/24)) as days

FROM projects as pro

JOIN projects_programmers as pp
ON pp.project_id = pro.id

JOIN programmers as p
ON pp.programmer_id = p.id

GROUP BY pro.name

```
5. Napíšte SELECT, ktorý vráti meno projektu, na ktorom pracuje najviac programátorov. Ak je
takýchto projektov viac, tak uplatnite lexikografické radenie a vypíšte prvý.

```sql
SELECT pro.name, COUNT(pp.programmer_id) as programer_count

FROM projects as pro

JOIN projects_programmers as pp
ON pp.project_id = pro.id

GROUP BY pro.name

ORDER BY programer_count desc, pro.name

LIMIT 1
```
6. Napíšte SELECT, ktorý vráti meno projektu, na ktorom pracuje najviac programátorov. Ak je
takýchto projektov viac, tak vypíšte mená všetkých

```sql
SELECT x.name

FROM (
	
	SELECT pro.name, COUNT(pp.programmer_id) as programer_count
	
	FROM projects as pro
	
	JOIN projects_programmers as pp
	ON pp.project_id = pro.id
	
	GROUP BY pro.name
	
	ORDER BY programer_count desc, pro.name
	
	LIMIT 1
) AS x
```
7. Napíšte SELECT, ktorý vráti meno každého programovacieho jazyka spolu s počtom
programátorov, ktorí ho používajú. Zoradené od najväčšieho po najmenší.

```sql
select x.label, count(x.name) as pro_count

from (
	select distinct l.label, p.name 
	from languages as l
	
	JOIN projects as pro
	on pro.language_id = l.id
	
	JOIN projects_programmers as pp
	on pp.project_id = pro.id
	
	JOIN programmers as p
	on p.id = pp.programmer_id
	
	where p.name IS NOT NULL
) as x

group by x.label

order by pro_count desc
 
```

8. Napíšte SELECT, ktorý vráti meno každého programovacieho jazyka spolu s menom
najstaršieho projektu pre tento programovací jazyk. Tie jazyky, ktoré nemajú žiadny projekt,
nech majú namiesto projektu uvedené 'no project yet'.

```sql
SELECT label, project, age
FROM (
  SELECT x.label, x.project, x.age, ROW_NUMBER() OVER (PARTITION BY x.label ORDER BY x.age DESC) AS row_number
  FROM (
  	select l.label, COALESCE(pro.name, 'no-project-yet') as project, COALESCE(ROUND((EXTRACT(epoch FROM NOW()) - EXTRACT(epoch FROM pro.created_at))/60/60/24),0) as age
	
	from languages as l
	
	JOIN projects as pro
	on pro.language_id = l.id
	
	order by age desc
  
	) as x
) subquery
WHERE row_number = 1;

```
9. Napíšte SELECT, ktorý vráti meno každého programovacieho jazyka spolu s počtom projektov,
v ktorých je jazyk použitý. Zoradené od najväčšieho po najmenší, v prípade rovnakého počtu
projektov nech sú jazyky radené lexikograficky. Skúste v zoradení použiť index stĺpca miesto
jeho názvu.

```sql
select l.label, count(pro.name) as project_count
	
from languages as l

JOIN projects as pro
on pro.language_id = l.id

group by l.label

order by 2 desc
```