from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user import User


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Το unique κάνει τη σχέση 1:1 - κάθε χρήστης έχει το πολύ ένα προφίλ μέλους.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(200))

    membership_date: Mapped[date] = mapped_column(default=date.today)

    user: Mapped[User] = relationship()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
