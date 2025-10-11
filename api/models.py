"""
Green Jobs Brasil - SQLAlchemy Models
Database models for the Green Jobs Brasil application.
"""

from sqlalchemy import Column, String, Integer, DateTime, Date, Text
from sqlalchemy.sql import func
from enum import Enum
from api.db import Base

class PrioridadeEnum(str, Enum):
    """Priority levels for green CNAEs."""
    CORE = "Core"
    ADJACENTE = "Adjacente"

class CnaeGreen(Base):
    """Model for green CNAE classifications."""
    
    __tablename__ = "cnae_green"
    
    cnae = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    ods_raw = Column(String)
    ods_tags = Column(String)  # JSON string for SQLite compatibility
    prioridade = Column(String, nullable=False)  # Core/Adjacente/Secondary
    observacoes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EmpresasVerdes(Base):
    """Model for green companies."""
    
    __tablename__ = "empresas_verdes"
    
    id = Column(Integer, primary_key=True)
    cnpj = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)  # razao_social
    fantasia = Column(String)  # nome_fantasia
    cnae_principal = Column(String)
    cnaes_secundarias = Column(String)  # JSON string for SQLite
    green_score = Column(Integer, default=0)  # score_verde
    situacao = Column(String)  # situacao_cadastral
    porte = Column(String)
    uf = Column(String)
    municipio = Column(String)
    cep = Column(String)
    telefone = Column(String)
    email = Column(String)
    data_abertura = Column(Date)
    ods_tags = Column(String)  # JSON string for SQLite
    fonte_atualizacao = Column(String, default="ETL_RFB")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class EmpresaCnae(Base):
    """Junction model for company-CNAE relationships."""
    
    __tablename__ = "empresa_cnae"
    
    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, nullable=False)  # References empresas_verdes.id
    cnae_codigo = Column(String, nullable=False)  # References cnae_green.codigo