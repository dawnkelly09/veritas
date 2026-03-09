from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import os
import re
import json
from pathlib import Path

router = APIRouter()

class GapInfo(BaseModel):
    period_start: str
    period_end: str
    location: str
    severity: str
    acknowledged: bool = False
    reason: Optional[str] = None

class PlannedAbsence(BaseModel):
    start: str
    end: str
    reason: str
    expected_return: str
    active: bool = True

class AcknowledgedGap(BaseModel):
    period_start: str
    period_end: str
    reason: str
    acknowledged_at: str

class BootstrapResponse(BaseModel):
    status: str
    last_known_state: str
    current_time: str
    gaps_found: int
    gaps_acknowledged: int
    gaps: List[GapInfo]
    planned_absences: List[PlannedAbsence]
    primary_locations_checked: List[str]
    fallback_locations_checked: List[str]

class AcknowledgeRequest(BaseModel):
    period_start: str
    period_end: str
    reason: str

class PlannedAbsenceRequest(BaseModel):
    start: str
    end: str
    reason: str
    expected_return: str

# Configuration
PRIMARY_LOCATIONS = [
    "/Users/trinity/.openclaw/workspace/memory/",
    "/Users/trinity/.openclaw/workspace/"
]

FALLBACK_LOCATIONS = [
    "/Users/trinity/Documents/Trinity-Mind/OpenClaw Backup/",
    "/Users/trinity/Desktop/"
]

def get_workspace_path() -> str:
    """Get the workspace path from env or default."""
    return os.environ.get("TRINITY_WORKSPACE", "/Users/trinity/.openclaw/workspace/")

def load_acknowledged_gaps() -> List[AcknowledgedGap]:
    """Load acknowledged gaps from workspace file."""
    workspace = get_workspace_path()
    ack_file = Path(workspace) / "acknowledged-gaps.json"
    
    if not ack_file.exists():
        return []
    
    try:
        with open(ack_file) as f:
            data = json.load(f)
            return [AcknowledgedGap(**g) for g in data.get("acknowledged", [])]
    except Exception as e:
        print(f"Error loading acknowledged gaps: {e}")
        return []

def load_planned_absences() -> List[PlannedAbsence]:
    """Load planned absences from workspace file."""
    workspace = get_workspace_path()
    abs_file = Path(workspace) / "planned-absences.json"
    
    if not abs_file.exists():
        return []
    
    try:
        with open(abs_file) as f:
            data = json.load(f)
            absences = []
            for a in data.get("absences", []):
                # Check if absence is still active
                end = datetime.strptime(a["end"], "%Y-%m-%d")
                a["active"] = end >= datetime.now()
                absences.append(PlannedAbsence(**a))
            return absences
    except Exception as e:
        print(f"Error loading planned absences: {e}")
        return []

def save_acknowledged_gaps(gaps: List[AcknowledgedGap]):
    """Save acknowledged gaps to workspace file."""
    workspace = get_workspace_path()
    ack_file = Path(workspace) / "acknowledged-gaps.json"
    
    try:
        with open(ack_file, "w") as f:
            json.dump({"acknowledged": [g.model_dump() for g in gaps]}, f, indent=2)
    except Exception as e:
        print(f"Error saving acknowledged gaps: {e}")

def save_planned_absences(absences: List[PlannedAbsence]):
    """Save planned absences to workspace file."""
    workspace = get_workspace_path()
    abs_file = Path(workspace) / "planned-absences.json"
    
    try:
        with open(abs_file, "w") as f:
            json.dump({"absences": [a.model_dump() for a in absences]}, f, indent=2)
    except Exception as e:
        print(f"Error saving planned absences: {e}")

def is_gap_acknowledged(gap: GapInfo, acknowledged: List[AcknowledgedGap]) -> bool:
    """Check if a gap has been acknowledged."""
    for ack in acknowledged:
        if ack.period_start == gap.period_start and ack.period_end == gap.period_end:
            return True
    return False

def is_during_planned_absence(gap: GapInfo, absences: List[PlannedAbsence]) -> tuple[bool, Optional[str]]:
    """Check if gap falls within a planned absence. Returns (is_covered, reason)."""
    gap_start = datetime.strptime(gap.period_start, "%Y-%m-%d")
    gap_end = datetime.strptime(gap.period_end, "%Y-%m-%d")
    
    for absence in absences:
        abs_start = datetime.strptime(absence.start, "%Y-%m-%d")
        abs_end = datetime.strptime(absence.end, "%Y-%m-%d")
        
        # Check if gap overlaps with absence
        if gap_start <= abs_end and gap_end >= abs_start:
            return True, absence.reason
    
    return False, None

def scan_daily_notes(directory: str) -> List[datetime]:
    """Scan directory for daily note files (YYYY-MM-DD.md pattern)."""
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
                        continue
    except Exception as e:
        print(f"Error scanning {directory}: {e}")
    
    return sorted(dates)

