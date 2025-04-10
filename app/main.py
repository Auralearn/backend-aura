from fastapi import FastAPI
from app.routes.interacts import router as interacts_router

app = FastAPI()

app.include_router(interacts_router, prefix="/api")