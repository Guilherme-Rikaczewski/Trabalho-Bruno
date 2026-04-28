from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room_schema import (RoomCreate, RoomUpdate,
                                     RoomResponse, RoomRole)
from app.schemas.types import RoomCode
import app.services.room_user_service as rus
import app.services.room_service as rs
from app.services.auth_service import get_current_user_id


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse)
def create(
    room: RoomCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
        ):
    try:
        new_room = rs.create_room(db, room)
        room_user = rus.create_room_user(db, new_room.id, user_id)
        setattr(new_room, 'role', room_user.role)
        return new_room
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.patch('/{room_id}', response_model=RoomResponse)
def update(room_id: int,
           room: RoomUpdate,
           user_id: int = Depends(get_current_user_id), 
           db: Session = Depends(get_db)):
    try:
        room_user = rus.read_role_room_user(db, room_id, user_id)
        if room_user.role != RoomRole.master:
            raise HTTPException(403, detail='Permission denied')

        updated_room = rs.update_room(db, room_id, room)
        setattr(updated_room, 'role', room_user.role)
        return updated_room
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(500, detail=f'Internal server error {error}')


@router.get('/{room_id}', response_model=RoomResponse)
def read(
    room_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
        ):
    try:
        get_room = rs.get_room(db, room_id)
        if not get_room:
            raise HTTPException(500, detail='Internal server error')

        room_user = rus.read_role_room_user(db, room_id, user_id)
        setattr(get_room, 'role', room_user.role)
        return get_room
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.get('/all/')
def read_all(user_id: int = Depends(get_current_user_id),
             db: Session = Depends(get_db)):
    try:
        return rs.get_all_rooms_from_user(db, user_id)
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.get('/recent/')
def read_recent(user_id: int = Depends(get_current_user_id),
                db: Session = Depends(get_db)):
    try:
        return rs.get_recent_rooms_from_user(db, user_id)
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.delete('/{room_id}', status_code=204)
def delete(room_id: int,
           user_id: int = Depends(get_current_user_id),
           db: Session = Depends(get_db)):
    try:
        room_user = rus.read_role_room_user(db, room_id, user_id)
        if room_user.role != RoomRole.master:
            raise HTTPException(403, detail='Permission denied')

        success = rs.delete_room(db, room_id)

        if not success:
            raise
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(500, detail=f'Internal server error {error}')


@router.post('/join/{room_code}', response_model=RoomResponse)
def join_room(
    room_code: RoomCode,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        room_user = rus.join_room_by_code(
            db, room_code, user_id
        )

        room = rs.get_room(db, room_user.room_id)
        if not room:
            raise HTTPException(500, detail='Internal server error')

        setattr(room, 'role', room_user.role)
        return room
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, detail='Internal server error')
