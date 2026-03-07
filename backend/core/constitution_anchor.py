"""
Layer 1: Constitution Anchor Orchestrator

Coordinates the three sponsor technologies:
1. Lit Protocol → Encrypt/decrypt constitution
2. Storacha → Store encrypted constitution (CID)
3. Filecoin → Anchor CID on-chain

This is the core of Veritas — immutable, verifiable agent constitution.

FLOW:
    Upload: Constitution → Lit encrypt → Storacha store → Filecoin anchor
    Download: Filecoin verify → Storacha fetch → Lit decrypt → Constitution
"""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime

from backend.core.lit_client import LitClient
from backend.core.storacha_client import StorachaClient
from backend.core.filecoin_client import FilecoinClient
from backend.config import get_agent_config


class ConstitutionAnchor:
    """
    Orchestrates the full Layer 1 flow for constitution anchoring.
    
    This is what makes the constitution:
    - Encrypted (Lit Protocol)
    - Content-addressed (Storacha/IPFS)
    - On-chain anchored (Filecoin)
    """
    
    def __init__(self):
        self.lit = LitClient()
        self.storacha = StorachaClient()
        self.filecoin = FilecoinClient()
        self.agent_config = get_agent_config()
        
        self._initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize all three sponsor connections.
        
        Must be called before any anchor operations.
        """
        try:
            self.lit.authenticate()
            self.storacha.authenticate()
            self.filecoin.connect()
            self._initialized = True
            return True
        except Exception as e:
            print(f"Layer 1 initialization failed: {e}")
            return False
    
    def anchor_constitution(self, constitution_text: str) -> Dict[str, Any]:
        """
        Full flow: Encrypt → Store → Anchor
        
        Args:
            constitution_text: Raw constitution markdown
            
        Returns:
            {
                "success": True,
                "cid": "Qm...",
                "transaction_hash": "0x...",
                "anchor_block": 3847291,
                "timestamp": "2026-02-24T13:30:00Z"
            }
            
        Raises:
            RuntimeError: If not initialized or any step fails
        """
        if not self._initialized:
            raise RuntimeError("Must call initialize() first")
        
        agent_id = self.agent_config.agent_id
        
        # Step 1: Encrypt with Lit Protocol
        print("\n[Layer 1] Step 1: Encrypting constitution...")
        encrypted = self.lit.encrypt_constitution(constitution_text, agent_id)
        
        # Step 2: Store in Storacha, get CID
        print("[Layer 1] Step 2: Storing in Storacha...")
        cid = self.storacha.upload_constitution(encrypted, agent_id)
        
        # Step 3: Anchor CID on Filecoin
        print("[Layer 1] Step 3: Anchoring on Filecoin...")
        tx_hash = self.filecoin.anchor_constitution(cid, agent_id)
        
        # Get anchor details
        anchor_info = self.filecoin.get_anchor(cid)
        
        result = {
            "success": True,
            "cid": cid,
            "transaction_hash": tx_hash,
            "anchor_block": anchor_info["block_number"],
            "timestamp": anchor_info["timestamp"],
            "agent_id": agent_id
        }
        
        print(f"\n[Layer 1] Constitution anchored successfully!")
        print(f"  CID: {cid}")
        print(f"  Block: {result['anchor_block']}")
        print(f"  Tx: {tx_hash}")
        
        return result
    
    def fetch_constitution(self, cid: str) -> str:
        """
        Full flow: Verify → Fetch → Decrypt
        
        Args:
            cid: Content identifier from anchor
            
        Returns:
            Decrypted constitution text
            
        Raises:
            RuntimeError: If verification fails or any step fails
        """
        if not self._initialized:
            raise RuntimeError("Must call initialize() first")
        
        agent_id = self.agent_config.agent_id
        
        # Step 1: Verify on-chain anchoring
        print(f"\n[Layer 1] Step 1: Verifying anchor for CID {cid[:20]}...")
        if not self.filecoin.verify_constitution(cid):
            raise RuntimeError("Constitution CID not found on-chain! Possible tampering.")
        
        # Step 2: Fetch from Storacha
        print("[Layer 1] Step 2: Fetching from Storacha...")
        encrypted = self.storacha.download_constitution(cid)
        
        # Step 3: Decrypt with Lit
        print("[Layer 1] Step 3: Decrypting with Lit...")
        constitution = self.lit.decrypt_constitution(encrypted, agent_id)
        
        print("[Layer 1] Constitution retrieved successfully!")
        return constitution
    
    def get_constitution_status(self) -> Dict[str, Any]:
        """
        Get current anchoring status.
        
        Returns:
            {
                "anchored": bool,
                "cid": str or None,
                "anchor_block": int or None,
                "last_updated": str or None,
                "lit_connected": bool,
                "storacha_connected": bool,
                "filecoin_connected": bool
            }
        """
        return {
            "anchored": self.agent_config.encrypted_constitution_cid is not None,
            "cid": self.agent_config.encrypted_constitution_cid,
            "anchor_block": None,  # Would fetch from Filecoin
            "last_updated": None,  # Would fetch from Filecoin
            "lit_connected": self.lit.authenticated if self._initialized else False,
            "storacha_connected": self.storacha.authenticated if self._initialized else False,
            "filecoin_connected": self.filecoin.connected if self._initialized else False
        }
    
    def verify_integrity(self, expected_cid: str) -> Tuple[bool, str]:
        """
        Verify constitution integrity against expected CID.
        
        This is the core security check:
        - Is the CID anchored on-chain?
        - Does the on-chain record match our expectations?
        
        Returns:
            (is_valid, message)
        """
        if not self._initialized:
            return False, "Layer 1 not initialized"
        
        anchor = self.filecoin.get_anchor(expected_cid)
        
        if anchor is None:
            return False, f"CID {expected_cid[:20]}... not found on-chain!"
        
        if anchor["agent_id"] != self.agent_config.agent_id:
            return False, f"Agent ID mismatch! Expected {self.agent_config.agent_id}, got {anchor['agent_id']}"
        
        return True, f"Verified at block {anchor['block_number']}"
