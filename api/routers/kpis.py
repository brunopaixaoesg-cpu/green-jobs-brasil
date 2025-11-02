"""
Router para endpoints de KPIs e métricas consolidadas
Fornece estatísticas agregadas, tendências e rankings
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Literal
from datetime import datetime, timedelta
from pydantic import BaseModel
import sqlite3
from ..db import get_db

router = APIRouter(prefix="/api/kpis", tags=["KPIs"])


# ==================== MODELS ====================

class KPIsGerais(BaseModel):
    """Métricas gerais da plataforma"""
    total_profissionais: int
    total_empresas: int
    total_vagas: int
    total_candidaturas: int
    profissionais_ativos: int
    vagas_abertas: int
    taxa_match: float
    crescimento_profissionais_30d: float
    crescimento_vagas_30d: float


class KPIsPorPeriodo(BaseModel):
    """Métricas agregadas por período"""
    periodo: str
    novos_profissionais: int
    novas_vagas: int
    novas_candidaturas: int
    matches_realizados: int


class TopItem(BaseModel):
    """Item de ranking"""
    id: int
    nome: str
    valor: float
    metrica: str


class KPIsConsolidados(BaseModel):
    """Response completo do endpoint /api/kpis"""
    gerais: KPIsGerais
    tendencias: list[KPIsPorPeriodo]
    top_profissionais: list[TopItem]
    top_empresas: list[TopItem]
    top_vagas: list[TopItem]
    ods_mais_buscados: list[dict]
    areas_mais_demandadas: list[dict]


# ==================== ENDPOINTS ====================

@router.get("/", response_model=KPIsConsolidados)
async def obter_kpis_consolidados(
    periodo: Literal["dia", "semana", "mes"] = Query("mes", description="Período para tendências"),
    limit_top: int = Query(10, ge=1, le=50, description="Limite para rankings")
):
    """
    Retorna KPIs consolidados da plataforma
    
    Inclui:
    - Métricas gerais (totais, ativos, taxas)
    - Tendências por período
    - Top profissionais (por candidaturas)
    - Top empresas (por vagas publicadas)
    - Top vagas (por candidatos)
    - ODS mais buscados
    - Áreas mais demandadas
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # ========== MÉTRICAS GERAIS ==========
        
        # Total de profissionais
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        total_profissionais = cursor.fetchone()[0]
        
        # Total de empresas
        cursor.execute("SELECT COUNT(*) FROM empresas_verdes")
        total_empresas = cursor.fetchone()[0]
        
        # Total de vagas
        cursor.execute("SELECT COUNT(*) FROM vagas")
        total_vagas = cursor.fetchone()[0]
        
        # Total de candidaturas
        cursor.execute("SELECT COUNT(*) FROM candidaturas")
        total_candidaturas = cursor.fetchone()[0]
        
        # Profissionais ativos (com login nos últimos 30 dias)
        cursor.execute("""
            SELECT COUNT(*) FROM profissionais_esg 
            WHERE ultimo_acesso >= date('now', '-30 days')
        """)
        profissionais_ativos = cursor.fetchone()[0] or 0
        
        # Vagas abertas
        cursor.execute("SELECT COUNT(*) FROM vagas WHERE status = 'aberta'")
        vagas_abertas = cursor.fetchone()[0]
        
        # Taxa de match (candidaturas / profissionais)
        taxa_match = (total_candidaturas / total_profissionais * 100) if total_profissionais > 0 else 0
        
        # Crescimento profissionais 30 dias
        cursor.execute("""
            SELECT COUNT(*) FROM profissionais_esg 
            WHERE created_at >= date('now', '-30 days')
        """)
        novos_prof_30d = cursor.fetchone()[0]
        crescimento_prof = (novos_prof_30d / total_profissionais * 100) if total_profissionais > 0 else 0
        
        # Crescimento vagas 30 dias
        cursor.execute("""
            SELECT COUNT(*) FROM vagas 
            WHERE created_at >= date('now', '-30 days')
        """)
        novas_vagas_30d = cursor.fetchone()[0]
        crescimento_vagas = (novas_vagas_30d / total_vagas * 100) if total_vagas > 0 else 0
        
        gerais = KPIsGerais(
            total_profissionais=total_profissionais,
            total_empresas=total_empresas,
            total_vagas=total_vagas,
            total_candidaturas=total_candidaturas,
            profissionais_ativos=profissionais_ativos,
            vagas_abertas=vagas_abertas,
            taxa_match=round(taxa_match, 2),
            crescimento_profissionais_30d=round(crescimento_prof, 2),
            crescimento_vagas_30d=round(crescimento_vagas, 2)
        )
        
        # ========== TENDÊNCIAS ==========
        
        # Calcular número de períodos baseado no tipo
        if periodo == "dia":
            num_periodos = 30
            date_format = "%Y-%m-%d"
            date_modifier = "-1 day"
        elif periodo == "semana":
            num_periodos = 12
            date_format = "%Y-W%W"
            date_modifier = "-7 days"
        else:  # mes
            num_periodos = 12
            date_format = "%Y-%m"
            date_modifier = "-1 month"
        
        tendencias = []
        for i in range(num_periodos, 0, -1):
            # Calcular data inicial e final do período
            if periodo == "dia":
                data_inicio = f"date('now', '-{i} days')"
                data_fim = f"date('now', '-{i-1} days')"
            elif periodo == "semana":
                data_inicio = f"date('now', '-{i*7} days')"
                data_fim = f"date('now', '-{(i-1)*7} days')"
            else:
                data_inicio = f"date('now', '-{i} months', 'start of month')"
                data_fim = f"date('now', '-{i-1} months', 'start of month')"
            
            # Novos profissionais
            cursor.execute(f"""
                SELECT COUNT(*) FROM profissionais_esg 
                WHERE created_at >= {data_inicio} AND created_at < {data_fim}
            """)
            novos_prof = cursor.fetchone()[0]
            
            # Novas vagas
            cursor.execute(f"""
                SELECT COUNT(*) FROM vagas 
                WHERE created_at >= {data_inicio} AND created_at < {data_fim}
            """)
            novas_vagas = cursor.fetchone()[0]
            
            # Novas candidaturas
            cursor.execute(f"""
                SELECT COUNT(*) FROM candidaturas 
                WHERE created_at >= {data_inicio} AND created_at < {data_fim}
            """)
            novas_candidaturas = cursor.fetchone()[0]
            
            # Matches (candidaturas aceitas ou em entrevista)
            cursor.execute(f"""
                SELECT COUNT(*) FROM candidaturas 
                WHERE (status = 'aceita' OR status = 'em_entrevista')
                AND created_at >= {data_inicio} AND created_at < {data_fim}
            """)
            matches = cursor.fetchone()[0]
            
            tendencias.append(KPIsPorPeriodo(
                periodo=f"Período {num_periodos - i + 1}",
                novos_profissionais=novos_prof,
                novas_vagas=novas_vagas,
                novas_candidaturas=novas_candidaturas,
                matches_realizados=matches
            ))
        
        # ========== TOP PROFISSIONAIS ==========
        
        cursor.execute(f"""
            SELECT 
                p.id,
                p.nome_completo,
                COUNT(c.id) as num_candidaturas
            FROM profissionais_esg p
            LEFT JOIN candidaturas c ON p.id = c.profissional_id
            GROUP BY p.id, p.nome_completo
            ORDER BY num_candidaturas DESC
            LIMIT {limit_top}
        """)
        
        top_profissionais = [
            TopItem(
                id=row[0],
                nome=row[1],
                valor=float(row[2]),
                metrica="candidaturas"
            )
            for row in cursor.fetchall()
        ]
        
        # ========== TOP EMPRESAS ==========
        
        cursor.execute(f"""
            SELECT 
                e.id,
                e.nome_empresa,
                COUNT(v.id) as num_vagas
            FROM empresas_verdes e
            LEFT JOIN vagas v ON e.id = v.empresa_id
            GROUP BY e.id, e.nome_empresa
            ORDER BY num_vagas DESC
            LIMIT {limit_top}
        """)
        
        top_empresas = [
            TopItem(
                id=row[0],
                nome=row[1],
                valor=float(row[2]),
                metrica="vagas_publicadas"
            )
            for row in cursor.fetchall()
        ]
        
        # ========== TOP VAGAS ==========
        
        cursor.execute(f"""
            SELECT 
                v.id,
                v.titulo,
                COUNT(c.id) as num_candidatos
            FROM vagas v
            LEFT JOIN candidaturas c ON v.id = c.vaga_id
            GROUP BY v.id, v.titulo
            ORDER BY num_candidatos DESC
            LIMIT {limit_top}
        """)
        
        top_vagas = [
            TopItem(
                id=row[0],
                nome=row[1],
                valor=float(row[2]),
                metrica="candidatos"
            )
            for row in cursor.fetchall()
        ]
        
        # ========== ODS MAIS BUSCADOS ==========
        
        # Agregar ODS de profissionais e vagas
        ods_count = {}
        
        # ODS de interesse dos profissionais
        cursor.execute("SELECT ods_interesse FROM profissionais_esg WHERE ods_interesse IS NOT NULL")
        for row in cursor.fetchall():
            if row[0]:
                for ods in row[0].split(','):
                    ods = ods.strip()
                    ods_count[ods] = ods_count.get(ods, 0) + 1
        
        # ODS das vagas
        cursor.execute("SELECT ods_alinhados FROM vagas WHERE ods_alinhados IS NOT NULL")
        for row in cursor.fetchall():
            if row[0]:
                for ods in row[0].split(','):
                    ods = ods.strip()
                    ods_count[ods] = ods_count.get(ods, 0) + 1
        
        ods_mais_buscados = [
            {"ods": ods, "count": count}
            for ods, count in sorted(ods_count.items(), key=lambda x: x[1], reverse=True)[:limit_top]
        ]
        
        # ========== ÁREAS MAIS DEMANDADAS ==========
        
        cursor.execute(f"""
            SELECT 
                area_atuacao,
                COUNT(*) as count
            FROM vagas
            WHERE area_atuacao IS NOT NULL
            GROUP BY area_atuacao
            ORDER BY count DESC
            LIMIT {limit_top}
        """)
        
        areas_mais_demandadas = [
            {"area": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return KPIsConsolidados(
            gerais=gerais,
            tendencias=tendencias,
            top_profissionais=top_profissionais,
            top_empresas=top_empresas,
            top_vagas=top_vagas,
            ods_mais_buscados=ods_mais_buscados,
            areas_mais_demandadas=areas_mais_demandadas
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter KPIs: {str(e)}")


@router.get("/gerais")
async def obter_kpis_gerais():
    """Retorna apenas KPIs gerais (mais rápido)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        total_profissionais = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empresas_verdes")
        total_empresas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vagas")
        total_vagas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM candidaturas")
        total_candidaturas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vagas WHERE status = 'aberta'")
        vagas_abertas = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_profissionais": total_profissionais,
            "total_empresas": total_empresas,
            "total_vagas": total_vagas,
            "total_candidaturas": total_candidaturas,
            "vagas_abertas": vagas_abertas
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter KPIs gerais: {str(e)}")
