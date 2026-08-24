from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db, require_staff
from app.models.loan import Loan, LoanStatus
from app.models.user import User
from app.schemas.loans import LoanCreate, LoanResponse
from app.services import loans

router = APIRouter(prefix="/api", tags=["loans"])


def loan_response(loan: Loan) -> LoanResponse:
    return LoanResponse(
        id=loan.id,
        member_name=loan.member.full_name,
        book_title=loan.book_copy.book.title,
        copy_code=loan.book_copy.copy_code,
        loan_date=loan.loan_date,
        due_date=loan.due_date,
        return_date=loan.return_date,
        status=loan.status,
        fine_amount=loan.fine_amount,
        days_overdue=loan.days_overdue(),
    )


@router.get(
    "/loans",
    response_model=list[LoanResponse],
    dependencies=[Depends(require_staff)],
)
def list_loans(status: LoanStatus | None = None, db: Session = Depends(get_db)):
    return [loan_response(loan) for loan in loans.list_loans(db, status)]


@router.get(
    "/loans/overdue",
    response_model=list[LoanResponse],
    dependencies=[Depends(require_staff)],
)
def list_overdue(db: Session = Depends(get_db)):
    return [loan_response(loan) for loan in loans.list_overdue(db)]


@router.get("/loans/my", response_model=list[LoanResponse])
def my_loans(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [loan_response(loan) for loan in loans.my_loans(db, user)]


@router.post(
    "/loans",
    response_model=LoanResponse,
    status_code=201,
    dependencies=[Depends(require_staff)],
)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    try:
        loan = loans.create_loan(db, data)
    except loans.InvalidLoanDataError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except loans.CopyNotAvailableError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return loan_response(loan)


@router.post(
    "/loans/{loan_id}/return",
    response_model=LoanResponse,
    dependencies=[Depends(require_staff)],
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loans.get_loan(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Ο δανεισμός δεν βρέθηκε")

    try:
        loan = loans.return_loan(db, loan)
    except loans.LoanAlreadyReturnedError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return loan_response(loan)
