from pydantic import BaseModel

from hotel_fastapi.schemes.city import CityResponse


class HotelCreate(BaseModel):
    name: str
    city_id: int
    description: str


class HotelResponse(BaseModel):
    id: int
    name: str
    description: str
    city: CityResponse

    class Config:
        from_attributes = True