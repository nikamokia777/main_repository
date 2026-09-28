from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, model_validator
class UserCreate(BaseModel):
    username: str = Field( min_length=3, max_length=50)
    email: EmailStr 
    password: str = Field(min_length=8, max_length=200)
    confirm_password: str = Field(min_length=8, max_length=200)
    @model_validator(mode='before')
    def passwords_match(cls, value):
        password = value.get('password')
        confirm_password = value.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return value
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    
    class Config:
       from_attributes = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str


