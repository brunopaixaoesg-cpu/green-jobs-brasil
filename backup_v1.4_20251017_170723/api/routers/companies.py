"""
Green Jobs Brasil - Companies Router
API endpoints for managing and querying green companies.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from api.db import get_db
from api.models import EmpresasVerdes, CnaeGreen, EmpresaCnae
from api.schemas import (
    EmpresaVerdeResponse, 
    EmpresaVerdeDetalhada,
    EmpresasListResponse, 
    EmpresasFilter,
    PorteEnum,
    SituacaoEnum
)

router = APIRouter(prefix="/empresas", tags=["empresas"])

@router.get("", response_model=EmpresasListResponse)
async def listar_empresas(
    uf: Optional[str] = Query(None, description="Filter by state (UF)"),
    municipio: Optional[str] = Query(None, description="Filter by municipality"),
    porte: Optional[PorteEnum] = Query(None, description="Filter by company size"),
    situacao: Optional[SituacaoEnum] = Query(None, description="Filter by registration status"),
    cnae: Optional[str] = Query(None, description="Filter by CNAE code"),
    ods: Optional[int] = Query(None, description="Filter by ODS number"),
    q: Optional[str] = Query(None, description="Text search in company name"),
    limit: int = Query(50, ge=1, le=1000, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    List green companies with optional filters.
    
    Returns paginated list of companies matching the specified criteria.
    """
    try:
        # Build base query
        query = db.query(EmpresasVerdes)
        
        # Apply filters
        filters = []
        
        if uf:
            filters.append(EmpresasVerdes.uf == uf.upper())
        
        if municipio:
            filters.append(EmpresasVerdes.municipio.ilike(f"%{municipio}%"))
        
        if porte:
            filters.append(EmpresasVerdes.porte == porte.value)
        
        if situacao:
            filters.append(EmpresasVerdes.situacao_cadastral == situacao.value)
        
        if cnae:
            # Search in primary or secondary CNAEs
            cnae_filter = or_(
                EmpresasVerdes.cnae_principal == cnae,
                EmpresasVerdes.cnaes_secundarias.any(cnae)
            )
            filters.append(cnae_filter)
        
        if ods:
            filters.append(EmpresasVerdes.ods_tags.any(ods))
        
        if q:
            # Text search in company names
            text_filter = or_(
                EmpresasVerdes.razao_social.ilike(f"%{q}%"),
                EmpresasVerdes.nome_fantasia.ilike(f"%{q}%")
            )
            filters.append(text_filter)
        
        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        companies = query.order_by(
            EmpresasVerdes.score_verde.desc(),
            EmpresasVerdes.razao_social
        ).limit(limit).offset(offset).all()
        
        # Calculate pagination info
        has_next = offset + limit < total
        has_prev = offset > 0
        
        return EmpresasListResponse(
            items=companies,
            total=total,
            limit=limit,
            offset=offset,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")

@router.get("/{cnpj}", response_model=EmpresaVerdeDetalhada)
async def obter_empresa(cnpj: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific company by CNPJ.
    
    Returns complete company data including related CNAEs information.
    """
    try:
        # Clean CNPJ (remove non-numeric characters)
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        # Get company
        empresa = db.query(EmpresasVerdes).filter(
            EmpresasVerdes.cnpj == cnpj_clean
        ).first()
        
        if not empresa:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get related CNAEs details
        cnaes_relacionados = db.query(CnaeGreen).join(
            EmpresaCnae, CnaeGreen.cnae == EmpresaCnae.codigo_cnae
        ).filter(EmpresaCnae.cnpj == cnpj_clean).all()
        
        # Build detailed response
        empresa_detalhada = EmpresaVerdeDetalhada(
            **empresa.__dict__,
            cnaes_detalhados=cnaes_relacionados
        )
        
        return empresa_detalhada
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")

@router.get("/stats/por-uf")
async def stats_por_uf(db: Session = Depends(get_db)):
    """Get company statistics grouped by state (UF)."""
    try:
        result = db.execute(text("""
            SELECT 
                uf,
                COUNT(*) as total_empresas,
                ROUND(AVG(score_verde), 2) as score_medio,
                COUNT(CASE WHEN cg.prioridade = 'Core' THEN 1 END) as empresas_core,
                COUNT(CASE WHEN cg.prioridade = 'Adjacente' THEN 1 END) as empresas_adjacentes
            FROM gjb.empresas_verdes ev
            LEFT JOIN gjb.cnae_green cg ON ev.cnae_principal = cg.cnae
            GROUP BY uf
            ORDER BY total_empresas DESC
        """)).fetchall()
        
        return [
            {
                "uf": row.uf,
                "total_empresas": row.total_empresas,
                "score_medio": float(row.score_medio or 0),
                "empresas_core": row.empresas_core,
                "empresas_adjacentes": row.empresas_adjacentes
            }
            for row in result
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching UF stats: {str(e)}")

@router.get("/stats/por-porte")
async def stats_por_porte(db: Session = Depends(get_db)):
    """Get company statistics grouped by company size (porte)."""
    try:
        result = db.execute(text("""
            SELECT 
                COALESCE(porte, 'NÃO_INFORMADO') as porte,
                COUNT(*) as total_empresas,
                ROUND(AVG(score_verde), 2) as score_medio
            FROM gjb.empresas_verdes
            GROUP BY porte
            ORDER BY total_empresas DESC
        """)).fetchall()
        
        return [
            {
                "porte": row.porte,
                "total_empresas": row.total_empresas,
                "score_medio": float(row.score_medio or 0)
            }
            for row in result
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching size stats: {str(e)}")

@router.get("/export/csv")
async def exportar_empresas_csv(
    uf: Optional[str] = Query(None),
    cnae: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Export companies data as CSV (placeholder for future implementation)."""
    # This would implement CSV export functionality
    raise HTTPException(status_code=501, detail="CSV export not yet implemented")