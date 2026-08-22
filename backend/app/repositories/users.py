from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalars(select(User).where(User.username == username)).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalars(select(User).where(User.email == email)).first()

    def get_all(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.username)))

    def add(self, user: User) -> User:
        self.db.add(user)
        return user


class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, member_id: int) -> Member | None:
        return self.db.get(Member, member_id)

    def get_by_user_id(self, user_id: int) -> Member | None:
        return self.db.scalars(select(Member).where(Member.user_id == user_id)).first()

    def get_all(self, search: str | None = None) -> list[Member]:
        query = select(Member)

        if search:
            pattern = f"%{search}%"
            query = query.where(
                Member.first_name.ilike(pattern) | Member.last_name.ilike(pattern)
            )

        return list(self.db.scalars(query.order_by(Member.last_name, Member.first_name)))

    def add(self, member: Member) -> Member:
        self.db.add(member)
        return member
