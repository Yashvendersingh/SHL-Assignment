from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.agent import init_gemini, handle_chat
from app.catalog import load_catalog
from app.models import ChatRequest, ChatResponse, HealthResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_catalog()
    init_gemini()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="SHL Assessment Advisor API",
    description="Conversational API for SHL assessment recommendations",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await handle_chat([m.model_dump() for m in request.messages])

@app.get("/", response_class=HTMLResponse)
async def serve_client():
    client_path = Path(__file__).resolve().parent.parent / "client.html"
    return HTMLResponse(content=client_path.read_text(encoding="utf-8"))
