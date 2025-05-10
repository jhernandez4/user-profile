from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from ..dependencies import (
    get_current_user, get_session, get_password_hash, validate_non_empty_string,
    is_jpeg 
)
from ..database import User
from ..models.users import UserCreate, UserPublic, UserUpdate
from pathvalidate import sanitize_filename
import os
import shutil

router = APIRouter(
    prefix="/users",
    # For FastAPI auto documentation
    tags=["users"],
)

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency Injection for Current User
CurrentUserDep = Annotated[User, Depends(get_current_user)]

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/me", response_model=UserPublic)
async def read_user_me(
    current_user: CurrentUserDep
):
    return current_user

@router.patch("/me", response_model=UserPublic)
async def edit_user_me(
    current_user: CurrentUserDep,
    session: SessionDep,
    request: Annotated[UserUpdate, Form()]
):
    edit_user_data = request.model_dump(exclude_unset=True)
    
    # Check if username is already taken
    if "username" in edit_user_data:
        stripped_username = validate_non_empty_string("Username", edit_user_data["username"])
        existing_user = session.exec(
            select(User)
            .where(User.username == stripped_username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The username '{stripped_username}' is already taken."
            )

        edit_user_data["username"] = stripped_username

    # Check if email is already in use
    if "email" in edit_user_data:
        stripped_email = validate_non_empty_string("Email", edit_user_data["email"])
        existing_user = session.exec(
            select(User)
            .where(User.email == edit_user_data["email"])
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{edit_user_data["email"]} is already in use"
            )
        edit_user_data["email"] = stripped_email

    if "password" in edit_user_data:
        hashed_password = get_password_hash(edit_user_data["password"])
        edit_user_data["password"] = hashed_password 

    # Check if profile picture is being updated
    if "profile_picture" in edit_user_data and current_user.profile_picture:
        profile_picture = edit_user_data["profile_picture"]

        if not is_jpeg(profile_picture):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile picture must be a JPG or JPEG image"
            )

        # Extract filename from stored path
        old_file_path = current_user.profile_picture.lstrip("/")  # remove leading slash
        full_path = os.path.join(os.getcwd(), old_file_path)

        # Delete the old profile picture file if it exists
        if os.path.exists(full_path):
            os.remove(full_path)

        sanitized_filename = sanitize_filename(profile_picture.filename) 
        file_path = os.path.join(UPLOAD_DIR, sanitized_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)

        edit_user_data["profile_picture"] = f"/images/{sanitized_filename}"

    current_user.sqlmodel_update(edit_user_data)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
    
@router.post("", response_model=UserPublic)
async def register_new_user(
    session: SessionDep,
    request: Annotated[UserCreate, Form()],
):
    stripped_username = validate_non_empty_string("Username", request.username) 
    existing_user_by_username = session.exec(
        select(User)
        .where(User.username == stripped_username)
    ).first()

    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The username '{stripped_username}' is already taken."
        )

    stripped_email = validate_non_empty_string("Email", request.email)
    existing_user_by_email = session.exec(
        select(User)
        .where(User.email == stripped_email)
    ).first()

    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{stripped_email} is already in use."
        )

    hashed_password = get_password_hash(request.password)

    user_data = request.model_dump()
    user_data["password"] = hashed_password
    user_data["username"] = stripped_username
    user_data["email"] = stripped_email

    if request.profile_picture:
        profile_picture = request.profile_picture

        if not is_jpeg(profile_picture):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile picture must be a JPG or JPEG image."
            )

        sanitized_filename = sanitize_filename(profile_picture.filename) 
        file_path = os.path.join(UPLOAD_DIR, sanitized_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(request.profile_picture.file, buffer)
        
        user_data["profile_picture"] = f"/images/{sanitized_filename}"
        
    new_user = User(**user_data)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user 
