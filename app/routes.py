from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .models import Note
from .schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter()

@router.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    """
    Obtiene todas las notas activas.
    """
    notes = db.query(Note).filter(Note.is_active == True).all()
    return notes

@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una nota específica por su ID.
    Lanza 404 si la nota no existe o no está activa.
    """
    note = db.query(Note).filter(Note.id == note_id, Note.is_active == True).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva nota.
    Retorna la nota creada con todos sus campos.
    """
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una nota existente.
    Solo actualiza los campos proporcionados.
    Lanza 404 si la nota no existe o no está activa.
    """
    db_note = db.query(Note).filter(Note.id == note_id, Note.is_active == True).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Realiza un soft delete de una nota.
    Marca la nota como inactiva en lugar de eliminarla.
    Lanza 404 si la nota no existe o ya está inactiva.
    """
    db_note = db.query(Note).filter(Note.id == note_id, Note.is_active == True).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.is_active = False
    db.commit()
    return None