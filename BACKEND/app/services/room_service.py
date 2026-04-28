from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.rooms import Room
from app.models.room_users import RoomUser
from app.schemas.room_schema import RoomCreate, RoomUpdate
from app.utils.code import generate_code


def create_room(db: Session, room_data: RoomCreate) -> Room:
    try:
        while True:
            room = Room(**room_data.model_dump())
            room.code = generate_code()

            try:
                db.add(room)
                db.commit()
                db.refresh(room)

                break
            except IntegrityError:
                db.rollback()
            except Exception:
                db.rollback()
                raise

        return room
    except Exception:
        raise


def update_room(
        db: Session,
        room_id: int,
        room_data: RoomUpdate
        ) -> Room | None:
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return None

        update_data: dict[str, str] = room_data.model_dump(
            exclude_unset=True, exclude_none=True
        )

        for k, v in update_data.items():
            setattr(room, k, v.strip())

        db.commit()
        db.refresh(room)

        return room
    except Exception:
        db.rollback()
        raise


def get_room(db: Session, room_id: int) -> Room | None:
    try:
        room = db.get(Room, room_id)
        return room
    except Exception:
        raise


def get_all_rooms_from_user(db: Session, user_id: int) -> list[Room] | None:
    try:
        rooms = (
            db.query(
                Room,
                RoomUser.role.label("role")
            )
            .join(RoomUser, RoomUser.room_id == Room.id)
            .filter(RoomUser.user_id == user_id)
            .order_by(Room.room_name)
            .all()
        )
        if not rooms:
            return None

        result: list = []

        for room, role in rooms:
            result.append({
                "id": room.id,
                "room_name": room.room_name,
                "code": room.code,
                "role": role,
                "created_at": room.created_at,
                "updated_at": room.updated_at,
            })

        return result
    except Exception:
        raise


def get_recent_rooms_from_user(db: Session, user_id: int) -> list[Room] | None:
    try:
        rooms = (
            db.query(
                Room,
                RoomUser.role.label("role")
            )
            .join(RoomUser, RoomUser.room_id == Room.id)
            .filter(RoomUser.user_id == user_id)
            .order_by(RoomUser.last_access.desc())
            .limit(9)
            .all()
        )
        if not rooms:
            return None

        result: list = []

        for room, role in rooms:
            result.append({
                "id": room.id,
                "room_name": room.room_name,
                "code": room.code,
                "role": role,
                "created_at": room.created_at,
                "updated_at": room.updated_at,
            })

        return result
    except Exception:
        raise


def delete_room(db: Session, room_id: int) -> bool:
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return False

        db.delete(room)
        db.commit()
        # db.refresh(room)

        return True
    except Exception:
        db.rollback()
        raise
