from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(default="", max_length=10000, description="Note content")


class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(default="", max_length=10000, description="Note content")


class Note(BaseModel):
    """Note model with all fields including auto-generated ones."""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class NoteListResponse(BaseModel):
    """Response schema for listing notes."""
    notes: list[Note]
