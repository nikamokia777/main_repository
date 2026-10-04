from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel_fastapi.database import Base


class RoomType(Base):
    __tablename__ = 'room_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    rooms: Mapped[list['Room']] = relationship(back_populates='room_type')