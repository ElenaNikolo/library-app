from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.repositories.users import UserRepository
from app.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Μη έγκυρο ή ληγμένο token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserRepository(db).get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Μη έγκυρο ή ληγμένο token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Ο λογαριασμός σας είναι απενεργοποιημένος.",
        )

    return user


def require_staff(user: User = Depends(get_current_user)) -> User:
    if user.role not in (UserRole.ADMIN, UserRole.LIBRARIAN):
        raise HTTPException(
            status_code=403,
            detail="Δεν έχετε δικαίωμα για αυτή την ενέργεια",
        )

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Απαιτούνται δικαιώματα διαχειριστή",
        )

    return user
