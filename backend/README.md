# Backend API

FastAPI backend for the LED subway board.

## Local Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/config
curl http://127.0.0.1:8000/api/board
```

## Render Web Service

Create a **Web Service** from this repo.

Recommended settings:

```text
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

The frontend should use:

```text
VITE_API_BASE_URL=https://your-render-service.onrender.com
```

## Endpoints

```text
GET  /health
GET  /api/config
POST /api/config
POST /api/reset
GET  /api/board
```

`/api/board` returns the small JSON payload the LED panel should poll.
