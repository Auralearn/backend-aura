from fastapi import FastAPI

from app.routes.interacts import router as interacts_router
from app.routes.materials import router as materials_router

from app.core.config import settings

app = FastAPI(
    title="AuraLearn API",
    description="Backend API for AuraLearn Application",
    version="0.1.0",
)

app.include_router(interacts_router, prefix="/api")
app.include_router(materials_router, prefix="/api")
