import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book_copy import BookCopy
from app.models.member import Member

LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = Decimal("0.50")


class LoanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    book_copy_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id"))

    loan_date: Mapped[date] = mapped_column(Date)
    due_date: Mapped[date] = mapped_column(Date)
    return_date: Mapped[date | None] = mapped_column(Date)

    status: Mapped[LoanStatus] = mapped_column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    fine_amount: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=Decimal("0.00"))

    member: Mapped[Member] = relationship()
    book_copy: Mapped[BookCopy] = relationship()

    def days_overdue(self, today: date | None = None) -> int:
        """Πόσες μέρες έχει καθυστερήσει. Μηδέν αν είμαστε εντός προθεσμίας."""
        reference = self.return_date or today or date.today()
        if reference <= self.due_date:
            return 0
        return (reference - self.due_date).days

    def calculate_fine(self, today: date | None = None) -> Decimal:
        return FINE_PER_DAY * self.days_overdue(today)
