# ShipIt Notes Architecture

## Overview

ShipIt Notes is a minimal notes application built with a FastAPI backend and React frontend. The architecture prioritizes simplicity and rapid development for v1, with no authentication layer.

## System Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  React Frontend │ <──────>│ FastAPI Backend │
│   (Port 3000)   │  HTTP   │   (Port 8000)   │
└─────────────────┘         └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   SQLite DB     │
                            │  (notes.db)     │
                            └─────────────────┘
```

## Technology Choices

### Backend: FastAPI
- **Why**: Modern, fast Python web framework with automatic API documentation
- **Benefits**: Built-in OpenAPI/Swagger docs, type hints, async support
- **Trade-offs**: Python ecosystem vs Node.js; acceptable for simple CRUD operations

### Frontend: React
- **Why**: Industry-standard UI library with excellent ecosystem
- **Benefits**: Component reusability, strong typing with TypeScript, rich tooling
- **Trade-offs**: Requires build step; worth it for maintainability

### Database: SQLite
- **Why**: Zero-configuration, file-based database perfect for v1
- **Benefits**: No separate DB server, simple backup/restore, sufficient for single-user or low-traffic scenarios
- **Trade-offs**: Not suitable for high concurrency; can migrate to PostgreSQL later if needed

### ORM: SQLAlchemy (Backend)
- **Why**: Standard Python ORM with excellent FastAPI integration
- **Benefits**: Type-safe queries, migration support via Alembic, easy to test

## Data Models

### Note
```python
{
  "id": int,              # Auto-incrementing primary key
  "title": str,           # Note title (required, max 200 chars)
  "content": str,         # Note content (optional, text field)
  "created_at": datetime, # Auto-generated timestamp
  "updated_at": datetime  # Auto-updated timestamp
}
```

### Validation Rules
- `title`: Required, 1-200 characters
- `content`: Optional, max 10,000 characters
- Timestamps are managed by the database

## REST API Contract

Base URL: `http://localhost:8000/api/v1`

### Endpoints

#### 1. List All Notes
```
GET /notes
```

**Response 200:**
```json
{
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "This is the content",
      "created_at": "2025-12-27T10:00:00Z",
      "updated_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

#### 2. Get Single Note
```
GET /notes/{id}
```

**Response 200:**
```json
{
  "id": 1,
  "title": "My First Note",
  "content": "This is the content",
  "created_at": "2025-12-27T10:00:00Z",
  "updated_at": "2025-12-27T10:00:00Z"
}
```

**Response 404:**
```json
{
  "detail": "Note not found"
}
```

#### 3. Create Note
```
POST /notes
```

**Request Body:**
```json
{
  "title": "New Note",
  "content": "Optional content"
}
```

**Response 201:**
```json
{
  "id": 2,
  "title": "New Note",
  "content": "Optional content",
  "created_at": "2025-12-27T10:05:00Z",
  "updated_at": "2025-12-27T10:05:00Z"
}
```

**Response 422:** Validation error (e.g., missing title, title too long)

#### 4. Update Note
```
PUT /notes/{id}
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Response 200:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content",
  "created_at": "2025-12-27T10:00:00Z",
  "updated_at": "2025-12-27T10:10:00Z"
}
```

**Response 404:** Note not found

#### 5. Delete Note
```
DELETE /notes/{id}
```

**Response 204:** No content (success)

**Response 404:** Note not found

### CORS Configuration
- Allow frontend origin: `http://localhost:3000`
- Methods: GET, POST, PUT, DELETE, OPTIONS
- Headers: Content-Type, Authorization (for future auth)

## Folder Structure

```
shipit-notes/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas for validation
│   │   ├── database.py          # Database connection/session
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── notes.py         # Notes CRUD endpoints
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures
│   │   └── test_notes.py        # Notes endpoint tests
│   ├── requirements.txt         # Python dependencies
│   ├── .venv/                   # Virtual environment (gitignored)
│   └── notes.db                 # SQLite database (gitignored)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── NoteList.tsx     # Display all notes
│   │   │   ├── NoteForm.tsx     # Create/edit note form
│   │   │   └── NoteItem.tsx     # Single note display
│   │   ├── services/
│   │   │   └── api.ts           # API client for backend
│   │   ├── types/
│   │   │   └── note.ts          # TypeScript interfaces
│   │   ├── App.tsx              # Main app component
│   │   └── index.tsx            # React entry point
│   ├── package.json
│   ├── tsconfig.json
│   └── node_modules/            # (gitignored)
│
├── docs/
│   └── ARCHITECTURE.md          # This file
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI
│
├── CLAUDE.md                    # Project instructions for Claude
└── README.md                    # Project documentation
```

