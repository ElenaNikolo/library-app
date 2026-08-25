from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.loan_request import LoanRequest, RequestStatus


class LoanRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, request_id: int) -> LoanRequest | None:
        return self.db.get(LoanRequest, request_id)

    def get_all(self) -> list[LoanRequest]:
        query = select(LoanRequest)
        return list(self.db.scalars(query.order_by(LoanRequest.request_date.desc())))

    def get_by_member(self, member_id: int) -> list[LoanRequest]:
        query = select(LoanRequest).where(LoanRequest.member_id == member_id)
        return list(self.db.scalars(query.order_by(LoanRequest.request_date.desc())))

    def get_active_for(self, member_id: int, book_id: int) -> LoanRequest | None:
        return self.db.scalars(
            select(LoanRequest).where(
                LoanRequest.member_id == member_id,
                LoanRequest.book_id == book_id,
                LoanRequest.status.in_(
                    (RequestStatus.PENDING, RequestStatus.APPROVED)
                ),
            )
        ).first()

    def add(self, request: LoanRequest) -> LoanRequest:
        self.db.add(request)
        return request
