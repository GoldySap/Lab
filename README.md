# lab

VG2 IT – Check-off Lab prosjekt  
Flask-webapp med MariaDB-database, kjørt på Raspberry Pi.

---

## Teknologier

| Teknologi | Hva den gjør |
|-----------|-------------|
| Python / Flask | Webserver og routing |
| MariaDB | Relasjonsdatabase |
| Jinja2 | HTML-templates |
| Waitress | Produksjonsserver |
| Git / GitHub | Versjonskontroll |

---

## Kom i gang

### 1. Klon prosjektet

```bash
git clone https://github.com/DITT-BRUKERNAVN/lab.git
cd lab
```

### 2. Lag og aktiver virtuelt miljø

```bash
python -m venv venv
source venv/bin/activate        # Linux / Raspberry Pi
# venv\Scripts\activate         # Windows
```

### 3. Installer pakker

```bash
pip install -r requirements.txt
```

### 4. Sett opp databasen

Logg inn i MariaDB og kjør:

```sql
CREATE DATABASE lab_db;
CREATE USER 'lab_user'@'%' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON lab_db.* TO 'lab_user'@'%';
FLUSH PRIVILEGES;

USE lab_db;

CREATE TABLE brukere (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    navn  VARCHAR(100) NOT NULL,
    epost VARCHAR(150) NOT NULL
);
```

### 5. Oppdater tilkoblings­informasjon

Rediger `app.py` og bytt ut `ditt_passord` med det faktiske passordet du satte i steg 4.

### 6. Start appen

**Utvikling** (debug-modus):
```bash
python app.py
```

**Produksjon** med Waitress:
```bash
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

Åpne nettleseren på en annen maskin og gå til:
```
http://<raspberry-pi-ip>:5000
```

---

## Prosjektstruktur

```
lab/
├── app.py                  # Flask-applikasjonen
├── requirements.txt        # Python-pakker
├── README.md               # Denne filen
└── templates/
    ├── index.html          # Forside – viser alle brukere
    ├── bruker.html         # Velkomstside for én bruker (/bruker/<navn>)
    └── legg_til.html       # Skjema for å legge til bruker
```

---

## Routes

| URL | Metode | Beskrivelse |
|-----|--------|-------------|
| `/` | GET | Forside – lister alle brukere fra databasen |
| `/bruker/<navn>` | GET | Velkomstside for én navngitt bruker |
| `/legg-til` | GET | Vis skjema for å legge til ny bruker |
| `/legg-til` | POST | Lagre ny bruker fra skjema til databasen |

---

## Fagbegreper forklart

**SSH** – Secure Shell. Kryptert protokoll for å logge inn på en maskin over nettverket (port 22).

**Statisk vs. dynamisk IP** – Statisk IP endrer seg aldri; dynamisk IP tildeles automatisk av DHCP og kan endre seg.

**Port** – Et logisk endepunkt for nettverkskommunikasjon. Port 22 = SSH, port 5000 = Flask (utvikling), port 80 = HTTP, port 443 = HTTPS, port 8080 = alternativ HTTP.

**UFW** – Uncomplicated Firewall. Brukes til å åpne/lukke porter på Linux, f.eks. `sudo ufw allow 5000`.

**Service / tjeneste** – Et program som kjører i bakgrunnen på Linux, f.eks. MariaDB. Sjekkes med `sudo systemctl status mariadb`.

**GET vs. POST** – GET henter data (synlig i URL). POST sender data (f.eks. skjemadata) i forespørselskroppen – tryggere for passord og sensitiv info.

**commit()** – Lagrer databaseendringer permanent. Uten `commit()` blir ikke INSERT/UPDATE/DELETE skrevet til disken.

**Jinja2** – Templatemotor i Flask. Lar deg sette inn Python-variabler (`{{ variabel }}`), løkker (`{% for %}`), og if-setninger (`{% if %}`) direkte i HTML.

**Waitress** – En produksjonsklar WSGI-server for Python. Erstatter Flasks innebygde debug-server når appen skal kjøre stabilt.

**venv** – Virtuelt Python-miljø. Isolerer prosjektets pakker fra resten av systemet.

**requirements.txt** – Liste over alle pakker og versjoner prosjektet trenger. Lages med `pip freeze > requirements.txt`.

---

## Sikkerhet

- Passord og sensitiv konfigurasjon bør ligge i miljøvariabler, ikke hardkodet i `app.py`.
- Bruk parameteriserte SQL-spørringer (`?`-plassholdere) for å unngå SQL-injeksjon.
- Åpne kun nødvendige porter i UFW.
- Ikke kjør Flask i `debug=True` i produksjon.

---

## Mulige forbedringer

- Legg til brukerautentisering (innlogging med passord).
- Legg til sletting og redigering av brukere (DELETE / UPDATE).
- HTTPS med SSL-sertifikat via Nginx som reverse proxy.
- Legg til roller og tilgangs verifisering.
