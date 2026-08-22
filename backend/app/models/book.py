from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.author import Author
from app.models.category import Category

# Ενώνει βιβλία και συγγραφείς. Ένα βιβλίο μπορεί να έχει πολλούς
# συγγραφείς και ένας συγγραφέας πολλά βιβλία.
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    title: Mapped[str] = mapped_column(String(200))

    publisher: Mapped[str | None] = mapped_column(String(120))
    publication_year: Mapped[int | None]
    description: Mapped[str | None] = mapped_column(Text)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped[Category] = relationship()
    authors: Mapped[list[Author]] = relationship(secondary=book_authors)
