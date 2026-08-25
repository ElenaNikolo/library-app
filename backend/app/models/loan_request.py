import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book
from app.models.member import Member


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"


class LoanRequest(Base):
    __tablename__ = "loan_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    # Το αίτημα αφορά βιβλίο. Το αντίτυπο επιλέγεται κατά την παραλαβή.
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    request_date: Mapped[date] = mapped_column(Date)
    decided_date: Mapped[date | None] = mapped_column(Date)

    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus), default=RequestStatus.PENDING
    )

    # Συμπληρώνεται μόνο όταν το αίτημα καταλήξει σε πραγματικό δανεισμό.
    loan_id: Mapped[int | None] = mapped_column(ForeignKey("loans.id"))

    member: Mapped[Member] = relationship()
    book: Mapped[Book] = relationship()
