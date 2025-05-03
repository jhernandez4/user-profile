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
    uername: str = Field(unique=True, index=True)
    password: str 
    email: EmailStr = Field(unique=True)
    first_name: str 
    last_name: str 
    birthday: datetime 
    biography: str 
    favorite_number: int 
    profile_picture: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

MYSQL_URI = os.getenv("MYSQL_URI")
engine = create_engine(MYSQL_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
