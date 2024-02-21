# Dátové modelovanie #1 – Kardinality

Oddelenie zamestnáva osoby. Osoba je zamestnaná najviac v jednom oddelení.
```mermaid
classDiagram
    Oddelenie "01" <-- "1*" Osoba
```


Manažér riadi najviac jedno oddelenie. Oddelenie je riadené najviac jedným manažérom.
```mermaid
classDiagram
    Oddelenie "01" <-- "01" Manazer
```


Autor môže napísať veľa článkov. Veľa článkov môže byť napísaných viacerými autormi. Autor článku môže byť neznámy.
```mermaid
classDiagram
    Clanok "0n" <-- "0n" Autor
```


Tím je zložený z viacerých hráčov. Hráč hrá iba za jeden tím. Osoba, ktorá nehrá za tím nie je hráč.
```mermaid
classDiagram
    Tim "1" <-- "1n" Hrac
```


Produkt patrí do viacerých kategórií. Kategória obsahuje veľa produktov. Produkt nemôže existovať bez kategórie.
```mermaid
classDiagram
    Kategoria "1n" <-- "0n" Produkt
```


Konkrétny produkt sa predáva v najviac jednej krajine. V krajine sa predáva veľa produktov.
```mermaid
classDiagram
    Krajina "01" <-- "0n" Produkt
```

# Dátové modelovanie #2 - Kardinality

V nasledovných diagramoch vysvetlite kardinalitu vzťahov medzi entitami. Určte, ktorý z týchto vzťahov je typu 1:1 a vysvetlite, prečo je vždy potrebné zvážiť vhodnosť použitia takéhoto typu vzťahu. Vysvetlite, akým typom vzťahu by ho bolo vhodné v tomto prípade nahradiť, a prečo

Areal strazi 0 az n straznikov, straznik strazi aspon 1 areal.

Policajt ma 0 alebo 1 zbraj, jednu zbran vlastni 0 az 1 majitelov.

Lekar je lekarom 1 az n pacientov, pacient ma 1 lekara.

Policajt zbran je 1:1. => vzdy treba zvazit preco to nemat ako 1 object.

# Dátové modelovanie #3 - e-shop

```mermaid
classDiagram
    Zakaznik "1"-- "0n" Objednavka
    Objednavka "1" -- "01" Faktura
    Platba "01" -- "1" Faktura
    Objednavka "0n"-- "1n" Polozka
    Polozka "0n" -- "1" Produkt
```

# Dátové modelovanie #4 - Štúdium

```mermaid
classDiagram
    Ustav "1n" -- "1" Fakulta
    Ustav "1" -- "1n" StudijnyProgram
    Kurz "1n" -- "1" StudijnyProgram
    Kurz "1n" -- "1n" Ucitel
    Ustav "1" -- "1n" Ucitel
```

# Dátové modelovanie #5 - Provider

```mermaid
classDiagram
    Adresa "1n"--"1" Zakaznik
    Zakaznik "1"-- "1n" Poziadavka
    Poziadavka "1"--"1n" PolozkaPoziadavky
    PolozkaPoziadavky "0n"--"1" Sluzba 
    Poskytovatel "1" --"0n" Sluzba
    PodmienkyPouzitiia "1"--"1n" Sluzba
```

# Dátové modelovanie #6 - Farmaceutická firma

```mermaid
classDiagram 
    Predajna "1"--"0n" Objednavka
    Objednavka "0n"--"01" ObchodnyReprezentant
    Objednavka "1"--"1n" PolozkaObejdnavky
    PolozkaObejdnavky "0n"--"1" Produkt
```

# Dátové modelovanie #7 - Autobusový dopravca


```mermaid
classDiagram
    Dopravca "1"--"0n" Autobus
    Autobus "1n"--"1" Trasa
    Trasa "1n"--"1n" Usek
    Usek "1n"--"1n" Mesto
    Sofer "1n"--"1n" Usek
    Garaz "1"--"1n" Mesto
```

# Dátové modelovanie #8 - Publikácie

```mermaid
classDiagram
    Vydavatelstvo "1"--"1n" Publikacia
    Publikacia "1n"--"1" Autor
    Publikacia "1n"--"1" Editor
    Publikacia "1n"--"1" Recenzent
    Autor "1n"--"1" Tema
    Editor "1"--"1n" Tema
```

# Dátové modelovanie #9 - Nemocnica

```mermaid
classDiagram
    Nemocnica "1" -- "1n" Oddelenie
    Pacient "1" -- "1n" Evidencia
    Oddelenie "1" -- "1n" Evidencia
    Evidencia "0n" -- "1" VseobecnyLekar
    Evidencia "0n" -- "1" Konzultant
    Evidencia "0n" -- "0n" DalsiLekar
    Evidencia "1" -- "1n" Test
```

# Dátové modelovanie #10 - Centrum voľného času


```mermaid
classDiagram
    Kruzok "1" -- "1n" KruzokTurnus
    Dieta "1n" -- "1n" KruzokTurnus
    KruzokTurnus "1n" -- "1n" Instruktor
    Kruzok "0n" -- "0n" Instruktor
    Miestnost "1n" -- "1n" KruzokTurnus
```