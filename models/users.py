from fastapi import UploadFile
from sqlmodel import Field, SQLModel, create_engine, select
from pydantic import EmailStr 
from datetime import datetime, timezone

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, min_length=1, max_length=30)
    email: EmailStr = Field(unique=True, max_length=255)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    birthday: datetime 
    biography: str = Field(max_length=255)
    favorite_number: int

# Response model
class UserPublic(UserBase):
    id: int
    created_at: datetime
    profile_picture: str

# Create request model
class UserCreate(UserBase):
    password: str= Field(min_length=1)
    profile_picture: UploadFile | None = None,

# Edit request model
class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=1, max_length=30) 
    password: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    first_name: str  | None = Field(default=None, min_length=1)
    last_name: str  | None = Field(default=None, min_length=1)
    birthday: datetime | None = None
    biography: str | None = Field(default=None, max_length=255)
    favorite_number: int | None = None
    profile_picture: UploadFile | None = None
