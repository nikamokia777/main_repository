from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.models.roomtype import RoomType
from hotel_fastapi.models.room import Room
from hotel_fastapi.models.user import User
from hotel_fastapi.schemes.roomtype import RoomTypeCreate, RoomTypeResponse
from hotel_fastapi.security import get_current_user, require_admin

router = APIRouter(prefix='/room-types', tags=['Room types'])


@router.post('/', response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_room_type(roomtype: RoomTypeCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    existing_type = db.query(RoomType).filter(RoomType.name == roomtype.name).first()
    if existing_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='room type already exists')

    new_type = RoomType(name=roomtype.name)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.get('/', response_model=List[RoomTypeResponse])
def get_room_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(RoomType).all()


@router.delete('/{room_type_id}')
def delete_room_type(roomtype_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    roomtype = db.query(RoomType).filter(RoomType.id == roomtype_id).first()
    if not roomtype:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='room type not found')

    has_rooms = db.query(Room).filter(Room.room_type_id == roomtype_id).first()
    if has_rooms:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='room type has rooms and can not be deleted')

    db.delete(roomtype)
    db.commit()
    return {'message': 'room type deleted'}