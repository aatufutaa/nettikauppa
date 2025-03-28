# Nettikauppa
Nettikauppa web-sovellus, jossa käyttäjät voivat jättää omia ilmoituksia ja keskustella niistä.

## Sovelluksen toiminnot
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan, poistamaan ja tarkastelemaan myynti-ilmoituksia, jotka voivat sisältää kuvia ja tekstiä.
- Käyttäjä pystyy etsimään ilmoituksia hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja, kuten myynti-ilmoitusten määrän ja käyttäjän lisäämät ilmoitukset.
- Käyttäjä pystyy valitsemaan myynti-ilmoitukselle luokittelut, kuten osasto (autot, elektroniikka, vaatteet, huonekalut, lelut) ja tavaran kunto (erinomainen, hyvä, kohtalainen, huono).
- Käyttäjä pystyy keskustelemaan myytävinä olevista tuotteista myynti-ilmoitusten alla.

## Sovelluksen tilanne tällä hetkellä
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen sekä lisäämään, muokkaamaan, poistamaan ja tarkastelemaan myynti-ilmoituksia. Käyttäjä pystyy myös valitsemaan luokittelun, mikä ei vielä ole tietokannassa. Lisäksi käyttäjä pystyy etsimään ilmoituksia hakusanalla. Sovelluksessa on myös alustava käyttäjä sivu. Sovelluksesta puuttuu keskustelu alue myytävistä olevista tuotteista.

## Sovelluksen asennus
Asenna flask -kirjasto
```
pip install flask
```
Luo tietokantaan taulut
```
sqlite3 database.db < schema.sql
```
Käynnistä sovellus
```
flask run
```