from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import router as notes_router

# Se crean las tablas
models.Base.metadata.create_all(bind=engine)

#  la aplicación FastAPI
app = FastAPI(
    title="Notes API",
    description="A simple API for managing notes",
    version="0.1.0"
)

# Incluye el router de notas
app.include_router(notes_router, prefix="/api", tags=["notes"]) 

