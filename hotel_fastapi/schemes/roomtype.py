from pydantic import BaseModel, Field


class RoomTypeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class RoomTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True