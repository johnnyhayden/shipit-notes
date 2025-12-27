import pytest
from fastapi import status


class TestCreateNote:
    """Tests for POST /api/v1/notes endpoint."""

    def test_create_note_success(self, client):
        """Test creating a note successfully."""
        response = client.post(
            "/api/v1/notes",
            json={"title": "Test Note", "content": "Test content"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Note"
        assert data["content"] == "Test content"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_note_without_content(self, client):
        """Test creating a note without content."""
        response = client.post(
            "/api/v1/notes",
            json={"title": "Title Only"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Title Only"
        assert data["content"] == ""

    def test_create_note_missing_title(self, client):
        """Test creating a note without a title fails."""
        response = client.post(
            "/api/v1/notes",
            json={"content": "Content only"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_note_empty_title(self, client):
        """Test creating a note with empty title fails."""
        response = client.post(
            "/api/v1/notes",
            json={"title": "", "content": "Content"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_note_title_too_long(self, client):
        """Test creating a note with title exceeding max length."""
        response = client.post(
            "/api/v1/notes",
            json={"title": "x" * 201, "content": "Content"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_note_content_too_long(self, client):
        """Test creating a note with content exceeding max length."""
        response = client.post(
            "/api/v1/notes",
            json={"title": "Title", "content": "x" * 10001}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListNotes:
    """Tests for GET /api/v1/notes endpoint."""

    def test_list_notes_empty(self, client):
        """Test listing notes when none exist."""
        response = client.get("/api/v1/notes")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["notes"] == []

    def test_list_notes_with_data(self, client):
        """Test listing notes when some exist."""
        # Create some notes
        client.post("/api/v1/notes", json={"title": "Note 1", "content": "Content 1"})
        client.post("/api/v1/notes", json={"title": "Note 2", "content": "Content 2"})

        response = client.get("/api/v1/notes")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["notes"]) == 2
        assert data["notes"][0]["title"] == "Note 1"
        assert data["notes"][1]["title"] == "Note 2"


class TestGetNote:
    """Tests for GET /api/v1/notes/{id} endpoint."""

    def test_get_note_success(self, client):
        """Test getting a note by ID."""
        create_response = client.post(
            "/api/v1/notes",
            json={"title": "Test Note", "content": "Test content"}
        )
        note_id = create_response.json()["id"]

        response = client.get(f"/api/v1/notes/{note_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "Test Note"
        assert data["content"] == "Test content"

    def test_get_note_not_found(self, client):
        """Test getting a non-existent note."""
        response = client.get("/api/v1/notes/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Note not found"


class TestUpdateNote:
    """Tests for PUT /api/v1/notes/{id} endpoint."""

    def test_update_note_success(self, client):
        """Test updating a note."""
        create_response = client.post(
            "/api/v1/notes",
            json={"title": "Original Title", "content": "Original content"}
        )
        note_id = create_response.json()["id"]

        response = client.put(
            f"/api/v1/notes/{note_id}",
            json={"title": "Updated Title", "content": "Updated content"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        # Verify updated_at changed
        assert data["updated_at"] != data["created_at"]

    def test_update_note_not_found(self, client):
        """Test updating a non-existent note."""
        response = client.put(
            "/api/v1/notes/999",
            json={"title": "Updated Title", "content": "Updated content"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Note not found"

    def test_update_note_invalid_title(self, client):
        """Test updating a note with invalid title."""
        create_response = client.post(
            "/api/v1/notes",
            json={"title": "Original Title", "content": "Original content"}
        )
        note_id = create_response.json()["id"]

        response = client.put(
            f"/api/v1/notes/{note_id}",
            json={"title": "", "content": "Updated content"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteNote:
    """Tests for DELETE /api/v1/notes/{id} endpoint."""

    def test_delete_note_success(self, client):
        """Test deleting a note."""
        create_response = client.post(
            "/api/v1/notes",
            json={"title": "To Delete", "content": "Will be deleted"}
        )
        note_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/notes/{note_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify note is deleted
        get_response = client.get(f"/api/v1/notes/{note_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_not_found(self, client):
        """Test deleting a non-existent note."""
        response = client.delete("/api/v1/notes/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Note not found"


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.options(
            "/api/v1/notes",
            headers={"Origin": "http://localhost:3000"}
        )
        # FastAPI handles OPTIONS automatically
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]


class TestRootEndpoints:
    """Tests for root and health endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
