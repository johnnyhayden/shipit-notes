from datetime import datetime
from typing import Optional
from app.models import Note


class InMemoryStorage:
    """In-memory storage for notes using a dictionary."""

    def __init__(self):
        self.notes_store: dict[int, Note] = {}
        self.next_id: int = 1

    def create_note(self, title: str, content: str) -> Note:
        """Create a new note and store it."""
        now = datetime.utcnow()
        note = Note(
            id=self.next_id,
            title=title,
            content=content,
            created_at=now,
            updated_at=now
        )
        self.notes_store[self.next_id] = note
        self.next_id += 1
        return note

    def get_note(self, note_id: int) -> Optional[Note]:
        """Get a note by ID."""
        return self.notes_store.get(note_id)

    def get_all_notes(self) -> list[Note]:
        """Get all notes."""
        return list(self.notes_store.values())

    def update_note(self, note_id: int, title: str, content: str) -> Optional[Note]:
        """Update an existing note."""
        note = self.notes_store.get(note_id)
        if note is None:
            return None

        updated_note = Note(
            id=note.id,
            title=title,
            content=content,
            created_at=note.created_at,
            updated_at=datetime.utcnow()
        )
        self.notes_store[note_id] = updated_note
        return updated_note

    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID. Returns True if deleted, False if not found."""
        if note_id in self.notes_store:
            del self.notes_store[note_id]
            return True
        return False

    def clear(self):
        """Clear all notes (useful for testing)."""
        self.notes_store.clear()
        self.next_id = 1


# Global storage instance
storage = InMemoryStorage()
