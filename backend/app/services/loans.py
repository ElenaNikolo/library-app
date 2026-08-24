from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.book_copy import CopyStatus
from app.models.loan import LOAN_PERIOD_DAYS, Loan, LoanStatus
from app.models.user import User
from app.repositories.catalog import BookCopyRepository
from app.repositories.loans import LoanRepository
from app.repositories.users import MemberRepository
from app.schemas.loans import LoanCreate


class InvalidLoanDataError(Exception):
    pass


class CopyNotAvailableError(Exception):
    pass


class LoanAlreadyReturnedError(Exception):
    pass


def list_loans(db: Session, status: LoanStatus | None) -> list[Loan]:
    return LoanRepository(db).get_all(status)


def list_overdue(db: Session) -> list[Loan]:
    return LoanRepository(db).get_overdue()


def my_loans(db: Session, user: User) -> list[Loan]:
    member = MemberRepository(db).get_by_user_id(user.id)
    if member is None:
        return []

    return LoanRepository(db).get_by_member(member.id)


def get_loan(db: Session, loan_id: int) -> Loan | None:
    return LoanRepository(db).get_by_id(loan_id)


def create_loan(db: Session, data: LoanCreate) -> Loan:
    member = MemberRepository(db).get_by_id(data.member_id)
    if member is None:
        raise InvalidLoanDataError("Το μέλος δεν υπάρχει.")

    copy = BookCopyRepository(db).get_by_id(data.copy_id)
    if copy is None:
        raise InvalidLoanDataError("Το αντίτυπο δεν υπάρχει.")

    if copy.status != CopyStatus.AVAILABLE:
        raise CopyNotAvailableError("Το αντίτυπο δεν είναι διαθέσιμο.")

    today = date.today()
    loan = Loan(
        member=member,
        book_copy=copy,
        loan_date=today,
        due_date=today + timedelta(days=LOAN_PERIOD_DAYS),
    )
    copy.status = CopyStatus.ON_LOAN
    LoanRepository(db).add(loan)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan


def return_loan(db: Session, loan: Loan) -> Loan:
    if loan.status == LoanStatus.RETURNED:
        raise LoanAlreadyReturnedError("Ο δανεισμός έχει ήδη επιστραφεί.")

    loan.return_date = date.today()
    loan.status = LoanStatus.RETURNED
    loan.fine_amount = loan.calculate_fine()
    loan.book_copy.status = CopyStatus.AVAILABLE

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan
