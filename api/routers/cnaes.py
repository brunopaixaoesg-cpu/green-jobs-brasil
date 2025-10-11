"""
Green Jobs Brasil - CNAEs Router
API endpoints for managing and querying green CNAE classifications.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from api.db import get_db
from api.models import CnaeGreen
from api.schemas import CnaeGreenResponse, CnaesListResponse, PrioridadeEnum

router = APIRouter(prefix="/cnaes", tags=["cnaes"])

@router.get("", response_model=CnaesListResponse)
async def listar_cnaes(
    categoria: Optional[str] = Query(None, description="Filter by category"),
    prioridade: Optional[PrioridadeEnum] = Query(None, description="Filter by priority level"),
    ods: Optional[int] = Query(None, description="Filter by ODS number"),
    db: Session = Depends(get_db)
):
    """
    List all green CNAE classifications with optional filters.
    
    Returns list of CNAEs with their categories, priorities, and ODS mappings.
    """
    try:
        # Build base query
        query = db.query(CnaeGreen)
        
        # Apply filters
        filters = []
        
        if categoria:
            filters.append(CnaeGreen.categoria.ilike(f"%{categoria}%"))
        
        if prioridade:
            filters.append(CnaeGreen.prioridade == prioridade)
        
        if ods:
            filters.append(CnaeGreen.ods_tags.any(ods))
        
        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Get results ordered by category and title
        cnaes = query.order_by(
            CnaeGreen.categoria,
            CnaeGreen.prioridade.desc(),
            CnaeGreen.titulo
        ).all()
        
        return CnaesListResponse(
            items=cnaes,
            total=len(cnaes)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CNAEs: {str(e)}")

@router.get("/{cnae_code}", response_model=CnaeGreenResponse)
async def obter_cnae(cnae_code: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific CNAE code.
    
    Returns complete CNAE classification data including ODS mappings.
    """
    try:
        cnae = db.query(CnaeGreen).filter(CnaeGreen.cnae == cnae_code).first()
        
        if not cnae:
            raise HTTPException(status_code=404, detail="CNAE not found")
        
        return cnae
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CNAE: {str(e)}")

@router.get("/categorias/list")
async def listar_categorias(db: Session = Depends(get_db)):
    """
    Get list of all available CNAE categories.
    
    Returns unique categories from the green CNAEs database.
    """
    try:
        result = db.query(CnaeGreen.categoria).distinct().order_by(CnaeGreen.categoria).all()
        categorias = [row.categoria for row in result]
        
        return {"categorias": categorias}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.get("/stats/resumo")
async def stats_cnaes(db: Session = Depends(get_db)):
    """
    Get summary statistics about green CNAEs.
    
    Returns counts by category, priority, and ODS mappings.
    """
    try:
        # Count by category
        categoria_stats = db.query(
            CnaeGreen.categoria,
            func.count(CnaeGreen.cnae).label('total')
        ).group_by(CnaeGreen.categoria).order_by(CnaeGreen.categoria).all()
        
        # Count by priority
        prioridade_stats = db.query(
            CnaeGreen.prioridade,
            func.count(CnaeGreen.cnae).label('total')
        ).group_by(CnaeGreen.prioridade).all()
        
        # Total count
        total_cnaes = db.query(CnaeGreen).count()
        
        return {
            "total_cnaes": total_cnaes,
            "por_categoria": [
                {"categoria": row.categoria, "total": row.total}
                for row in categoria_stats
            ],
            "por_prioridade": [
                {"prioridade": row.prioridade, "total": row.total}
                for row in prioridade_stats
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CNAE stats: {str(e)}")

@router.get("/ods/mapping")
async def mapping_ods(db: Session = Depends(get_db)):
    """
    Get mapping of CNAEs to ODS (Sustainable Development Goals).
    
    Returns CNAEs grouped by ODS numbers.
    """
    try:
        # This would require more complex SQL to unnest array and group
        # For now, return a simplified version
        cnaes_com_ods = db.query(CnaeGreen).filter(
            CnaeGreen.ods_tags.isnot(None)
        ).all()
        
        # Group by ODS manually
        ods_mapping = {}
        for cnae in cnaes_com_ods:
            if cnae.ods_tags:
                for ods_num in cnae.ods_tags:
                    if ods_num not in ods_mapping:
                        ods_mapping[ods_num] = []
                    ods_mapping[ods_num].append({
                        "cnae": cnae.cnae,
                        "titulo": cnae.titulo,
                        "categoria": cnae.categoria,
                        "prioridade": cnae.prioridade
                    })
        
        return {"ods_mapping": ods_mapping}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ODS mapping: {str(e)}")