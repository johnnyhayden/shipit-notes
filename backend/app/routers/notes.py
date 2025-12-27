from fastapi import APIRouter, HTTPException, status
from app.models import Note, NoteCreate, NoteUpdate, NoteListResponse
from app.storage import storage

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note_data: NoteCreate):
    """Create a new note."""
    note = storage.create_note(title=note_data.title, content=note_data.content)
    return note


@router.get("", response_model=NoteListResponse)
def list_notes():
    """Get all notes."""
    notes = storage.get_all_notes()
    return NoteListResponse(notes=notes)


@router.get("/{note_id}", response_model=Note)
def get_note(note_id: int):
    """Get a single note by ID."""
    note = storage.get_note(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(note_id: int, note_data: NoteUpdate):
    """Update an existing note."""
    note = storage.update_note(note_id, title=note_data.title, content=note_data.content)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int):
    """Delete a note."""
    deleted = storage.delete_note(note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
