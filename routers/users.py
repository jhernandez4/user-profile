from typing import Annotated
from fastapi import APIRouter, Depends
from ..dependencies import get_current_user 
from ..database import User
from ..models import UserResponse

router = APIRouter(
    prefix="/users",
    # For FastAPI auto documentation
    tags=["users"]
)

# Dependency Injection for Current User
CurrentUserDep = Annotated[User, Depends(get_current_user)]

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: CurrentUserDep
):
    return current_user
