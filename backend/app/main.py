from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routers import deviations, data

# Create tables if they don't exist (expects schema.sql executed already; this is a safety net)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LIMS Deviation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deviations.router)
app.include_router(data.router)

@app.get("/health")
def health():
    return {"ok": True}
