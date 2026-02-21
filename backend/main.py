from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import status, integrity, bootstrap

app = FastAPI(
    title="Veritas API",
    description="Agent Constitution Protocol backend",
    version="0.1.0"
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(status.router, prefix="/api/status", tags=["status"])
app.include_router(integrity.router, prefix="/api/integrity", tags=["integrity"])
app.include_router(bootstrap.router, prefix="/api/bootstrap", tags=["bootstrap"])

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
