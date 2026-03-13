"""
Layer 1: Constitution Anchor API

Handles:
- Anchoring constitution to Storacha + Filecoin
- Checking anchoring status
- Verifying constitution integrity
- Managing constitution versions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from core.constitution_anchor import ConstitutionAnchor
from config import get_agent_config, get_veritas_config

router = APIRouter()

# Global anchor instance (initialized on first use)
_anchor_instance: Optional[ConstitutionAnchor] = None

def get_anchor() -> ConstitutionAnchor:
    """Get or initialize the constitution anchor."""
    global _anchor_instance
    if _anchor_instance is None:
        _anchor_instance = ConstitutionAnchor()
        _anchor_instance.initialize()
    return _anchor_instance


class AnchorRequest(BaseModel):
    """Request to anchor a constitution."""
    constitution_path: Optional[str] = None  # Path to constitution file
    version: Optional[str] = None  # Version tag


class AnchorResponse(BaseModel):
    """Response from anchoring operation."""
    success: bool
    cid: str
    transaction_hash: str
    anchor_block: int
    timestamp: str
    agent_id: str
    version: Optional[str] = None
    mock_mode: bool = True  # True if using mock data


class IntegrityStatus(BaseModel):
    """Full integrity status for the dashboard."""
    constitution_anchored: bool
    constitution_cid: Optional[str]
    anchor_block: Optional[int]
    anchor_timestamp: Optional[str]
    anchor_transaction: Optional[str]
    lit_connected: bool
    storacha_connected: bool
    filecoin_connected: bool
    mock_mode: bool
    agent_id: str
    constitution_version: Optional[str] = None


class ConstitutionVersion(BaseModel):
    """A single constitution version."""
    cid: str
    timestamp: str
    version: str
    block_number: Optional[int] = None
    transaction_hash: Optional[str] = None


class VersionHistoryResponse(BaseModel):
    """Response with version history."""
    versions: List[ConstitutionVersion]
    agent_id: str


class VerifyRequest(BaseModel):
    """Request to verify a constitution CID."""
    cid: str


class VerifyResponse(BaseModel):
    """Response from verification."""
    valid: bool
    message: str
    anchor_info: Optional[Dict[str, Any]] = None


def load_constitution_text(path: Optional[str] = None) -> str:
    """Load constitution text from file."""
    if path is None:
        # Default to docs/constitution.md
        config = get_agent_config()
        base_path = Path(__file__).parent.parent.parent / "docs"
        path = base_path / config.constitution_filename
    else:
        path = Path(path)
    
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Constitution not found at {path}")
    
    return path.read_text()


@router.get("/status", response_model=IntegrityStatus)
async def get_integrity_status():
    """Get current Layer 1 integrity status."""
    config = get_veritas_config()
    agent_config = get_agent_config()
    
    try:
        anchor = get_anchor()
        status = anchor.get_constitution_status()
        
        return IntegrityStatus(
            constitution_anchored=status["anchored"],
            constitution_cid=status["cid"],
            anchor_block=status["anchor_block"],
            anchor_timestamp=status["last_updated"],
            anchor_transaction=None,  # Would need to fetch from Filecoin
            lit_connected=status["lit_connected"],
            storacha_connected=status["storacha_connected"],
            filecoin_connected=status["filecoin_connected"],
            mock_mode=config.use_mock_data,
            agent_id=agent_config.agent_id,
            constitution_version="0.1.0"  # TODO: Extract from constitution
        )
    except Exception as e:
        # Return disconnected status if initialization fails
        return IntegrityStatus(
            constitution_anchored=False,
            constitution_cid=None,
            anchor_block=None,
            anchor_timestamp=None,
            anchor_transaction=None,
            lit_connected=False,
            storacha_connected=False,
            filecoin_connected=False,
            mock_mode=config.use_mock_data,
            agent_id=agent_config.agent_id,
            constitution_version=None
        )


@router.post("/anchor", response_model=AnchorResponse)
async def anchor_constitution(request: AnchorRequest):
    """
    Anchor the constitution to Storacha + Filecoin.
    
    This performs the full Layer 1 flow:
    1. Load constitution text
    2. Encrypt with Lit Protocol
    3. Store in Storacha (get CID)
    4. Anchor CID on Filecoin
    """
    config = get_veritas_config()
    
    try:
        # Load constitution
        constitution_text = load_constitution_text(request.constitution_path)
        
        # Get anchor orchestrator
        anchor = get_anchor()
        
        # Perform anchoring
        result = anchor.anchor_constitution(constitution_text)
        
        return AnchorResponse(
            success=result["success"],
            cid=result["cid"],
            transaction_hash=result["transaction_hash"],
            anchor_block=result["anchor_block"],
            timestamp=result["timestamp"],
            agent_id=result["agent_id"],
            version=request.version,
            mock_mode=config.use_mock_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anchoring failed: {str(e)}")


@router.post("/verify", response_model=VerifyResponse)
async def verify_constitution(request: VerifyRequest):
    """
    Verify a constitution CID is properly anchored.
    
    Checks:
    - CID exists on-chain
    - Agent ID matches
    - No tampering detected
    """
    try:
        anchor = get_anchor()
        is_valid, message = anchor.verify_integrity(request.cid)
        
        # Get anchor info if valid
        anchor_info = None
        if is_valid:
            anchor_info = anchor.filecoin.get_anchor(request.cid)
        
        return VerifyResponse(
            valid=is_valid,
            message=message,
            anchor_info=anchor_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@router.get("/versions", response_model=VersionHistoryResponse)
async def get_constitution_versions():
    """Get version history for this agent's constitution."""
    try:
        anchor = get_anchor()
        agent_config = get_agent_config()
        
        # Get history from Filecoin
        history = anchor.filecoin.get_constitution_history(agent_config.agent_id)
        
        versions = [
            ConstitutionVersion(
                cid=h["cid"],
                timestamp=h["timestamp"],
                version=f"0.1.{i}",  # Mock versioning
                block_number=h.get("block"),
                transaction_hash=None
            )
            for i, h in enumerate(reversed(history))
        ]
        
        return VersionHistoryResponse(
            versions=versions,
            agent_id=agent_config.agent_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch versions: {str(e)}")


@router.get("/constitution/current")
async def get_current_constitution():
    """Fetch and decrypt the currently anchored constitution."""
    agent_config = get_agent_config()
    
    if not agent_config.encrypted_constitution_cid:
        raise HTTPException(status_code=404, detail="No constitution anchored yet")
    
    try:
        anchor = get_anchor()
        constitution_text = anchor.fetch_constitution(agent_config.encrypted_constitution_cid)
        
        return {
            "cid": agent_config.encrypted_constitution_cid,
            "constitution": constitution_text,
            "agent_id": agent_config.agent_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch constitution: {str(e)}")
