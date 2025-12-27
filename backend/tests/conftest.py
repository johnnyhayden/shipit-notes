import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import storage


@pytest.fixture
def client():
    """Create a test client with clean storage."""
    storage.clear()
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    """Clean storage before each test."""
    storage.clear()
    yield
    storage.clear()
