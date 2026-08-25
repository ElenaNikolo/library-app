"""Γεμίζει τη βάση με αρχικά δεδομένα. Τρέχει μετά το create_tables.py."""

from datetime import date, timedelta

from sqlalchemy import select

from app.database import SessionLocal
from app.models.author import Author
from app.models.book import Book
from app.models.book_copy import BookCopy, CopyStatus
from app.models.category import Category
from app.models.loan import LOAN_PERIOD_DAYS, Loan, LoanStatus
from app.models.member import Member
from app.models.user import User, UserRole
from app.security import hash_password

session = SessionLocal()

# Αν η βάση έχει ήδη δεδομένα, σταματάμε εδώ. Αλλιώς η δεύτερη εκτέλεση
# θα έσκαγε με σφάλμα διπλού ISBN.
if session.scalars(select(Category)).first():
    print("Database already has data. Nothing to do.")
    session.close()
    raise SystemExit

today = date.today()

# --- Κατηγορίες ---

fantasy = Category(name="Φαντασία", description="Έργα φαντασίας και μυθοπλασίας.")
children = Category(name="Παιδική & Νεανική", description="Βιβλία για παιδιά και εφήβους.")
science_fiction = Category(name="Επιστημονική Φαντασία", description="Επιστημονική φαντασία.")
classics = Category(name="Κλασική Λογοτεχνία", description="Κλασικά έργα της παγκόσμιας λογοτεχνίας.")
computing = Category(name="Πληροφορική", description="Βιβλία προγραμματισμού και πληροφορικής.")

categories = [fantasy, children, science_fiction, classics, computing]

# --- Βιβλία ---
# Οι συγγραφείς γράφονται μέσα σε κάθε βιβλίο. Κανένας δεν εμφανίζεται σε
# δεύτερο βιβλίο, οπότε δεν δημιουργούνται διπλοεγγραφές.

fellowship = Book(
    isbn="9780007269709",
    title="The Fellowship of the Ring",
    publisher="HarperCollins",
    publication_year=2008,
    description="Ο πρώτος τόμος του Άρχοντα των Δαχτυλιδιών.",
    category=fantasy,
    authors=[Author(first_name="J.R.R.", last_name="Tolkien")],
)

circe = Book(
    isbn="9781526612519",
    title="Circe",
    publisher="Bloomsbury",
    publication_year=2019,
    description="Η ιστορία της μάγισσας Κίρκης από τη δική της οπτική.",
    category=fantasy,
    authors=[Author(first_name="Madeline", last_name="Miller")],
)

piranesi = Book(
    isbn="9781526622419",
    title="Piranesi",
    publisher="Bloomsbury",
    publication_year=2020,
    description="Ένας άνθρωπος ζει μόνος σε ένα ατέλειωτο σπίτι με αίθουσες και αγάλματα.",
    category=fantasy,
    authors=[Author(first_name="Susanna", last_name="Clarke")],
)

harry_potter = Book(
    isbn="9781408855652",
    title="Harry Potter and the Philosopher's Stone",
    publisher="Bloomsbury",
    publication_year=2014,
    description="Ο Χάρι Πότερ ανακαλύπτει ότι είναι μάγος και πηγαίνει στο Χόγκουαρτς.",
    category=children,
    authors=[Author(first_name="J.K.", last_name="Rowling")],
)

wonder = Book(
    isbn="9780552778626",
    title="Wonder",
    publisher="Black Swan",
    publication_year=2013,
    description="Ένα αγόρι με παραμόρφωση στο πρόσωπο πηγαίνει για πρώτη φορά σχολείο.",
    category=children,
    authors=[Author(first_name="R.J.", last_name="Palacio")],
)

impossible_creatures = Book(
    isbn="9781408897409",
    title="Impossible Creatures",
    publisher="Bloomsbury",
    publication_year=2023,
    description="Δύο παιδιά ταξιδεύουν σε έναν κόσμο όπου ζουν μυθικά πλάσματα.",
    category=children,
    authors=[Author(first_name="Katherine", last_name="Rundell")],
)

nineteen_eighty_four = Book(
    isbn="9780141036144",
    title="Nineteen Eighty-Four",
    publisher="Penguin Books",
    publication_year=2008,
    description="Δυστοπία σε ένα καθεστώς ολοκληρωτικής παρακολούθησης.",
    category=science_fiction,
    authors=[Author(first_name="George", last_name="Orwell")],
)

