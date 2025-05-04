from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import create_db_and_tables
from .routers import users
import os

app = FastAPI()

app.include_router(users.router)
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}