from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    # For FastAPI auto documentation
    tags=["users"]
)

@router.get("/")
async def get_users():
    return {"message": "Hello users!"}