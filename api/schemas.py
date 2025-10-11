"""
Green Jobs Brasil - Pydantic Schemas
Request/Response models for the API.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class PrioridadeEnum(str, Enum):
    """Priority levels for green CNAEs."""
    CORE = "Core"
    ADJACENTE = "Adjacente"

class PorteEnum(str, Enum):
    """Company size categories."""
    ME = "ME"  # Microempresa
    EPP = "EPP"  # Empresa de Pequeno Porte
    DEMAIS = "DEMAIS"  # Demais empresas

class SituacaoEnum(str, Enum):
    """Company registration status."""
    ATIVA = "ATIVA"
    SUSPENSA = "SUSPENSA"
    INAPTA = "INAPTA"
    BAIXADA = "BAIXADA"

# Base schemas
class CnaeGreenBase(BaseModel):
    """Base schema for CNAE green classification."""
    cnae: str
    titulo: str
    categoria: str
    ods_raw: Optional[str] = None
    prioridade: PrioridadeEnum
    observacoes: Optional[str] = None

class CnaeGreenResponse(CnaeGreenBase):
    """Response schema for CNAE green classification."""
    ods_tags: List[int] = Field(default_factory=list)
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmpresaVerdeBase(BaseModel):
    """Base schema for green company."""
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnae_principal: str
    cnaes_secundarias: List[str] = Field(default_factory=list)
    porte: Optional[str] = None
    uf: str
    municipio: Optional[str] = None
    situacao_cadastral: Optional[str] = None
    data_abertura: Optional[date] = None

class EmpresaVerdeResponse(EmpresaVerdeBase):
    """Response schema for green company."""
    score_verde: Optional[int] = None
    ods_tags: List[int] = Field(default_factory=list)
    fonte_atualizacao: str = "ETL_RFB"
    atualizado_em: datetime
    
    class Config:
        from_attributes = True

class EmpresaVerdeDetalhada(EmpresaVerdeResponse):
    """Detailed company response with related CNAEs."""
    cnaes_detalhados: List[CnaeGreenResponse] = Field(default_factory=list)

# Request schemas
class EmpresasFilter(BaseModel):
    """Filter parameters for companies search."""
    uf: Optional[str] = None
    municipio: Optional[str] = None
    porte: Optional[PorteEnum] = None
    situacao: Optional[SituacaoEnum] = None
    cnae: Optional[str] = None
    ods: Optional[int] = None
    q: Optional[str] = Field(None, description="Text search in company name")
    limit: int = Field(50, ge=1, le=1000, description="Number of results per page")
    offset: int = Field(0, ge=0, description="Number of results to skip")

class CnaesFilter(BaseModel):
    """Filter parameters for CNAEs search."""
    categoria: Optional[str] = None
    prioridade: Optional[PrioridadeEnum] = None
    ods: Optional[int] = None

# Response schemas for lists
class EmpresasListResponse(BaseModel):
    """Paginated response for companies list."""
    items: List[EmpresaVerdeResponse]
    total: int
    limit: int
    offset: int
    has_next: bool
    has_prev: bool

class CnaesListResponse(BaseModel):
    """Response for CNAEs list."""
    items: List[CnaeGreenResponse]
    total: int

# Statistics schemas
class UFStats(BaseModel):
    """Statistics by state."""
    uf: str
    total_empresas: int
    score_medio: float
    empresas_core: int
    empresas_adjacentes: int

class CnaeStats(BaseModel):
    """Statistics by CNAE."""
    cnae: str
    titulo: str
    categoria: str
    total_empresas: int
    por_uf: List[dict]

class PorteStats(BaseModel):
    """Statistics by company size."""
    porte: str
    total_empresas: int
    score_medio: float

class StatsResponse(BaseModel):
    """Complete statistics response."""
    total_empresas_verdes: int
    ultima_atualizacao: datetime
    por_uf: List[UFStats]
    por_cnae: List[CnaeStats]
    por_porte: List[PorteStats]
    ods_mais_frequentes: List[dict]

# Health check schema
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    timestamp: datetime
    version: str = "1.0.0"
    database_connected: bool