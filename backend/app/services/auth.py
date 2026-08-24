from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.user import User, UserRole
from app.repositories.users import MemberRepository, UserRepository
from app.schemas.auth import RegisterRequest
from app.security import create_token, hash_password, verify_password


class AlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AccountDisabledError(Exception):
    pass


def register_member(db: Session, data: RegisterRequest) -> User:
    users = UserRepository(db)

    if users.get_by_username(data.username):
        raise AlreadyExistsError("Το όνομα χρήστη χρησιμοποιείται ήδη.")
    if users.get_by_email(data.email):
        raise AlreadyExistsError("Το email χρησιμοποιείται ήδη.")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.MEMBER,
    )
    member = Member(
        user=user,
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        address=data.address,
    )

    users.add(user)
    MemberRepository(db).add(member)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return user


def login(db: Session, username: str, password: str) -> str:
    user = UserRepository(db).get_by_username(username)

    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise AccountDisabledError()

    return create_token(user.username)
