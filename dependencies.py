from .database import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

# Create annotated dependency for a database session
SessionDep = Annotated[Session, Depends(get_session)]