dune = Book(
    isbn="9781529347852",
    title="Dune",
    publisher="Hodder & Stoughton",
    publication_year=2020,
    description="Η πάλη για τον έλεγχο του πλανήτη Αρράκις και του μπαχαρικού.",
    category=science_fiction,
    authors=[Author(first_name="Frank", last_name="Herbert")],
)

project_hail_mary = Book(
    isbn="9781529100617",
    title="Project Hail Mary",
    publisher="Del Rey",
    publication_year=2021,
    description="Ένας αστροναύτης ξυπνά μόνος του σε διαστημόπλοιο χωρίς μνήμη.",
    category=science_fiction,
    authors=[Author(first_name="Andy", last_name="Weir")],
)

pride_and_prejudice = Book(
    isbn="9780525505136",
    title="Pride and Prejudice",
    publisher="Penguin Books",
    publication_year=2009,
    description="Η Ελίζαμπεθ Μπένετ και ο κύριος Ντάρσι στην Αγγλία του 19ου αιώνα.",
    category=classics,
    authors=[Author(first_name="Jane", last_name="Austen")],
)

great_gatsby = Book(
    isbn="9781847493354",
    title="The Great Gatsby",
    publisher="Alma Classics",
    publication_year=2012,
    description="Ο Τζέι Γκάτσμπι και η Αμερική της δεκαετίας του 1920.",
    category=classics,
    authors=[Author(first_name="F. Scott", last_name="Fitzgerald")],
)

zorba = Book(
    isbn="9781476782812",
    title="Zorba the Greek",
    publisher="Simon & Schuster",
    publication_year=2014,
    description="Η γνωριμία ενός διανοούμενου με τον Αλέξη Ζορμπά στην Κρήτη.",
    category=classics,
    authors=[Author(first_name="Nikos", last_name="Kazantzakis")],
)

design_patterns = Book(
    isbn="9780201633610",
    title="Design Patterns",
    publisher="Addison-Wesley",
    publication_year=1995,
    description="Τα 23 σχεδιαστικά πρότυπα του αντικειμενοστρεφούς προγραμματισμού.",
    category=computing,
    authors=[
        Author(first_name="Erich", last_name="Gamma"),
        Author(first_name="Richard", last_name="Helm"),
        Author(first_name="Ralph", last_name="Johnson"),
        Author(first_name="John", last_name="Vlissides"),
    ],
)

pragmatic_programmer = Book(
    isbn="9780135957059",
    title="The Pragmatic Programmer",
    publisher="Addison-Wesley",
    publication_year=2019,
    description="Πρακτικές συμβουλές για την καθημερινή δουλειά του προγραμματιστή.",
    category=computing,
    authors=[
        Author(first_name="Andrew", last_name="Hunt"),
        Author(first_name="David", last_name="Thomas"),
    ],
)

introduction_to_algorithms = Book(
    isbn="9780262046305",
    title="Introduction to Algorithms",
    publisher="MIT Press",
    publication_year=2022,
    description="Το βασικό πανεπιστημιακό εγχειρίδιο για αλγορίθμους και δομές δεδομένων.",
    category=computing,
    authors=[
        Author(first_name="Thomas H.", last_name="Cormen"),
        Author(first_name="Charles E.", last_name="Leiserson"),
        Author(first_name="Ronald L.", last_name="Rivest"),
        Author(first_name="Clifford", last_name="Stein"),
    ],
)

books = [
    fellowship,
    circe,
    piranesi,
    harry_potter,
    wonder,
    impossible_creatures,
    nineteen_eighty_four,
    dune,
    project_hail_mary,
    pride_and_prejudice,
    great_gatsby,
    zorba,
    design_patterns,
    pragmatic_programmer,
    introduction_to_algorithms,
]

# --- Αντίτυπα ---

copies_per_book = [
    (fellowship, 3),
    (circe, 3),
    (piranesi, 3),
    (harry_potter, 4),
    (wonder, 4),
    (impossible_creatures, 3),
    (nineteen_eighty_four, 3),
    (dune, 4),
    (project_hail_mary, 3),
    (pride_and_prejudice, 2),
    (great_gatsby, 2),
    (zorba, 2),
    (design_patterns, 2),
    (pragmatic_programmer, 2),
    (introduction_to_algorithms, 2),
]

# Ο κωδικός κάθε αντιτύπου είναι το ISBN του βιβλίου και ένας αύξων αριθμός.
# Τα κρατάμε σε λεξικό για να βρίσκουμε εύκολα αυτά που θα δανειστούν.
copies = {}
for book, how_many in copies_per_book:
    for number in range(1, how_many + 1):
        code = f"{book.isbn}-{number}"
        copies[code] = BookCopy(copy_code=code, book=book)

