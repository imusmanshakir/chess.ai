# Chess AI

A chess platform foundation with a React frontend and Python chess engine.

## Run locally

Install backend dependencies once:

```bash
.venv/bin/python -m pip install -r backend/requirements.txt
```

Start the API from the repository root:

```bash
.venv/bin/python -m uvicorn backend.main:app --reload
```

In a second terminal, start the frontend:

```bash
cd frontend
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

The frontend creates a game through FastAPI and asks the Python engine for legal moves. Game state is currently stored in memory, so restarting the API resets all games.

## API endpoints

- `POST /api/games` — create a new game
- `GET /api/games/{game_id}` — fetch game state
- `GET /api/games/{game_id}/legal-moves?from_square=e2` — legal destinations for a square
- `POST /api/games/{game_id}/moves` — submit a move

## Verification

```bash
.venv/bin/python -m compileall -q backend
cd frontend && npm run build && npm run lint
```
