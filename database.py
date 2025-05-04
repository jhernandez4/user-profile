from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import EmailStr 
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, min_length=1, max_length=30)
    password: str= Field(min_length=1)
    email: EmailStr = Field(unique=True, max_length=255)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    birthday: datetime 
    biography: str 
    favorite_number: int 
    profile_picture: str = Field(default="https://i.imgur.com/vIaC7Uq.png")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

MYSQL_URI = os.getenv("MYSQL_URI")
engine = create_engine(MYSQL_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
