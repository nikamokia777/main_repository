from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hotel_fastapi import get_db
from hotel_fastapi.schemes.user import UserCreate, UserResponse, UserLogin
from hotel_fastapi.models import User
from hotel_fastapi.security import hash_password, verify_password

router = APIRouter(prefix="/user", tags=["users"])

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query().filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"message": "Login successful"}