from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.models.city import City
from hotel_fastapi.models.hotel import Hotel
from hotel_fastapi.models.user import User
from hotel_fastapi.schemes.hotel import HotelCreate, HotelResponse
from hotel_fastapi.security import get_current_user, require_admin

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.post('/', response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    city = db.query(City).filter(City.id == hotel.city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='city not found')

    new_hotel = Hotel(**hotel.model_dump())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


@router.get('/', response_model=List[HotelResponse])
def get_hotels(city: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Hotel)
    if city:
        query = query.join(City).filter(City.name == city)
    return query.all()


@router.get('/{hotel_id}', response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='hotel not found')
    return hotel