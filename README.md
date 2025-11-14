# Skriptomat

## Opis projekta
Trenutno, studenti često koriste različite platforme za dijeljenje bilješki, poput društvenih mreža ili e-mailova, što može biti neučinkovito i kaotično. Ovaj način dijeljenja informacija često rezultira gubitkom vremena i nemogućnošću pronalaska relevantnih materijala kada su najpotrebniji. Zato smo mi smislili rješenje za taj problem! Platforma „Skriptomat“ omogućuje dijeljenje vlastitih materijala među studentima čime se olakšava pristup relevantnim i ažurnim materijalima s predavanja. Studenti će imati brži i lakši pristup relevantnim materijalima za učenje te time uštedjeti vrijeme koje bi inače posvetili prikupljanju svih materijala potrebnih za učenje. Nadalje, poboljšat će se i kvaliteta bilješki sustavom ocjenjivanja koji omogućuje jednostavno identificiranje najkvalitetnijih materijala za učenje. Također, aplikacija potiče suradnju među studentima zato što međusobnom pomoći dolazi do boljeg razumijevanja gradiva, odnosno većeg akademskog uspjeha. 

Ovaj projekt je rezultat timskog rada u sklopu projektnog zadatka kolegija Programsko inženjerstvo na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu.

## Funkcijski zahtjevi
| ID zahtjeva | Opis                                                                                          | Prioritet | Izvor                     | Kriteriji prihvaćanja                                                                                         |
|-------------|-----------------------------------------------------------------------------------------------|-----------|---------------------------|---------------------------------------------------------------------------------------------------------------|
| F-001       | Sustav omogućuje registraciju korisnika kao moderatora ili regularnih korisnika.                          | Visok     | Zahtjev dionika          | Korisnici se na platformu mogu registrirati e-mail adresom i lozinkom korištenjem vanjskih servisa za autentifikaciju. Uz vlastite podatke, korisnici moraju odabrati i ulogu: moderatori ili regularni korisnici.                    |
| F-002       | Sustav omogućuje prijavu korisnika.                                           | Visok   | Zahtjev dionika          | Registrirani korisnici se kasnije mogu prijaviti na svoj račun koristeći podatke kojima su se registrirali.|
| F-003       | Sustav omogućuje regularnim korisnicima objavljivanje materijala.                              | Visok     | Zahtjev dionika          | Korisnik može objaviti svoju skriptu. Svaki materijal mora sadržavati osnovne podatke: godinu nastanka, naziv kolegija i naslov.       |
| F-004       | Sustav omogućuje regularnim korisnicima recenziranje i ocjenjivanje materijala.          | Visok     | Zahtjev dionika         | Korisnik može uz svaki objavljeni materijal ostaviti povratnu informaciju u obliku ocjene „upvote“ ili „downvote“ i komentara.   |
| F-005       | Sustav omogućuje moderatorima provjeru validnosti objavljenih materijala.                      | Visok     | Zahtjev dionika | Moderatori mogu pregledati nove materijale i određivati njihovu točnost i prikladnost te imaju mogućnost označiti sadržaj kao neprimjeren ili odobriti objavu. Oni pregledavaju sadržaj prije objavljivanja. 
| F-006       | Sustav omogućuje regularnim korisnicima slanje donacija.                      | Visok     | Zahtjev dionika | Svaki korisnik može za bilo koju skriptu poslati donaciju pisatelju skripte u obliku ,,Buy me a coffee" inicijative.  
| F-007       | Sustav ima postojeće rješenje za web chat pomoću kojeg korisnici razgovaraju.                      | Visok     | Zahtjev dionika | Unutar aplikacije integrirano je postojeće rješenje za web chat pomoću kojeg studenti mogu razgovarati međusobno ili kontaktirati moderatore.
| F-008       | Sustav omogućuje administratorima odobravanje novih moderatora, upozoravanje i uklanjanje korisnika.                | Visok     | Zahtjev dionika | U sustavu postoje administratori koji upravljaju korisnicima, odobravaju nove moderatore.
| F-009       | Sustav omogućuje administratorima uklanjanje i uređivanje objava.                | Visok     | Zahtjev dionika | Administratori nadgledaju rad sustava.
| F-010       | Sustav omogućuje objavu materijala u pdf formatu.                | Visok     | Zahtjev dionika | Materijali se objavljuju u pdf formatu.
| F-011       | Sustav omogućuje dobivanje obavijesti za aktivnosti na platformi.                | Visok     | Zahtjev dionika | Kada moderator potvrdi skriptu, korisniku koji je objavio skriptu dolazi potvrda/obavijest o prihvaćanju skripte.


## Tehnologije
- Backend: Python, Django, Django REST Framework
- Frontend: React Vite
- Database: PostgreSQL (pgAdmin4 for management)
- Dijagrami: Astah

## Članovi tima
- Leonarda Laušić - voditeljica (dokumentacija)
- Dunja Međurečan (frontend, backend)
- Lorena Pratljačić (baza podataka)
- Daniela Jovanović
- Jakov Miličić
- Mihael Smud


## Licenca
Ovaj repozitorij sadrži otvoreni obrazovni sadržaji (eng. Open Educational Resources) i licenciran je prema pravilima Creative Commons licencije koja omogućava da preuzmete djelo, podijelite ga s drugima uz uvjet da navođenja autora, ne upotrebljavate ga u komercijalne svrhe te dijelite pod istim uvjetima [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License HR](https://creativecommons.org/licenses/by-nc/4.0/deed.hr). 
