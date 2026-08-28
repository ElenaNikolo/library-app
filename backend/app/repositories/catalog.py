from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.author import Author
from app.models.book import Book
from app.models.book_copy import BookCopy, CopyStatus
from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        return list(self.db.scalars(select(Category).order_by(Category.name)))

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.scalars(select(Category).where(Category.name == name)).first()

    def add(self, category: Category) -> Category:
        self.db.add(category)
        return category


class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Author]:
        return list(
            self.db.scalars(select(Author).order_by(Author.first_name, Author.last_name))
        )

    def get_by_ids(self, author_ids: list[int]) -> list[Author]:
        return list(self.db.scalars(select(Author).where(Author.id.in_(author_ids))))

    def add(self, author: Author) -> Author:
        self.db.add(author)
        return author


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(self, title: str | None = None, category_id: int | None = None) -> list[Book]:
        query = select(Book)

        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if category_id:
            query = query.where(Book.category_id == category_id)

        return list(self.db.scalars(query.order_by(Book.title)))

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.db.scalars(select(Book).where(Book.isbn == isbn)).first()

    def add(self, book: Book) -> Book:
        self.db.add(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)


class BookCopyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, copy_id: int) -> BookCopy | None:
        return self.db.get(BookCopy, copy_id)

    def get_by_book(self, book_id: int) -> list[BookCopy]:
        return list(
            self.db.scalars(
                select(BookCopy)
                .where(BookCopy.book_id == book_id)
                .order_by(BookCopy.copy_code)
            )
        )

    def get_by_code(self, copy_code: str) -> BookCopy | None:
        return self.db.scalars(
            select(BookCopy).where(BookCopy.copy_code == copy_code)
        ).first()

    def get_available_by_book(self, book_id: int) -> BookCopy | None:
        return self.db.scalars(
            select(BookCopy).where(
                BookCopy.book_id == book_id,
                BookCopy.status == CopyStatus.AVAILABLE,
            ).order_by(BookCopy.copy_code)
        ).first()

    def add(self, copy: BookCopy) -> BookCopy:
        self.db.add(copy)
        return copy
