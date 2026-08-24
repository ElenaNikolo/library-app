from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.users import MemberRepository, UserRepository
from app.schemas.users import UserCreate, UserUpdate
from app.security import hash_password


class UserAlreadyExistsError(Exception):
    pass


class InvalidUserUpdateError(Exception):
    pass


def list_users(db: Session) -> list[User]:
    return UserRepository(db).get_all()


def get_user(db: Session, user_id: int) -> User | None:
    return UserRepository(db).get_by_id(user_id)


def create_user(db: Session, data: UserCreate) -> User:
    users = UserRepository(db)

    if users.get_by_username(data.username):
        raise UserAlreadyExistsError("Το όνομα χρήστη χρησιμοποιείται ήδη.")
    if users.get_by_email(data.email):
        raise UserAlreadyExistsError("Το email χρησιμοποιείται ήδη.")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    users.add(user)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return user


def update_user(db: Session, user: User, data: UserUpdate, admin: User) -> User:
    if user.id == admin.id and (data.role != UserRole.ADMIN or not data.is_active):
        raise InvalidUserUpdateError(
            "Δεν μπορείτε να αφαιρέσετε τα δικαιώματα διαχειριστή "
            "ή να απενεργοποιήσετε τον λογαριασμό σας."
        )

    if data.role == UserRole.MEMBER and MemberRepository(db).get_by_user_id(user.id) is None:
        raise InvalidUserUpdateError("Ο χρήστης δεν έχει προφίλ μέλους.")

    user.role = data.role
    user.is_active = data.is_active

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return user
