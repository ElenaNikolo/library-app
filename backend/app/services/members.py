from sqlalchemy.orm import Session

from app.models.member import Member
from app.repositories.users import MemberRepository


def list_members(db: Session, search: str | None) -> list[Member]:
    return MemberRepository(db).get_all(search)


def get_member(db: Session, member_id: int) -> Member | None:
    return MemberRepository(db).get_by_id(member_id)
