# Βιβλιοθήκη

Εφαρμογή δανεισμού βιβλίων για μια μικρή βιβλιοθήκη. Τελική εργασία για το
Coding Factory 10 του Οικονομικού Πανεπιστημίου Αθηνών.

Το προσωπικό παρακολουθεί τους δανεισμούς, ενώ τα μέλη βλέπουν τον κατάλογο
και τους δικούς τους δανεισμούς.

## Τεχνολογίες

| Μέρος | Τεχνολογίες |
|---|---|
| Backend | Python 3.14, FastAPI, SQLAlchemy 2 |
| Βάση | PostgreSQL 16 σε Docker |
| Authentication | JWT (PyJWT), Argon2 (pwdlib) |
| Frontend | React 19, Vite, React Router |

## Προϋποθέσεις

- Python 3.14 (η έκδοση με την οποία αναπτύχθηκε και επαληθεύτηκε το project)
- Node.js 20.19+ ή 22.12+ (απαίτηση του Vite)
- Docker Desktop

Οι παρακάτω εντολές είναι για Windows με PowerShell.

## Εγκατάσταση και εκτέλεση

### 1. Ρυθμίσεις

Αντίγραψε το `.env.example` σε `.env`:

```
Copy-Item .env.example .env
```

Συμπλήρωσε τα `POSTGRES_USER`, `POSTGRES_PASSWORD` και `POSTGRES_DB` για τη
βάση, καθώς και ένα τυχαίο `SECRET_KEY` για την υπογραφή των JWT.

Το `DATABASE_URL` πρέπει να συμφωνεί με τα ίδια στοιχεία σύνδεσης: τον ίδιο
χρήστη, τον ίδιο κωδικό, την ίδια βάση και την ίδια θύρα. Αν δεν ταιριάζουν,
το backend δεν θα συνδεθεί.

Το `.env` δεν ανεβαίνει στο git.

### 2. Βάση δεδομένων

Από τη ρίζα του project:

```
docker compose up -d
```

Έλεγχος ότι ξεκίνησε:

```
docker compose ps
```

### 3. Backend

Από τον φάκελο `backend`:

```
python -m venv .venv
```

```
.venv\Scripts\activate
```

```
pip install -r requirements.txt
```

Δημιουργία των πινάκων και των αρχικών δεδομένων:

```
python create_tables.py
```

```
python seed.py
```

Και τα δύο μπορούν να ξανατρέξουν χωρίς πρόβλημα. Το `create_tables.py` δεν
πειράζει πίνακες που υπάρχουν ήδη και το `seed.py` σταματάει αν η βάση έχει
δεδομένα.

Εκκίνηση του API:

```
uvicorn app.main:app --reload
```

Το backend ακούει στο `http://127.0.0.1:8000`.

### 4. Frontend

Από τον φάκελο `frontend`:

```
npm install
```

```
npm run dev
```

Άνοιξε το `http://localhost:5173`.

> Κατά την ανάπτυξη το frontend πρέπει να ανοίγει ως `localhost` και όχι ως
> `127.0.0.1`, γιατί το CORS του backend επιτρέπει προς το παρόν μόνο το
> `http://localhost:5173`.

## Δοκιμαστικοί λογαριασμοί

Κωδικός για όλους: `Library2026!`

| Χρήστης | Ρόλος |
|---|---|
| `admin` | ADMIN |
| `librarian` | LIBRARIAN |
| `maria` | MEMBER |
| `giorgos` | MEMBER |
| `eleni` | MEMBER |
| `nikos` | MEMBER |

## Τεκμηρίωση του API

Swagger: `http://127.0.0.1:8000/docs`

Για τα endpoints που χρειάζονται σύνδεση, πάρε token από το
`POST /api/auth/login` και βάλ' το στο κουμπί «Authorize».

## Ρόλοι

Η εφαρμογή υποστηρίζει τρεις ρόλους: MEMBER, LIBRARIAN και ADMIN.

Στο τρέχον frontend:

- ο MEMBER βλέπει τον κατάλογο και τους δικούς του δανεισμούς,
- ο LIBRARIAN και ο ADMIN μπορούν επιπλέον να βλέπουν όλους τους δανεισμούς.

Το backend εφαρμόζει επιπλέον δικαιώματα ανά ρόλο στα αντίστοιχα API endpoints.

Ο κατάλογος είναι ορατός και χωρίς σύνδεση.

## Αρχιτεκτονική

Το backend είναι χωρισμένο σε στρώματα:

```
router  ->  service  ->  repository  ->  model
```

- Οι **routers** χειρίζονται μόνο το HTTP κομμάτι.
- Τα **services** έχουν τους κανόνες του domain και δεν γνωρίζουν HTTP.
- Τα **repositories** είναι το μόνο σημείο που μιλάει στη βάση και δεν κάνουν
  commit· το commit γίνεται στο service.

## Δομή του project

```
backend/
  app/
    models/         οι οντότητες
    repositories/   πρόσβαση στη βάση
    services/       κανόνες του domain
    routers/        endpoints
    schemas/        Pydantic schemas
  create_tables.py
  seed.py
frontend/
  src/
    components/
    pages/
docker-compose.yml
```
