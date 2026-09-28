from fastapi import FastAPI
from hotel_fastapi.database import engine, Base
from hotel_fastapi.routers import user, room , hotel

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(room.router)
app.include_router(hotel.router)