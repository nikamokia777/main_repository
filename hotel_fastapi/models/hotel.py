from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel_fastapi.database import Base


class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'))
    description: Mapped[str] = mapped_column(String(1000))

    city: Mapped['City'] = relationship(back_populates='hotels')
    rooms: Mapped[list['Room']] = relationship(back_populates='hotel', cascade='all, delete-orphan')