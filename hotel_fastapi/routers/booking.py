from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.models.booking import Booking
from hotel_fastapi.models.room import Room
from hotel_fastapi.models.user import User
from hotel_fastapi.models.hotel import Hotel
from hotel_fastapi.schemes.booking import BookingCreate, BookingResponse
from hotel_fastapi.security import get_current_user
from hotel_fastapi.models.city import City

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.post('/', response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='room not found')

    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='check_out must be after check_in')

    overlapping = db.query(Booking).filter(
        Booking.room_id == booking.room_id,
        Booking.status == 'booked',
        Booking.check_in < booking.check_out,
        Booking.check_out > booking.check_in
    ).first()
    if overlapping:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='room is already booked for these dates')

    nights = (booking.check_out - booking.check_in).days
    total_price = nights * room.price

    new_booking = Booking(
        room_id=booking.room_id,
        user_id=current_user.id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status='booked',
        total_price=total_price
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.get('/', response_model=List[BookingResponse])
def get_bookings(city: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Booking).filter(Booking.user_id == current_user.id)
    if city:
        query = query.join(Room).join(Hotel).join(City).filter(City.name == city)
    return query.all()


@router.delete('/{booking_id}')
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='booking not found')

    booking.status = 'cancelled'
    db.commit()
    return {'message': 'booking cancelled'}