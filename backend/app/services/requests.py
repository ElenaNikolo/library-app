from datetime import date

from sqlalchemy.orm import Session

from app.models.loan_request import LoanRequest, RequestStatus
from app.models.user import User
from app.repositories.catalog import BookRepository
from app.repositories.requests import LoanRequestRepository
from app.repositories.users import MemberRepository
from app.schemas.requests import LoanRequestCreate


class MemberProfileRequiredError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class AlreadyRequestedError(Exception):
    pass


class InvalidStatusError(Exception):
    pass


def list_requests(db: Session) -> list[LoanRequest]:
    return LoanRequestRepository(db).get_all()


def my_requests(db: Session, user: User) -> list[LoanRequest]:
    member = MemberRepository(db).get_by_user_id(user.id)
    if member is None:
        return []

    return LoanRequestRepository(db).get_by_member(member.id)


def get_request(db: Session, request_id: int) -> LoanRequest | None:
    return LoanRequestRepository(db).get_by_id(request_id)


def create_request(db: Session, user: User, data: LoanRequestCreate) -> LoanRequest:
    member = MemberRepository(db).get_by_user_id(user.id)
    if member is None:
        raise MemberProfileRequiredError(
            "Μόνο τα μέλη μπορούν να ζητήσουν βιβλίο."
        )

    book = BookRepository(db).get_by_id(data.book_id)
    if book is None:
        raise BookNotFoundError("Το βιβλίο δεν βρέθηκε.")

    requests = LoanRequestRepository(db)
    if requests.get_active_for(member.id, book.id):
        raise AlreadyRequestedError("Έχετε ήδη ενεργό αίτημα για αυτό το βιβλίο.")

    request = LoanRequest(member=member, book=book, request_date=date.today())
    requests.add(request)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return request


def approve_request(db: Session, request: LoanRequest) -> LoanRequest:
    if request.status != RequestStatus.PENDING:
        raise InvalidStatusError("Το αίτημα δεν είναι σε εκκρεμότητα.")

    request.status = RequestStatus.APPROVED
    request.decided_date = date.today()

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return request


def reject_request(db: Session, request: LoanRequest) -> LoanRequest:
    if request.status != RequestStatus.PENDING:
        raise InvalidStatusError("Το αίτημα δεν είναι σε εκκρεμότητα.")

    request.status = RequestStatus.REJECTED
    request.decided_date = date.today()

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return request


def cancel_request(db: Session, request: LoanRequest) -> LoanRequest:
    if request.status != RequestStatus.APPROVED:
        raise InvalidStatusError("Μόνο εγκεκριμένο αίτημα μπορεί να ακυρωθεί.")

    request.status = RequestStatus.CANCELLED
    request.decided_date = date.today()

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return request
