from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class StatusResponse(BaseModel):
    agent_name: str
    last_memory_write: str
    bootstrap_status: str
    gaps_detected: int
    active_projects: int
    pending_alerts: int
    timestamp: str

@router.get("/", response_model=StatusResponse)
async def get_status():
    """Get current agent status for Trinity Status dashboard"""
    return StatusResponse(
        agent_name="Trinity",
        last_memory_write="2026-02-21 12:37:00",
        bootstrap_status="clean",
        gaps_detected=0,
        active_projects=3,
        pending_alerts=0,
        timestamp=datetime.now().isoformat()
    )
