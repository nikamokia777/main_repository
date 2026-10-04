from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel_fastapi.database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    room_type_id: Mapped[int] = mapped_column(ForeignKey('room_types.id'))
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(1000))

    hotel: Mapped['Hotel'] = relationship(back_populates='rooms')
    room_type: Mapped['RoomType'] = relationship(back_populates='rooms')