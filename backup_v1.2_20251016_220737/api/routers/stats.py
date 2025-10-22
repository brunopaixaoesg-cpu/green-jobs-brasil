"""
Green Jobs Brasil - Statistics Router
API endpoints for generating statistics and analytics.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime
from api.db import get_db
from api.models import EmpresasVerdes, CnaeGreen
from api.schemas import StatsResponse

router = APIRouter(prefix="/stats", tags=["statistics"])

@router.get("", response_model=StatsResponse)
async def obter_estatisticas_completas(db: Session = Depends(get_db)):
    """
    Get comprehensive statistics about green companies.
    
    Returns complete analytics including:
    - Total companies count
    - Statistics by state (UF)
    - Statistics by CNAE
    - Statistics by company size
    - Most frequent ODS
    - Last update timestamp
    """
    try:
        # Get total companies count
        total_empresas = db.query(EmpresasVerdes).count()
        
        # Get last update
        ultima_atualizacao_result = db.query(
            func.max(EmpresasVerdes.atualizado_em)
        ).scalar()
        ultima_atualizacao = ultima_atualizacao_result or datetime.now()
        
        # Statistics by UF
        uf_stats_query = text("""
            SELECT 
                ev.uf,
                COUNT(*) as total_empresas,
                ROUND(AVG(ev.score_verde), 2) as score_medio,
                COUNT(CASE WHEN cg.prioridade = 'Core' THEN 1 END) as empresas_core,
                COUNT(CASE WHEN cg.prioridade = 'Adjacente' THEN 1 END) as empresas_adjacentes
            FROM gjb.empresas_verdes ev
            LEFT JOIN gjb.cnae_green cg ON ev.cnae_principal = cg.cnae
            GROUP BY ev.uf
            ORDER BY total_empresas DESC
        """)
        uf_stats_raw = db.execute(uf_stats_query).fetchall()
        
        por_uf = [
            {
                "uf": row.uf,
                "total_empresas": row.total_empresas,
                "score_medio": float(row.score_medio or 0),
                "empresas_core": row.empresas_core,
                "empresas_adjacentes": row.empresas_adjacentes
            }
            for row in uf_stats_raw
        ]
        
        # Statistics by CNAE
        cnae_stats_query = text("""
            SELECT 
                cg.cnae,
                cg.titulo,
                cg.categoria,
                COUNT(ev.cnpj) as total_empresas,
                array_agg(DISTINCT ev.uf ORDER BY ev.uf) as ufs
            FROM gjb.cnae_green cg
            LEFT JOIN gjb.empresas_verdes ev ON cg.cnae = ev.cnae_principal
            GROUP BY cg.cnae, cg.titulo, cg.categoria
            HAVING COUNT(ev.cnpj) > 0
            ORDER BY total_empresas DESC
            LIMIT 20
        """)
        cnae_stats_raw = db.execute(cnae_stats_query).fetchall()
        
        por_cnae = []
        for row in cnae_stats_raw:
            # Get UF distribution for this CNAE
            uf_dist_query = text("""
                SELECT uf, COUNT(*) as count
                FROM gjb.empresas_verdes
                WHERE cnae_principal = :cnae
                GROUP BY uf
                ORDER BY count DESC
            """)
            uf_dist = db.execute(uf_dist_query, {"cnae": row.cnae}).fetchall()
            
            por_cnae.append({
                "cnae": row.cnae,
                "titulo": row.titulo,
                "categoria": row.categoria,
                "total_empresas": row.total_empresas,
                "por_uf": [{"uf": r.uf, "count": r.count} for r in uf_dist]
            })
        
        # Statistics by company size (porte)
        porte_stats_query = text("""
            SELECT 
                COALESCE(porte, 'NÃO_INFORMADO') as porte,
                COUNT(*) as total_empresas,
                ROUND(AVG(score_verde), 2) as score_medio
            FROM gjb.empresas_verdes
            GROUP BY porte
            ORDER BY total_empresas DESC
        """)
        porte_stats_raw = db.execute(porte_stats_query).fetchall()
        
        por_porte = [
            {
                "porte": row.porte,
                "total_empresas": row.total_empresas,
                "score_medio": float(row.score_medio or 0)
            }
            for row in porte_stats_raw
        ]
        
        # Most frequent ODS
        ods_stats_query = text("""
            SELECT 
                unnest(ods_tags) as ods_numero,
                COUNT(*) as frequencia
            FROM gjb.empresas_verdes
            WHERE ods_tags IS NOT NULL AND array_length(ods_tags, 1) > 0
            GROUP BY ods_numero
            ORDER BY frequencia DESC
            LIMIT 10
        """)
        ods_stats_raw = db.execute(ods_stats_query).fetchall()
        
        ods_mais_frequentes = [
            {"ods": row.ods_numero, "frequencia": row.frequencia}
            for row in ods_stats_raw
        ]
        
        return StatsResponse(
            total_empresas_verdes=total_empresas,
            ultima_atualizacao=ultima_atualizacao,
            por_uf=por_uf,
            por_cnae=por_cnae,
            por_porte=por_porte,
            ods_mais_frequentes=ods_mais_frequentes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating statistics: {str(e)}")

@router.get("/dashboard/kpis")
async def obter_kpis_dashboard(db: Session = Depends(get_db)):
    """
    Get key performance indicators for dashboard display.
    
    Returns essential metrics in a format optimized for dashboard widgets.
    """
    try:
        # Main KPIs
        kpis_query = text("""
            SELECT 
                COUNT(*) as total_empresas,
                COUNT(DISTINCT uf) as total_ufs,
                COUNT(DISTINCT cnae_principal) as total_cnaes_ativos,
                ROUND(AVG(score_verde), 1) as score_medio_geral,
                COUNT(CASE WHEN score_verde >= 80 THEN 1 END) as empresas_alto_score,
                COUNT(CASE WHEN situacao_cadastral = 'ATIVA' THEN 1 END) as empresas_ativas
            FROM gjb.empresas_verdes
        """)
        
        kpis_result = db.execute(kpis_query).fetchone()
        
        # Recent activity
        atividade_recente_query = text("""
            SELECT DATE(atualizado_em) as data, COUNT(*) as empresas_atualizadas
            FROM gjb.empresas_verdes
            WHERE atualizado_em >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(atualizado_em)
            ORDER BY data DESC
        """)
        
        atividade_recente = db.execute(atividade_recente_query).fetchall()
        
        return {
            "kpis_principais": {
                "total_empresas": kpis_result.total_empresas,
                "total_ufs": kpis_result.total_ufs,
                "total_cnaes_ativos": kpis_result.total_cnaes_ativos,
                "score_medio_geral": float(kpis_result.score_medio_geral or 0),
                "empresas_alto_score": kpis_result.empresas_alto_score,
                "empresas_ativas": kpis_result.empresas_ativas,
                "percentual_ativas": round((kpis_result.empresas_ativas / kpis_result.total_empresas) * 100, 1) if kpis_result.total_empresas > 0 else 0
            },
            "atividade_recente": [
                {"data": row.data.isoformat(), "empresas_atualizadas": row.empresas_atualizadas}
                for row in atividade_recente
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating KPIs: {str(e)}")

@router.get("/trends/crescimento")
async def obter_trends_crescimento(db: Session = Depends(get_db)):
    """
    Get growth trends for green companies.
    
    Returns trend data for visualization charts.
    """
    try:
        # Growth by registration date
        crescimento_query = text("""
            SELECT 
                DATE_TRUNC('month', data_abertura) as mes,
                COUNT(*) as novas_empresas
            FROM gjb.empresas_verdes
            WHERE data_abertura IS NOT NULL 
              AND data_abertura >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY DATE_TRUNC('month', data_abertura)
            ORDER BY mes
        """)
        
        crescimento_result = db.execute(crescimento_query).fetchall()
        
        return {
            "crescimento_mensal": [
                {
                    "mes": row.mes.strftime("%Y-%m") if row.mes else None,
                    "novas_empresas": row.novas_empresas
                }
                for row in crescimento_result
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating growth trends: {str(e)}")