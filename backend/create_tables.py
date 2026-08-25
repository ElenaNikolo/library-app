"""Δημιουργεί τους πίνακες στη βάση. Τρέχει μία φορά, πριν το seed."""

from app.database import Base, engine

# Τα models πρέπει να γίνουν import για να καταχωρηθούν στο Base.metadata.
# Χωρίς αυτά η create_all δεν βλέπει τους πίνακες και δεν φτιάχνει τίποτα.
from app.models.author import Author
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.models.category import Category
from app.models.loan import Loan
from app.models.loan_request import LoanRequest
from app.models.member import Member
from app.models.user import User

Base.metadata.create_all(engine)

print("Tables created.")
