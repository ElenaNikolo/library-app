from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.users import UserCreate, UserListResponse, UserUpdate
from app.services import users

router = APIRouter(prefix="/api", tags=["users"], dependencies=[Depends(require_admin)])


@router.get("/users", response_model=list[UserListResponse])
def list_users(db: Session = Depends(get_db)):
    return users.list_users(db)


@router.post("/users", response_model=UserListResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return users.create_user(db, data)
    except users.UserAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.put("/users/{user_id}", response_model=UserListResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = users.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Ο χρήστης δεν βρέθηκε")

    try:
        return users.update_user(db, user, data, admin)
    except users.InvalidUserUpdateError as error:
        raise HTTPException(status_code=409, detail=str(error))
