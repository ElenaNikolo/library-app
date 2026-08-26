from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_member, require_staff
from app.models.loan_request import LoanRequest
from app.models.user import User
from app.schemas.requests import LoanRequestCreate, LoanRequestResponse
from app.services import loans, requests

router = APIRouter(prefix="/api", tags=["requests"])


def request_response(request: LoanRequest) -> LoanRequestResponse:
    return LoanRequestResponse(
        id=request.id,
        book_id=request.book_id,
        book_title=request.book.title,
        member_name=request.member.full_name,
        request_date=request.request_date,
        decided_date=request.decided_date,
        status=request.status,
    )


@router.post("/requests", response_model=LoanRequestResponse, status_code=201)
def create_request(
    data: LoanRequestCreate,
    user: User = Depends(require_member),
    db: Session = Depends(get_db),
):
    try:
        request = requests.create_request(db, user, data)
    except requests.MemberProfileRequiredError as error:
        raise HTTPException(status_code=403, detail=str(error))
    except requests.BookNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except requests.AlreadyRequestedError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return request_response(request)


@router.get("/requests/my", response_model=list[LoanRequestResponse])
def my_requests(user: User = Depends(require_member), db: Session = Depends(get_db)):
    return [request_response(request) for request in requests.my_requests(db, user)]


@router.get(
    "/requests",
    response_model=list[LoanRequestResponse],
    dependencies=[Depends(require_staff)],
)
def list_requests(db: Session = Depends(get_db)):
    return [request_response(request) for request in requests.list_requests(db)]


@router.post(
    "/requests/{request_id}/approve",
    response_model=LoanRequestResponse,
    dependencies=[Depends(require_staff)],
)
def approve_request(request_id: int, db: Session = Depends(get_db)):
    request = requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Το αίτημα δεν βρέθηκε")

    try:
        requests.approve_request(db, request)
    except requests.InvalidStatusError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return request_response(request)


@router.post(
    "/requests/{request_id}/reject",
    response_model=LoanRequestResponse,
    dependencies=[Depends(require_staff)],
)
def reject_request(request_id: int, db: Session = Depends(get_db)):
    request = requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Το αίτημα δεν βρέθηκε")

    try:
        requests.reject_request(db, request)
    except requests.InvalidStatusError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return request_response(request)


@router.post(
    "/requests/{request_id}/cancel",
    response_model=LoanRequestResponse,
    dependencies=[Depends(require_staff)],
)
def cancel_request(request_id: int, db: Session = Depends(get_db)):
    request = requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Το αίτημα δεν βρέθηκε")

    try:
        requests.cancel_request(db, request)
    except requests.InvalidStatusError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return request_response(request)


@router.post(
    "/requests/{request_id}/fulfill",
    response_model=LoanRequestResponse,
    dependencies=[Depends(require_staff)],
)
def fulfill_request(request_id: int, db: Session = Depends(get_db)):
    request = requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Το αίτημα δεν βρέθηκε")

    try:
        loans.fulfill_request(db, request)
    except loans.RequestNotApprovedError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except loans.CopyNotAvailableError as error:
        raise HTTPException(status_code=409, detail=str(error))

    return request_response(request)
