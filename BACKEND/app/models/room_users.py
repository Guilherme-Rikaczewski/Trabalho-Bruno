from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, func, Index
from app.db.base import Base
from app.schemas.room_schema import RoomRole


class RoomUser(Base):
    __tablename__ = "room_users"

    __table_args__ = (
        Index("idx_user_last_access", "user_id", "last_access"),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role = Column(
        Enum(RoomRole, name="room_role"),
        nullable=False,
    )

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    last_access = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
