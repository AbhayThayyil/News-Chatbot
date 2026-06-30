# AI News Chatbot

A conversational AI assistant that answers natural language questions about the latest news by retrieving real-time articles and summarizing them with an LLM, with citations.

## Stack

- **Frontend**: React, TypeScript, Vite, MUI, React Query, React Router, Axios
- **Backend**: FastAPI, Python, SQLAlchemy, httpx

## Getting Started

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173, backend at http://localhost:8000.
