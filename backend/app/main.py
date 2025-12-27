from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import notes

app = FastAPI(
    title="ShipIt Notes API",
    description="Simple notes API with in-memory storage",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include routers
app.include_router(notes.router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "ShipIt Notes API", "version": "1.0.0"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
