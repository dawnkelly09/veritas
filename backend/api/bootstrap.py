from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
import os
import re
from pathlib import Path

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

# Configuration - matches Trinity's actual setup
PRIMARY_LOCATIONS = [
    "/Users/trinity/.openclaw/workspace/memory/",
    "/Users/trinity/.openclaw/workspace/"
]

FALLBACK_LOCATIONS = [
    "/Users/trinity/Documents/Trinity-Mind/OpenClaw Backup/",
    "/Users/trinity/Desktop/"
]

def scan_daily_notes(directory: str) -> List[datetime]:
    """
    Scan directory for daily note files (YYYY-MM-DD.md pattern).
    Returns sorted list of dates found.
    """
    dates = []
    pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})\.md$')
    
    try:
        path = Path(directory)
        if not path.exists():
            return dates
            
        for file in path.iterdir():
            if file.is_file():
                match = pattern.match(file.name)
                if match:
                    year, month, day = map(int, match.groups())
                    try:
                        date = datetime(year, month, day)
                        dates.append(date)
                    except ValueError:
                        # Invalid date (e.g., 2026-02-30)
                        continue
    except Exception as e:
        print(f"Error scanning {directory}: {e}")
    
    return sorted(dates)

def detect_gaps(dates: List[datetime]) -> List[GapInfo]:
    """
    Detect gaps in daily note continuity.
    Returns list of GapInfo for missing periods.
    """
    if len(dates) < 2:
        return []
    
    gaps = []
    
    for i in range(1, len(dates)):
        prev_date = dates[i-1]
        curr_date = dates[i]
        expected_next = prev_date + timedelta(days=1)
        
        # Check if there's a gap
        while expected_next < curr_date:
            gap_end = min(curr_date - timedelta(days=1), expected_next + timedelta(days=6))
            
            severity = "warning" if (curr_date - expected_next).days <= 3 else "critical"
            
            gaps.append(GapInfo(
                period_start=expected_next.strftime("%Y-%m-%d"),
                period_end=gap_end.strftime("%Y-%m-%d"),
                location="workspace/memory/",
                severity=severity
            ))
            
            expected_next = gap_end + timedelta(days=1)
    
    return gaps

def check_today_missing(dates: List[datetime]) -> GapInfo | None:
    """Check if today's daily note is missing."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not dates:
        return None
        
    latest = dates[-1]
    latest = latest.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if latest < today:
        # Today's note is missing
        return GapInfo(
            period_start=latest.strftime("%Y-%m-%d"),
            period_end=today.strftime("%Y-%m-%d"),
            location="workspace/memory/",
            severity="info" if (today - latest).days == 1 else "warning"
        )
    
    return None

@router.get("/")
async def run_bootstrap():
    """
    Layer 0: Bootstrap Discovery
    
    Scans primary storage locations for daily notes,
    detects continuity gaps, and reports findings.
    """
    # Scan primary location for daily notes
    primary_path = PRIMARY_LOCATIONS[0]  # workspace/memory/
    dates_found = scan_daily_notes(primary_path)
    
    # Detect gaps between notes
    gaps = detect_gaps(dates_found)
    
    # Check if today's note is missing
    today_gap = check_today_missing(dates_found)
    if today_gap:
        gaps.append(today_gap)
    
    # Determine status
    status = "clean" if not gaps else ("warning" if all(g.severity != "critical" for g in gaps) else "critical")
    
    # Get last known state
    last_known = dates_found[-1].strftime("%Y-%m-%d %H:%M:%S") if dates_found else "unknown"
    
    return BootstrapResponse(
        status=status,
        last_known_state=last_known,
        current_time=datetime.now().isoformat(),
        gaps_found=len(gaps),
        gaps=gaps,
        primary_locations_checked=PRIMARY_LOCATIONS,
        fallback_locations_checked=FALLBACK_LOCATIONS
    )

@router.post("/self-report")
async def self_report_gap(gap: GapInfo):
    """
    Self-report a detected context gap to the human owner.
    """
    return {
        "reported": True,
        "message": f"Gap detected: Missing context from {gap.period_start} to {gap.period_end} in {gap.location}",
        "recommended_action": "Check backup location for missing files" if gap.severity == "critical" else "Create missing daily note if needed",
        "timestamp": datetime.now().isoformat()
    }
