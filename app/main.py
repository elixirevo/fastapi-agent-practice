from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.api.router import api_router
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Backend with LangGraph and Tavily Search",
    lifespan=lifespan,
)

# Include main router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!", "docs": "/docs"}
