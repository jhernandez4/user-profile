from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: int 
    username: str 
    # Exclude password
    email: EmailStr
    first_name: str 
    last_name: str 
    birthday: datetime 
    biography: str 
    favorite_number: int 
    profile_picture: str

    # Exclude created_at 