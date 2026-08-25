from datetime import date

from pydantic import BaseModel

from app.models.loan_request import RequestStatus


class LoanRequestCreate(BaseModel):
    book_id: int


class LoanRequestResponse(BaseModel):
    id: int
    book_id: int
    book_title: str
    member_name: str
    request_date: date
    decided_date: date | None
    status: RequestStatus
