from sqlalchemy.orm import Session
from app.models.room_users import RoomUser
from app.models.rooms import Room
from app.schemas.types import RoomCode


def create_room_user(db: Session, room_id: int, user_id: int) -> RoomUser:
    try:
        rule_data = {
            "user_id": user_id,
            "room_id": room_id,
            "role": "master",
        }
        room_user = RoomUser(**rule_data)

        db.add(room_user)
        db.commit()
        db.refresh(room_user)

        return room_user
    except Exception:
        db.rollback()
        raise


def read_role_room_user(db: Session, room_id: int, user_id: int) -> RoomUser:
    try:
        room_user = db.query(RoomUser).filter(
            RoomUser.room_id == room_id,
            RoomUser.user_id == user_id
        ).first()
        return room_user
    except Exception:
        db.rollback()
        raise


def join_room_by_code(db: Session, code: RoomCode, user_id: int) -> RoomUser:
    try:
        room = db.query(Room).filter(Room.code == code).first()
        rule_data = {
            "user_id": user_id,
            "room_id": room.id,
            "role": "player",
        }
        room_user = RoomUser(**rule_data)

        db.add(room_user)
        db.commit()
        db.refresh(room_user)

        return room_user
    except Exception:
        db.rollback()
        raise
