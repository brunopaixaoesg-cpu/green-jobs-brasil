"""
Green Jobs Brasil - Statistics Router
API endpoints for generating statistics and analytics.
"""

from typing import List
from fastapi import APIRouter, HTTPException
from datetime import datetime
import sqlite3
import json
from api.db import get_db

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("")
async def obter_estatisticas_completas():
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
        # Use sqlite3 connection and simple queries compatible with SQLite
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Total companies
        cur.execute("SELECT COUNT(*) as total FROM empresas_esg")
        total_empresas = cur.fetchone()['total']

        # Last update (fallback to now)
        try:
            cur.execute("SELECT MAX(created_at) as ultima FROM empresas_esg")
            ultima = cur.fetchone()['ultima']
            ultima_atualizacao = ultima if ultima else datetime.now().isoformat()
        except Exception:
            ultima_atualizacao = datetime.now().isoformat()

        # By UF
        cur.execute("SELECT COALESCE(localizacao_uf, 'NA') as uf, COUNT(*) as total_empresas, AVG(score_verde) as score_medio FROM empresas_esg GROUP BY uf ORDER BY total_empresas DESC LIMIT 50")
        por_uf = [dict(r) for r in cur.fetchall()]

        # By CNAE (top 20)
        cur.execute("SELECT cnae_principal as cnae, COUNT(*) as total_empresas FROM empresas_esg WHERE cnae_principal IS NOT NULL GROUP BY cnae_principal ORDER BY total_empresas DESC LIMIT 20")
        por_cnae = []
        for r in cur.fetchall():
            por_cnae.append({"cnae": r['cnae'], "total_empresas": r['total_empresas']})

        # By porte
        cur.execute("SELECT COALESCE(porte, 'NAO_INFORMADO') as porte, COUNT(*) as total_empresas, AVG(score_verde) as score_medio FROM empresas_esg GROUP BY porte ORDER BY total_empresas DESC")
        por_porte = [dict(r) for r in cur.fetchall()]

        # Simple ODS frequency (assumes ods_tags is a JSON array string)
        ods_counts = {}
        try:
            cur.execute("SELECT ods_tags FROM empresas_esg WHERE ods_tags IS NOT NULL")
            for row in cur.fetchall():
                try:
                    tags = json.loads(row['ods_tags']) if row['ods_tags'] else []
                    for t in tags:
                        ods_counts[str(t)] = ods_counts.get(str(t), 0) + 1
                except Exception:
                    continue
        except Exception:
            pass

        ods_mais_frequentes = sorted([{"ods": k, "frequencia": v} for k, v in ods_counts.items()], key=lambda x: x['frequencia'], reverse=True)[:10]

        conn.close()

        return {
            "total_empresas_verdes": total_empresas,
            "ultima_atualizacao": ultima_atualizacao,
            "por_uf": por_uf,
            "por_cnae": por_cnae,
            "por_porte": por_porte,
            "ods_mais_frequentes": ods_mais_frequentes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating statistics: {str(e)}")

@router.get("/dashboard/kpis")
async def obter_kpis_dashboard():
    """
    Get key performance indicators for dashboard display.
    
    Returns essential metrics in a format optimized for dashboard widgets.
    """
    try:
        # Main KPIs
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as total_empresas, COUNT(DISTINCT localizacao_uf) as total_ufs, COUNT(DISTINCT cnae_principal) as total_cnaes_ativos, AVG(score_verde) as score_medio_geral, SUM(CASE WHEN score_verde >= 80 THEN 1 ELSE 0 END) as empresas_alto_score, SUM(CASE WHEN status = 'ativa' THEN 1 ELSE 0 END) as empresas_ativas FROM empresas_esg")
        kpis = cur.fetchone()

        # Recent activity (simple last 7 days by created_at)
        try:
            cur.execute("SELECT DATE(created_at) as data, COUNT(*) as empresas_atualizadas FROM empresas_esg WHERE DATE(created_at) >= DATE('now','-7 days') GROUP BY DATE(created_at) ORDER BY data DESC")
            atividade_recente = [{"data": row['data'], "empresas_atualizadas": row['empresas_atualizadas']} for row in cur.fetchall()]
        except Exception:
            atividade_recente = []

        conn.close()

        total_empresas = kpis['total_empresas'] if kpis else 0
        return {
            "kpis_principais": {
                "total_empresas": total_empresas,
                "total_ufs": kpis['total_ufs'] if kpis else 0,
                "total_cnaes_ativos": kpis['total_cnaes_ativos'] if kpis else 0,
                "score_medio_geral": float(kpis['score_medio_geral'] or 0) if kpis else 0,
                "empresas_alto_score": kpis['empresas_alto_score'] if kpis else 0,
                "empresas_ativas": kpis['empresas_ativas'] if kpis else 0,
                "percentual_ativas": round((kpis['empresas_ativas'] / total_empresas) * 100, 1) if total_empresas > 0 else 0
            },
            "atividade_recente": atividade_recente
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating KPIs: {str(e)}")

@router.get("/trends/crescimento")
async def obter_trends_crescimento():
    """
    Get growth trends for green companies.
    
    Returns trend data for visualization charts.
    """
    try:
        # Growth by registration date
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Aggregate by month using SQLite strftime
        cur.execute("SELECT strftime('%Y-%m', created_at) as mes, COUNT(*) as novas_empresas FROM empresas_esg WHERE created_at IS NOT NULL AND created_at >= date('now','-2 years') GROUP BY mes ORDER BY mes")
        crescimento_result = cur.fetchall()
        conn.close()

        return {"crescimento_mensal": [{"mes": row['mes'], "novas_empresas": row['novas_empresas']} for row in crescimento_result]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating growth trends: {str(e)}")