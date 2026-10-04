from datetime import date, datetime
from pydantic import BaseModel

class BookingCreate(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class BookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    check_in: date
    check_out: date
    status: str
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True