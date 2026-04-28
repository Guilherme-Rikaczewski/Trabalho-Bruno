from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
import app.services.user_service as us
from app.services.auth_service import get_current_user_id


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return us.create_user(db, user)
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.patch('/', response_model=UserResponse)
def update(
    user: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
        ):
    try:
        return us.update_user(db, user_id, user)
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.get('/', response_model=UserResponse)
def read(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
        ):
    try:
        return us.get_user(db, user_id)
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.delete('/', status_code=204)
def delete(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
        ):
    try:
        success = us.delete_user(db, user_id)

        if not success:
            raise
    except Exception:
        raise HTTPException(500, detail='Internal server error')
