from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema para crear una nota
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Título de la nota")
    content: str = Field(description="Contenido de la nota")

# Schema para actualizar una nota
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Título de la nota")
    content: Optional[str] = Field(None, description="Contenido de la nota")

# Schema para respuesta
class NoteResponse(BaseModel):
    id: int = Field(description="ID único de la nota")
    title: str = Field(description="Título de la nota")
    content: str = Field(description="Contenido de la nota")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")
    is_active: bool = Field(default=True, description="Estado de la nota")

    class Config:
        from_attributes = True