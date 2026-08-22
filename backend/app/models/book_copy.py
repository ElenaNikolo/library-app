import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book


class CopyStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ON_LOAN = "ON_LOAN"
    LOST = "LOST"


class BookCopy(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    copy_code: Mapped[str] = mapped_column(String(30), unique=True)

    status: Mapped[CopyStatus] = mapped_column(
        Enum(CopyStatus), default=CopyStatus.AVAILABLE
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))

    book: Mapped[Book] = relationship()
