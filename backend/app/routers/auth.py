from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.repositories.users import MemberRepository
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from app.services import auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = auth.register_member(db, data)
    except auth.AlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))

    member = MemberRepository(db).get_by_user_id(user.id)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        member_id=member.id,
    )


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        token = auth.login(db, form.username, form.password)
    except auth.InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Λάθος όνομα χρήστη ή κωδικός",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.AccountDisabledError:
        raise HTTPException(
            status_code=403,
            detail="Ο λογαριασμός σας είναι απενεργοποιημένος.",
        )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = MemberRepository(db).get_by_user_id(user.id)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        member_id=member.id if member else None,
    )
