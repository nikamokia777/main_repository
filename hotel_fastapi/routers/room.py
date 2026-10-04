from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.models.booking import Booking
from hotel_fastapi.models.hotel import Hotel
from hotel_fastapi.models.room import Room
from hotel_fastapi.models.roomtype import RoomType
from hotel_fastapi.models.user import User
from hotel_fastapi.schemes.room import RoomCreate, RoomResponse
from hotel_fastapi.security import get_current_user, require_admin

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.post('/', response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    hotel = db.query(Hotel).filter(Hotel.id == room.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='hotel not found')

    room_type = db.query(RoomType).filter(RoomType.id == room.room_type_id).first()
    if not room_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='room type not found')

    new_room = Room(**room.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get('/', response_model=List[RoomResponse])
def get_rooms(
    hotel_id: Optional[int] = None,
    room_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    check_in: Optional[date] = None,
    check_out: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Room)
    if hotel_id:
        query = query.filter(Room.hotel_id == hotel_id)
    if room_type:
        query = query.join(RoomType).filter(RoomType.name == room_type)
    if min_price is not None:
        query = query.filter(Room.price >= min_price)
    if max_price is not None:
        query = query.filter(Room.price <= max_price)

    if check_in and check_out:
        if check_out <= check_in:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='check_out must be after check_in')

        booked_room_ids = db.query(Booking.room_id).filter(
            Booking.status == 'booked',
            Booking.check_in < check_out,
            Booking.check_out > check_in
        )

        query = query.filter(~Room.id.in_(booked_room_ids))

    return query.all()


@router.get('/{room_id}', response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='room not found')
    return room