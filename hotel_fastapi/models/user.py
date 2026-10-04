from datetime import datetime
from sqlalchemy import  String, DateTime, func
from sqlalchemy.orm import  mapped_column, Mapped
from hotel_fastapi.database import Base

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(50), unique=True,)
    email : Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password : Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(50), default='user', server_default='user')
    registered_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())