from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import status, integrity, bootstrap, anchor
from config import get_veritas_config

app = FastAPI(
    title="Veritas API",
    description="Agent Constitution Protocol backend",
    version="0.1.0"
)

# Load config for CORS origins
veritas_config = get_veritas_config()

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=veritas_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(status.router, prefix="/api/status", tags=["status"])
app.include_router(integrity.router, prefix="/api/integrity", tags=["integrity"])
app.include_router(bootstrap.router, prefix="/api/bootstrap", tags=["bootstrap"])
app.include_router(anchor.router, prefix="/api/anchor", tags=["anchor"])

@app.get("/")
async def root():
    return {
        "name": "Veritas",
        "version": "0.1.0",
        "description": "Agent Constitution Protocol"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
