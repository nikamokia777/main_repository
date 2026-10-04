from fastapi import FastAPI
from hotel_fastapi.routers import user, city, roomtype, hotel, room, booking

app = FastAPI()

app.include_router(user.router)
app.include_router(city.router)
app.include_router(roomtype.router)
app.include_router(hotel.router)
app.include_router(room.router)
app.include_router(booking.router)