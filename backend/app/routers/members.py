from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_staff
from app.schemas.members import MemberResponse
from app.services import members

router = APIRouter(prefix="/api", tags=["members"], dependencies=[Depends(require_staff)])


@router.get("/members", response_model=list[MemberResponse])
def list_members(search: str | None = None, db: Session = Depends(get_db)):
    return members.list_members(db, search)


@router.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = members.get_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Το μέλος δεν βρέθηκε")

    return member
