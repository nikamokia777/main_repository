from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi.database import get_db
from hotel_fastapi.schemes.user import UserCreate, UserResponse, UserLogin, RefreshTokenRequest
from hotel_fastapi.models import User
from hotel_fastapi.security import create_access_token, hash_password, verify_password, require_admin, create_refresh_token, SECRET_KEY, ALGORITHM  
from typing import List
from jose import jwt, JWTError

router = APIRouter(prefix='/user', tags=['users'])


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')
    access_token = create_access_token({'sub': str(existing_user.id)})
    refresh_token = create_refresh_token({'sub': str(existing_user.id)})
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@router.post('/refresh')
def refresh_access_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    invalid_token = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid or expired refresh token')
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        token_type = payload.get('type')
        if user_id is None or token_type != 'refresh':
            raise invalid_token
    except JWTError:
        raise invalid_token

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise invalid_token

    access_token = create_access_token({'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/', response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).all()


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return user