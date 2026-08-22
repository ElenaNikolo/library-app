from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.loan import Loan, LoanStatus


class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, loan_id: int) -> Loan | None:
        return self.db.get(Loan, loan_id)

    def get_all(self, status: LoanStatus | None = None) -> list[Loan]:
        query = select(Loan)

        if status:
            query = query.where(Loan.status == status)

        return list(self.db.scalars(query.order_by(Loan.loan_date.desc())))

    def get_by_member(self, member_id: int, status: LoanStatus | None = None) -> list[Loan]:
        query = select(Loan).where(Loan.member_id == member_id)

        if status:
            query = query.where(Loan.status == status)

        return list(self.db.scalars(query.order_by(Loan.loan_date.desc())))

    def get_overdue(self) -> list[Loan]:
        query = select(Loan).where(
            Loan.status == LoanStatus.ACTIVE,
            Loan.due_date < date.today(),
        )
        return list(self.db.scalars(query.order_by(Loan.due_date)))

    def add(self, loan: Loan) -> Loan:
        self.db.add(loan)
        return loan