circe_copy = copies[f"{circe.isbn}-1"]
dune_copy = copies[f"{dune.isbn}-1"]
orwell_copy = copies[f"{nineteen_eighty_four.isbn}-1"]

# Τα αντίτυπα των ενεργών δανεισμών δεν είναι διαθέσιμα. Το αντίτυπο του
# επιστραμμένου δανεισμού μένει AVAILABLE, όπως και όλα τα υπόλοιπα.
circe_copy.status = CopyStatus.ON_LOAN
dune_copy.status = CopyStatus.ON_LOAN
copies[f"{harry_potter.isbn}-4"].status = CopyStatus.LOST

# --- Χρήστες ---
# Κοινός κωδικός για όλους τους δοκιμαστικούς λογαριασμούς.
DEMO_PASSWORD = "Library2026!"

admin = User(
    username="admin",
    email="admin@library.gr",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.ADMIN,
)
librarian = User(
    username="librarian",
    email="librarian@library.gr",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.LIBRARIAN,
)
maria = User(
    username="maria",
    email="maria@example.com",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.MEMBER,
)
giorgos = User(
    username="giorgos",
    email="giorgos@example.com",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.MEMBER,
)
eleni = User(
    username="eleni",
    email="eleni@example.com",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.MEMBER,
)
nikos = User(
    username="nikos",
    email="nikos@example.com",
    password_hash=hash_password(DEMO_PASSWORD),
    role=UserRole.MEMBER,
)

users = [admin, librarian, maria, giorgos, eleni, nikos]

# --- Μέλη ---
# Ο admin και ο librarian δεν έχουν προφίλ μέλους.
# Οι ημερομηνίες εγγραφής είναι παλαιότερες από τους δανεισμούς.

maria_member = Member(
    user=maria,
    first_name="Μαρία",
    last_name="Παπαδοπούλου",
    phone="2101234567",
    address="Ερμού 15, Αθήνα",
    membership_date=today - timedelta(days=200),
)
giorgos_member = Member(
    user=giorgos,
    first_name="Γιώργος",
    last_name="Δημητρίου",
    phone="2109876543",
    address="Πατησίων 88, Αθήνα",
    membership_date=today - timedelta(days=150),
)
eleni_member = Member(
    user=eleni,
    first_name="Ελένη",
    last_name="Κωνσταντίνου",
    phone="2310445566",
    address="Τσιμισκή 42, Θεσσαλονίκη",
    membership_date=today - timedelta(days=120),
)
nikos_member = Member(
    user=nikos,
    first_name="Νίκος",
    last_name="Αντωνίου",
    phone="2610334455",
    address="Κορίνθου 210, Πάτρα",
    membership_date=today - timedelta(days=40),
)

members = [maria_member, giorgos_member, eleni_member, nikos_member]

# --- Δανεισμοί ---

maria_loan_date = today - timedelta(days=3)
giorgos_loan_date = today - timedelta(days=20)
eleni_loan_date = today - timedelta(days=30)

active_loan = Loan(
    member=maria_member,
    book_copy=circe_copy,
    loan_date=maria_loan_date,
    due_date=maria_loan_date + timedelta(days=LOAN_PERIOD_DAYS),
)

overdue_loan = Loan(
    member=giorgos_member,
    book_copy=dune_copy,
    loan_date=giorgos_loan_date,
    due_date=giorgos_loan_date + timedelta(days=LOAN_PERIOD_DAYS),
)

returned_loan = Loan(
    member=eleni_member,
    book_copy=orwell_copy,
    loan_date=eleni_loan_date,
    due_date=eleni_loan_date + timedelta(days=LOAN_PERIOD_DAYS),
    return_date=today - timedelta(days=10),
    status=LoanStatus.RETURNED,
)

# Το πρόστιμο το υπολογίζει το ίδιο το Loan, δεν το ξαναγράφουμε εδώ.
returned_loan.fine_amount = returned_loan.calculate_fine()

loans = [active_loan, overdue_loan, returned_loan]

# --- Αποθήκευση ---
# Οι συγγραφείς αποθηκεύονται μαζί με τα βιβλία μέσω της σχέσης authors.

session.add_all(categories)
session.add_all(books)
session.add_all(copies.values())
session.add_all(users)
session.add_all(members)
session.add_all(loans)

session.commit()
session.close()

print(
    f"Seed completed: {len(books)} books, {len(copies)} copies, "
    f"{len(users)} users, {len(members)} members, {len(loans)} loans."
)
