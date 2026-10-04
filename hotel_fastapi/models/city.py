from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel_fastapi.database import Base


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    hotels: Mapped[list['Hotel']] = relationship(back_populates='city')