## Development Workflow

### Backend Development
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # Start dev server
pytest                          # Run tests
```

### Frontend Development
```bash
cd frontend
npm install
npm start      # Start dev server
npm test       # Run tests
npm run build  # Production build
```

## Key Architectural Decisions

### 1. No Authentication in v1
**Decision**: Skip user authentication for initial release.

**Rationale**:
- Reduces complexity significantly
- Faster time to market
- Single-user or demo use case is acceptable for v1
- Can add auth layer later without major refactoring

**Future**: Add JWT-based authentication in v2 when needed.

### 2. SQLite for Data Persistence
**Decision**: Use SQLite instead of PostgreSQL or MySQL.

**Rationale**:
- Zero configuration overhead
- Perfect for development and small-scale deployment
- Easy to backup (single file)
- Sufficient for expected v1 load

**Migration Path**: When scaling needs arise, SQLAlchemy makes it easy to switch to PostgreSQL.

### 3. Monorepo Structure
**Decision**: Keep backend and frontend in the same repository.

**Rationale**:
- Simpler project management
- Easier to coordinate API changes
- Single CI pipeline
- Appropriate for team size and scope

### 4. REST over GraphQL
**Decision**: Use REST API instead of GraphQL.

**Rationale**:
- Simpler to implement and understand
- CRUD operations map naturally to REST
- No need for complex querying in v1
- FastAPI provides excellent REST support

### 5. TypeScript for Frontend
**Decision**: Use TypeScript instead of JavaScript.

**Rationale**:
- Type safety reduces bugs
- Better IDE support
- Easier refactoring
- Aligns with backend type hints philosophy

## Testing Strategy

### Backend
- **Unit Tests**: Test individual functions and models
- **Integration Tests**: Test API endpoints with test database
- **Coverage Target**: >80% for critical paths

### Frontend
- **Component Tests**: Test React components in isolation
- **Integration Tests**: Test user workflows
- **Tools**: Jest + React Testing Library

### CI/CD
- Run all tests on every PR
- Block merge if tests fail
- Optional: Deploy previews for frontend

## Security Considerations (for v1)

Since v1 has no authentication:
- **Input Validation**: Strict validation on all inputs (Pydantic handles this)
- **SQL Injection**: SQLAlchemy ORM prevents this by default
- **XSS Prevention**: React escapes output by default
- **CORS**: Restrict to known frontend origin
- **Rate Limiting**: Not implemented in v1, add if abuse occurs

**Important**: This app should NOT be deployed to public internet in v1 without authentication.

## Future Enhancements (Post-v1)

1. **User Authentication**: JWT-based auth with user accounts
2. **Note Sharing**: Share notes via public links
3. **Rich Text Editor**: Markdown or WYSIWYG support
4. **Tags/Categories**: Organize notes with tags
5. **Search**: Full-text search across notes
6. **Database Migration**: Move to PostgreSQL if needed
7. **Deployment**: Docker containers, cloud hosting

## API Versioning

Currently using `/api/v1` prefix to allow future API changes without breaking clients.

When breaking changes are needed:
- Create `/api/v2` with new endpoints
- Deprecate v1 with sunset timeline
- Update frontend to use v2

## Error Handling

### Backend
- Use FastAPI's HTTPException for standard errors
- Return consistent error format:
```json
{
  "detail": "Human-readable error message"
}
```

### Frontend
- Display user-friendly error messages
- Log errors to console for debugging
- Handle network failures gracefully

## Performance Considerations

For v1, performance is not a primary concern given the simple use case. However:

- **Backend**: FastAPI is async-capable for future optimization
- **Frontend**: Code splitting if bundle size becomes an issue
- **Database**: Add indexes if queries slow down (e.g., on created_at for sorting)

Current architecture can handle thousands of notes without issues.
