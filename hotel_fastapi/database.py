from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = 'postgresql://postgres:Mokia123$@localhost:1940/hotel_booking'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Base(DeclarativeBase):
    pass


