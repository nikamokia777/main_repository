from fastapi import APIRouter, Depends , HTTPException, status , BackgroundTasks
from app.schemes.user import UserCreate, UserResponse, UserLogin, UserUpdate
from app.database import get_db
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.security import hash_password, verify_password, create_access_token, create_refresh_token, get_current_user, require_admin
from typing import List
import time

router = APIRouter(prefix='/user', tags=['users'])
def send_welcome_email(email: str):
    print(f'Sending welcome email to {email}')
    time.sleep(3)
    print(f'Email sent to {email}')

@router.post('/register', response_model= UserResponse, status_code= status.HTTP_201_CREATED)
def create_user(user : UserCreate, background_tasks: BackgroundTasks, db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = 'there is existing account with this email')
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    background_tasks.add_task(send_welcome_email, new_user.email)
    
    return new_user

@router.post('/login')
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid email or password')

    access_token = create_access_token({'user_id': user.id})
    refresh_token = create_refresh_token({'user_id': user.id})

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@router.get('/', response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).all()
    return users

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    db.delete(user)
    db.commit()
    return None

@router.patch('/me', response_model=UserResponse)
def update_my_profile(updates: UserUpdate,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if updates.email and updates.email != current_user.email:
        existing = db.query(User).filter(User.email == updates.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this email is already taken')
        current_user.email = updates.email

    if updates.username and updates.username != current_user.username:
        existing = db.query(User).filter(User.username == updates.username).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this username is already taken')
        current_user.username = updates.username

    if updates.new_password:
        if not verify_password(updates.old_password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='old password is incorrect')
        current_user.hashed_password = hash_password(updates.new_password)

    db.commit()
    db.refresh(current_user)
    return current_user

    