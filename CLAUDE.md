# Project: ShipIt Notes

## Goals
- Tiny notes app: FastAPI backend + React frontend
- Must have tests + CI + human-reviewed PRs
- Keep it simple; no auth for v1

## Repository Commands

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

### Frontend
```bash
cd frontend
npm install
npm test
npm run build
```

## Code Style
- Prefer small, readable modules
- Add type hints/annotations where practical
- No giant PRs: keep changes scoped to acceptance criteria

## PR Etiquette
- Every PR must reference an issue
- Must include tests or explicit "no tests needed" rationale
- Must pass CI before review
- Use conventional commit format