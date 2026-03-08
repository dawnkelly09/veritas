"""
Veritas Configuration Loader

Loads environment variables and provides typed configuration objects.
All sensitive values come from .env file (never committed).
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, Field


class LitProtocolConfig(BaseSettings):
    """Lit Protocol (Vincent) configuration for key management and encryption."""
    
    network: str = Field(default="nagaDev", env="LIT_NETWORK")
    wallet_address: str = Field(..., env="WALLET_ADDRESS")
    wallet_private_key: str = Field(..., env="WALLET_PRIVATE_KEY")
    
    class Config:
        env_file = ".env"


class StorachaConfig(BaseSettings):
    """Storacha UCAN-based storage configuration."""
    
    email: str = Field(..., env="STORACHA_EMAIL")
    space_did: str = Field(..., env="STORACHA_SPACE_DID")
    delegation_proof: Optional[str] = Field(None, env="STORACHA_DELEGATION_PROOF")
    
    class Config:
        env_file = ".env"


class FilecoinConfig(BaseSettings):
    """Filecoin on-chain anchoring configuration."""
    
    wallet_address: str = Field(..., env="FILECOIN_WALLET_ADDRESS")
    rpc_url: str = Field(default="https://api.node.glif.io/rpc/v1", env="FILECOIN_RPC_URL")
    anchor_contract: Optional[str] = Field(None, env="FILECOIN_ANCHOR_CONTRACT")
    
    class Config:
        env_file = ".env"


class AgentConfig(BaseSettings):
    """Agent identity and bootstrap configuration."""
    
    name: str = Field(default="Trinity", env="AGENT_NAME")
    agent_id: str = Field(..., env="AGENT_ID")
    human_owner: str = Field(..., env="HUMAN_OWNER")
    
    # Bootstrap locations (comma-separated in env)
    primary_locations: List[str] = Field(default_factory=list)
    fallback_locations: List[str] = Field(default_factory=list)
    
    # Constitution
    constitution_filename: str = Field(default="constitution.md", env="CONSTITUTION_FILENAME")
    encrypted_constitution_cid: Optional[str] = Field(None, env="ENCRYPTED_CONSTITUTION_CID")
    
    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse comma-separated locations
        # Default: Workspace is primary, Obsidian is interface/backup only
        primary = os.getenv("BOOTSTRAP_PRIMARY_LOCATIONS", "/Users/trinity/.openclaw/workspace/memory/")
        fallback = os.getenv("BOOTSTRAP_FALLBACK_LOCATIONS", "/Users/trinity/Documents/Trinity-Mind/OpenClaw Backup/")
        self.primary_locations = [p.strip() for p in primary.split(",") if p.strip()]
        self.fallback_locations = [p.strip() for p in fallback.split(",") if p.strip()]


class GuardianConfig(BaseSettings):
    """Guardian injection detection thresholds."""
    
    block_threshold: float = Field(default=0.8, env="GUARDIAN_BLOCK_THRESHOLD")
    alert_threshold: float = Field(default=0.5, env="GUARDIAN_ALERT_THRESHOLD")
    
    class Config:
        env_file = ".env"


class ValidatorConfig(BaseSettings):
    """Internal Validator configuration."""
    
    violation_action: str = Field(default="alert", env="VALIDATOR_VIOLATION_ACTION")
    
    class Config:
        env_file = ".env"


class VeritasConfig(BaseSettings):
    """Master configuration container."""
    
    # Backend settings
    backend_host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(default=8000, env="BACKEND_PORT")
    backend_reload: bool = Field(default=True, env="BACKEND_RELOAD")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    log_level: str = Field(default="info", env="LOG_LEVEL")
    
    # Development flags
    use_mock_data: bool = Field(default=False, env="USE_MOCK_DATA")
    debug_lit: bool = Field(default=False, env="DEBUG_LIT")
    debug_storacha: bool = Field(default=False, env="DEBUG_STORACHA")
    debug_filecoin: bool = Field(default=False, env="DEBUG_FILECOIN")
    
    class Config:
        env_file = ".env"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
        self.cors_origins = [o.strip() for o in origins.split(",") if o.strip()]


# Global config instances (lazy-loaded)
_lit_config: Optional[LitProtocolConfig] = None
_storacha_config: Optional[StorachaConfig] = None
_filecoin_config: Optional[FilecoinConfig] = None
_agent_config: Optional[AgentConfig] = None
_guardian_config: Optional[GuardianConfig] = None
_validator_config: Optional[ValidatorConfig] = None
_veritas_config: Optional[VeritasConfig] = None


def get_lit_config() -> LitProtocolConfig:
    """Get Lit Protocol configuration."""
    global _lit_config
    if _lit_config is None:
        _lit_config = LitProtocolConfig()
    return _lit_config


def get_storacha_config() -> StorachaConfig:
    """Get Storacha configuration."""
    global _storacha_config
    if _storacha_config is None:
        _storacha_config = StorachaConfig()
    return _storacha_config


def get_filecoin_config() -> FilecoinConfig:
    """Get Filecoin configuration."""
    global _filecoin_config
    if _filecoin_config is None:
        _filecoin_config = FilecoinConfig()
    return _filecoin_config


def get_agent_config() -> AgentConfig:
    """Get Agent configuration."""
    global _agent_config
    if _agent_config is None:
        _agent_config = AgentConfig()
    return _agent_config


def get_guardian_config() -> GuardianConfig:
    """Get Guardian configuration."""
    global _guardian_config
    if _guardian_config is None:
        _guardian_config = GuardianConfig()
    return _guardian_config


def get_validator_config() -> ValidatorConfig:
    """Get Validator configuration."""
    global _validator_config
    if _validator_config is None:
        _validator_config = ValidatorConfig()
    return _validator_config


def get_veritas_config() -> VeritasConfig:
    """Get Veritas backend configuration."""
    global _veritas_config
    if _veritas_config is None:
        _veritas_config = VeritasConfig()
    return _veritas_config


def check_env_file() -> bool:
    """Check if .env file exists in project root."""
    env_path = Path(__file__).parent.parent / ".env"
    return env_path.exists()
