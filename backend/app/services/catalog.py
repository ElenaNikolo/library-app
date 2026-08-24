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
