from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.models.city import City
from hotel_fastapi.models.hotel import Hotel
from hotel_fastapi.models.user import User
from hotel_fastapi.schemes.city import CityCreate, CityResponse
from hotel_fastapi.security import get_current_user, require_admin

router = APIRouter(prefix='/cities', tags=['Cities'])


@router.post('/', response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    existing_city = db.query(City).filter(City.name == city.name).first()
    if existing_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city already exists')

    new_city = City(name=city.name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get('/', response_model=List[CityResponse])
def get_cities(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(City).all()


@router.delete('/{city_id}')
def delete_city(city_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='city not found')

    has_hotels = db.query(Hotel).filter(Hotel.city_id == city_id).first()
    if has_hotels:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city has hotels and can not be deleted')

    db.delete(city)
    db.commit()
    return {'message': 'city deleted'}