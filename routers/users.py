from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from ..dependencies import get_current_user, get_session, get_password_hash
from ..database import User
from ..models.users import UserCreate, UserPublic
from pathvalidate import sanitize_filename
import os
import shutil

router = APIRouter(
    prefix="/users",
    # For FastAPI auto documentation
    tags=["users"]
)

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency Injection for Current User
CurrentUserDep = Annotated[User, Depends(get_current_user)]

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/me", response_model=UserCreate)
async def read_user_me(
    current_user: CurrentUserDep
):
    return current_user

@router.post("", response_model=UserPublic)
async def register_new_user(
    session: SessionDep,
    request: Annotated[UserCreate, Form()],
):
    existing_user_by_username = session.exec(
        select(User)
        .where(User.username == request.username)
    ).first()

    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{request.username}' already exists."
        )

    existing_user_by_email = session.exec(
        select(User)
        .where(User.email == request.email)
    ).first()

    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{request.email} is already in use."
        )

    hashed_password = get_password_hash(request.password)
    user_data = request.model_dump()
    user_data["password"] = hashed_password

    if request.profile_picture:
        sanitized_filename = sanitize_filename(request.profile_picture.filename) 
        file_path = os.path.join(UPLOAD_DIR, sanitized_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(request.profile_picture.file, buffer)
        
        user_data["profile_picture"] = f"/images/{sanitized_filename}"
        
    new_user = User(**user_data)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user 
