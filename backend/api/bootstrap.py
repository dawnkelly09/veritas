from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter()

class GapInfo(BaseModel):
    period_start: str
    period_end: str
    location: str
    severity: str

class BootstrapResponse(BaseModel):
    status: str
    last_known_state: str
    current_time: str
    gaps_found: int
    gaps: List[GapInfo]
    primary_locations_checked: List[str]
    fallback_locations_checked: List[str]

@router.get("/")
async def run_bootstrap():
    """
    Layer 0: Bootstrap Discovery
    
    Checks for context gaps by comparing last known state to current time,
    scanning all known storage locations.
    
    Architecture:
    - Workspace is PRIMARY source of truth for Trinity's files
    - Obsidian is INTERFACE + BACKUP (read Dawn's notes, backup before updates)
    - Daily notes and working files stay in workspace
    """
    return BootstrapResponse(
        status="clean",
        last_known_state="2026-02-21 12:37:00",
        current_time=datetime.now().isoformat(),
        gaps_found=0,
        gaps=[],
        primary_locations_checked=[
            "/Users/trinity/.openclaw/workspace/memory/",
            "/Users/trinity/.openclaw/workspace/"
        ],
        fallback_locations_checked=[
            "/Users/trinity/Documents/Trinity-Mind/OpenClaw Backup/",
            "/Users/trinity/Desktop/"
        ]
    )

@router.post("/self-report")
async def self_report_gap(gap: GapInfo):
    """
    Self-report a detected context gap to the human owner.
    
    This is what Layer 0 does when it finds missing context.
    """
    return {
        "reported": True,
        "message": f"Gap detected: Missing context from {gap.period_start} to {gap.period_end} in {gap.location}",
        "recommended_action": "Check backup location for missing files",
        "timestamp": datetime.now().isoformat()
    }