def detect_gaps(dates: List[datetime]) -> List[GapInfo]:
    """Detect gaps in daily note continuity."""
    if len(dates) < 2:
        return []
    
    gaps = []
    
    for i in range(1, len(dates)):
        prev_date = dates[i-1]
        curr_date = dates[i]
        expected_next = prev_date + timedelta(days=1)
        
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

def check_today_missing(dates: List[datetime]) -> Optional[GapInfo]:
    """Check if today's daily note is missing."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if not dates:
        return None
        
    latest = dates[-1].replace(hour=0, minute=0, second=0, microsecond=0)
    
    if latest < today:
        return GapInfo(
            period_start=latest.strftime("%Y-%m-%d"),
            period_end=today.strftime("%Y-%m-%d"),
            location="workspace/memory/",
            severity="info" if (today - latest).days == 1 else "warning"
        )
    
    return None

@router.get("/", response_model=BootstrapResponse)
async def run_bootstrap():
    """Layer 0: Bootstrap Discovery with acknowledgment support."""
    # Load acknowledgment data
    acknowledged_gaps = load_acknowledged_gaps()
    planned_absences = load_planned_absences()
    
    # Scan for daily notes
    primary_path = PRIMARY_LOCATIONS[0]
    dates_found = scan_daily_notes(primary_path)
    
    # Detect gaps
    gaps = detect_gaps(dates_found)
    
    # Check if today's note is missing
    today_gap = check_today_missing(dates_found)
    if today_gap:
        gaps.append(today_gap)
    
    # Mark acknowledged gaps and check for planned absences
    for gap in gaps:
        if is_gap_acknowledged(gap, acknowledged_gaps):
            gap.acknowledged = True
            gap.reason = "Manually acknowledged"
        else:
            is_planned, reason = is_during_planned_absence(gap, planned_absences)
            if is_planned:
                gap.acknowledged = True
                gap.reason = f"Planned absence: {reason}"
    
    # Count active (non-acknowledged) gaps
    active_gaps = [g for g in gaps if not g.acknowledged]
    acknowledged_count = len([g for g in gaps if g.acknowledged])
    
    # Determine status based on active gaps only
    if not active_gaps:
        status = "clean"
    elif any(g.severity == "critical" for g in active_gaps):
        status = "critical"
    elif any(g.severity == "warning" for g in active_gaps):
        status = "warning"
    else:
        status = "clean"
    
    last_known = dates_found[-1].strftime("%Y-%m-%d %H:%M:%S") if dates_found else "unknown"
    
    return BootstrapResponse(
        status=status,
        last_known_state=last_known,
        current_time=datetime.now().isoformat(),
        gaps_found=len(active_gaps),
        gaps_acknowledged=acknowledged_count,
        gaps=gaps,
        planned_absences=planned_absences,
        primary_locations_checked=PRIMARY_LOCATIONS,
        fallback_locations_checked=FALLBACK_LOCATIONS
    )

@router.post("/acknowledge")
async def acknowledge_gap(request: AcknowledgeRequest):
    """Acknowledge a gap as expected/acceptable."""
    gaps = load_acknowledged_gaps()
    
    # Check if already acknowledged
    for g in gaps:
        if g.period_start == request.period_start and g.period_end == request.period_end:
            return {"acknowledged": True, "message": "Gap already acknowledged"}
    
    # Add new acknowledgment
    new_ack = AcknowledgedGap(
        period_start=request.period_start,
        period_end=request.period_end,
        reason=request.reason,
        acknowledged_at=datetime.now().isoformat()
    )
    gaps.append(new_ack)
    save_acknowledged_gaps(gaps)
    
    return {
        "acknowledged": True,
        "message": f"Gap from {request.period_start} to {request.period_end} acknowledged",
        "reason": request.reason
    }

@router.post("/planned-absence")
async def add_planned_absence(request: PlannedAbsenceRequest):
    """Add a planned absence period."""
    absences = load_planned_absences()
    
    new_absence = PlannedAbsence(
        start=request.start,
        end=request.end,
        reason=request.reason,
        expected_return=request.expected_return,
        active=True
    )
    absences.append(new_absence)
    save_planned_absences(absences)
    
    return {
        "added": True,
        "message": f"Planned absence from {request.start} to {request.end} added",
        "absence": new_absence.model_dump()
    }

@router.delete("/planned-absence/{start_date}")
async def remove_planned_absence(start_date: str):
    """Remove a planned absence by start date."""
    absences = load_planned_absences()
    original_count = len(absences)
    absences = [a for a in absences if a.start != start_date]
    
    if len(absences) == original_count:
        return {"removed": False, "message": f"No planned absence found starting {start_date}"}
    
    save_planned_absences(absences)
    return {"removed": True, "message": f"Planned absence starting {start_date} removed"}

@router.get("/self-report/{period_start}/{period_end}")
async def self_report_gap(period_start: str, period_end: str):
    """Generate a self-report for a detected gap."""
    return {
        "reported": True,
        "message": f"Gap detected: Missing context from {period_start} to {period_end}",
        "recommended_action": "Check backup locations or acknowledge if expected",
        "acknowledge_url": f"/api/bootstrap/acknowledge",
        "timestamp": datetime.now().isoformat()
    }
