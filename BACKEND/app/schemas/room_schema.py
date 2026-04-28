from pydantic import BaseModel
from datetime import datetime
from app.schemas.types import RoomName, RoomCode
import enum


class RoomRole(enum.Enum):
    master = "master"
    player = "player"


class RoomCreate(BaseModel):
    room_name: RoomName


class RoomUpdate(BaseModel):
    room_name: RoomName


class RoomResponse(BaseModel):
    id: int
    room_name: RoomName
    code: RoomCode
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
