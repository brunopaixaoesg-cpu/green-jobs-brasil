"""
Green Jobs Brasil - ETL Configuration
Manages environment variables and configuration settings for the ETL pipeline.
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ETLConfig:
    """Configuration class for ETL pipeline settings."""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/gjb_db")
    
    # Target states for processing
    TARGET_UFS: List[str] = os.getenv("TARGET_UFS", "MG,RJ,SP").split(",")
    
    # Data directories
    RAW_DIR: Path = Path(os.getenv("RAW_DIR", "data/raw"))
    PROCESSED_DIR: Path = Path(os.getenv("PROCESSED_DIR", "data/processed"))
    
    # RFB dataset files
    CNPJ_FILE: str = os.getenv("CNPJ_FILE", "Empresas*.EMPRECSV")
    ESTABELECIMENTOS_FILE: str = os.getenv("ESTABELECIMENTOS_FILE", "Estabelecimentos*.ESTABCSV")
    
    # Processing settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "10000"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    
    # Green CNAE seed file
    CNAE_GREEN_SEED: Path = Path("etl/cnae_green_seed.csv")
    
    # Logging level
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Backup and archive settings
    BACKUP_ENABLED: bool = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    ARCHIVE_DAYS: int = int(os.getenv("ARCHIVE_DAYS", "30"))
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.RAW_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for processed data partitioning
        for uf in cls.TARGET_UFS:
            (cls.PROCESSED_DIR / uf.strip()).mkdir(exist_ok=True)
    
    @classmethod
    def get_database_params(cls) -> dict:
        """Extract database connection parameters from DATABASE_URL."""
        import urllib.parse as urlparse
        
        parsed = urlparse.urlparse(cls.DATABASE_URL)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "database": parsed.path[1:],  # Remove leading slash
            "user": parsed.username,
            "password": parsed.password,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings."""
        errors = []
        
        # Check required directories
        if not cls.RAW_DIR.exists():
            errors.append(f"Raw data directory not found: {cls.RAW_DIR}")
        
        # Check CNAE seed file
        if not cls.CNAE_GREEN_SEED.exists():
            errors.append(f"CNAE green seed file not found: {cls.CNAE_GREEN_SEED}")
        
        # Check UFs format
        if not cls.TARGET_UFS or not all(uf.strip() for uf in cls.TARGET_UFS):
            errors.append("TARGET_UFS must contain valid state codes")
        
        if errors:
            for error in errors:
                print(f"CONFIG ERROR: {error}")
            return False
        
        return True

# Global configuration instance
config = ETLConfig()

# Scoring rules for green companies
class ScoringRules:
    """Scoring rules for calculating green score of companies."""
    
    CORE_CNAE_SCORE = 80
    ADJACENT_CNAE_SCORE = 60
    SECONDARY_CNAE_SCORE = 10
    MAX_SECONDARY_SCORE = 20
    INACTIVE_PENALTY = 50
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    ACTIVE_STATUS = ["ATIVA"]
    
    @classmethod
    def calculate_score(cls, cnae_principal: str, cnaes_secundarias: List[str], 
                       situacao: str, cnae_priorities: dict) -> int:
        """
        Calculate green score for a company based on CNAEs and status.
        
        Args:
            cnae_principal: Primary CNAE code
            cnaes_secundarias: List of secondary CNAE codes
            situacao: Company registration status
            cnae_priorities: Dictionary mapping CNAE to priority level
            
        Returns:
            Green score (0-100)
        """
        score = 0
        
        # Score from primary CNAE
        if cnae_principal in cnae_priorities:
            priority = cnae_priorities[cnae_principal]
            if priority == "Core":
                score += cls.CORE_CNAE_SCORE
            elif priority == "Adjacente":
                score += cls.ADJACENT_CNAE_SCORE
        
        # Score from secondary CNAEs (limited)
        secondary_score = 0
        for cnae in cnaes_secundarias[:5]:  # Limit to first 5 secondary CNAEs
            if cnae in cnae_priorities:
                secondary_score += cls.SECONDARY_CNAE_SCORE
        
        score += min(secondary_score, cls.MAX_SECONDARY_SCORE)
        
        # Penalty for inactive companies
        if situacao not in cls.ACTIVE_STATUS:
            score -= cls.INACTIVE_PENALTY
        
        # Ensure score is within valid range
        return max(cls.MIN_SCORE, min(score, cls.MAX_SCORE))