from sqlalchemy import  String, Float, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from hotel_fastapi.database import Base

class Room(Base):
    __tablename__ = 'rooms'
    id : Mapped[int] = mapped_column(primary_key=True)
    hotel_id : Mapped[int] = mapped_column(ForeignKey('hotels_id'))
    room_type : Mapped[str] = mapped_column(String(500))
    price : Mapped[float] = mapped_column(Float)
    image_url : Mapped[str] = mapped_column(String(1000))
    description : Mapped[str] = mapped_column(String(1000))
    hotel : Mapped['Hotel'] = relationship(back_populates="rooms")
