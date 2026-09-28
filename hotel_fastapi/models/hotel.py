from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from hotel_fastapi.database import Base

class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100),)
    description: Mapped[str] = mapped_column(String(1000))
    image_url: Mapped[str] = mapped_column(String(1000))
    rooms: Mapped[list['Room']] = relationship(back_populates="hotel", cascade="all, delete-orphan")



   

