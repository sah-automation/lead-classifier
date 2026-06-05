from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes.classify import router as classify_router
from routes.leads import router as leads_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup tasks."""
    init_db()
    yield


app = FastAPI(
    title="Lead Classifier API",
    description="API for lead intake, classification, and follow-up suggestions",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for local assignment/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classify_router)
app.include_router(leads_router)


@app.get("/")
def root():
    return {
        "message": "Lead Classifier API is running",
        "docs": "/docs",
    }