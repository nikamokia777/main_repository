from pydantic import BaseModel, Field

from hotel_fastapi.schemes.roomtype import RoomTypeResponse


class RoomCreate(BaseModel):
    hotel_id: int
    room_type_id: int
    price: float = Field(gt=0)
    description: str


class RoomResponse(BaseModel):
    id: int
    hotel_id: int
    price: float
    description: str
    room_type: RoomTypeResponse

    class Config:
        from_attributes = True