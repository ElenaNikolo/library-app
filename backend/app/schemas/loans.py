from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models.loan import LoanStatus


class LoanCreate(BaseModel):
    member_id: int
    copy_id: int


class LoanResponse(BaseModel):
    id: int
    member_name: str
    book_title: str
    copy_code: str
    loan_date: date
    due_date: date
    return_date: date | None
    status: LoanStatus
    fine_amount: Decimal
    days_overdue: int
