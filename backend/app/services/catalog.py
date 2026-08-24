from sqlalchemy.orm import Session

from app.models.author import Author
from app.models.book import Book
from app.models.book_copy import CopyStatus
from app.models.category import Category
from app.repositories.catalog import (
    AuthorRepository,
    BookCopyRepository,
    BookRepository,
    CategoryRepository,
)
from app.repositories.loans import LoanRepository
from app.schemas.catalog import AuthorCreate, BookCreate


class BookAlreadyExistsError(Exception):
    pass


class BookHasLoansError(Exception):
    pass


class InvalidBookDataError(Exception):
    pass


def list_categories(db: Session) -> list[Category]:
    return CategoryRepository(db).get_all()


def list_authors(db: Session) -> list[Author]:
    return AuthorRepository(db).get_all()


def search_books(db: Session, title: str | None, category_id: int | None) -> list[Book]:
    return BookRepository(db).search(title, category_id)


def get_book(db: Session, book_id: int) -> Book | None:
    return BookRepository(db).get_by_id(book_id)


def count_copies(db: Session, book_id: int) -> tuple[int, int]:
    copies = BookCopyRepository(db).get_by_book(book_id)
    available = sum(1 for copy in copies if copy.status == CopyStatus.AVAILABLE)
    return len(copies), available


def create_author(db: Session, data: AuthorCreate) -> Author:
    author = Author(first_name=data.first_name, last_name=data.last_name)
    AuthorRepository(db).add(author)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return author


def create_book(db: Session, data: BookCreate) -> Book:
    books = BookRepository(db)

    if books.get_by_isbn(data.isbn):
        raise BookAlreadyExistsError("Υπάρχει ήδη βιβλίο με αυτό το ISBN.")

    if CategoryRepository(db).get_by_id(data.category_id) is None:
        raise InvalidBookDataError("Η κατηγορία δεν υπάρχει.")

    authors = AuthorRepository(db).get_by_ids(data.author_ids)
    if len(authors) != len(data.author_ids):
        raise InvalidBookDataError("Κάποιος συγγραφέας δεν υπάρχει ή δηλώθηκε δύο φορές.")

    book = Book(
        isbn=data.isbn,
        title=data.title,
        publisher=data.publisher,
        publication_year=data.publication_year,
        description=data.description,
        category_id=data.category_id,
        authors=authors,
    )
    books.add(book)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return book


def update_book(db: Session, book: Book, data: BookCreate) -> Book:
    existing = BookRepository(db).get_by_isbn(data.isbn)
    if existing and existing.id != book.id:
        raise BookAlreadyExistsError("Υπάρχει ήδη βιβλίο με αυτό το ISBN.")

    if CategoryRepository(db).get_by_id(data.category_id) is None:
        raise InvalidBookDataError("Η κατηγορία δεν υπάρχει.")

    authors = AuthorRepository(db).get_by_ids(data.author_ids)
    if len(authors) != len(data.author_ids):
        raise InvalidBookDataError("Κάποιος συγγραφέας δεν υπάρχει ή δηλώθηκε δύο φορές.")

    book.isbn = data.isbn
    book.title = data.title
    book.publisher = data.publisher
    book.publication_year = data.publication_year
    book.description = data.description
    book.category_id = data.category_id
    book.authors = authors

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return book


def delete_book(db: Session, book: Book) -> None:
    if LoanRepository(db).get_by_book(book.id):
        raise BookHasLoansError("Το βιβλίο έχει ιστορικό δανεισμών και δεν διαγράφεται.")

    BookRepository(db).delete(book)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
