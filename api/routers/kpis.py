"""
Router para endpoints de KPIs e métricas consolidadas
Fornece estatísticas agregadas, tendências e rankings
Versão atualizada com suporte a empresas_esg
"""

from fastapi import APIRouter, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Literal
from datetime import datetime, timedelta
from pydantic import BaseModel
import sqlite3
import sys
import os

# Adicionar path para importar db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db

# Configurar templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

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
        
        # Total de empresas (tentar diferentes nomes de tabela)
        total_empresas = 0
        empresa_table_found = None
        for table_name in ['empresas_esg', 'empresas', 'empresas_verdes', 'empresa']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_empresas = cursor.fetchone()[0]
                empresa_table_found = table_name
                print(f"✅ Tabela encontrada: {table_name} com {total_empresas} registros")
                break
            except Exception as e:
                print(f"❌ Tentou {table_name}: {e}")
                continue
        
        if not empresa_table_found:
            print("⚠️ Nenhuma tabela de empresas encontrada!")
        
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
                WHERE data_candidatura >= {data_inicio} AND data_candidatura < {data_fim}
            """)
            novas_candidaturas = cursor.fetchone()[0]
            
            # Matches (candidaturas aceitas ou em entrevista)
            cursor.execute(f"""
                SELECT COUNT(*) FROM candidaturas 
                WHERE (status = 'aceita' OR status = 'em analise')
                AND data_candidatura >= {data_inicio} AND data_candidatura < {data_fim}
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
                COALESCE(p.nome_completo, p.nome) as nome,
                COUNT(c.id) as num_candidaturas
            FROM profissionais_esg p
            LEFT JOIN candidaturas c ON p.email = c.email
            GROUP BY p.id, COALESCE(p.nome_completo, p.nome)
            ORDER BY num_candidaturas DESC
            LIMIT {limit_top}
        """)
        
        top_profissionais = [
            TopItem(
                id=row[0],
                nome=row[1] or "Profissional",
                valor=float(row[2]),
                metrica="candidaturas"
            )
            for row in cursor.fetchall()
        ]
        
        # ========== TOP EMPRESAS ==========
        
        # Detectar nome da tabela de empresas
        empresa_table = None
        for table_name in ['empresas_esg', 'empresas', 'empresas_verdes', 'empresa']:
            try:
                cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
                empresa_table = table_name
                break
            except:
                continue
        
        top_empresas = []
        if empresa_table:
            # Detectar campos disponíveis na tabela
            cursor.execute(f"PRAGMA table_info({empresa_table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Escolher campo de nome baseado no que existe
            if 'nome_fantasia' in columns:
                nome_field = "e.nome_fantasia"
            elif 'razao_social' in columns:
                nome_field = "e.razao_social"
            elif 'nome' in columns:
                nome_field = "e.nome"
            else:
                nome_field = "'Empresa'"
            
            cursor.execute(f"""
                SELECT 
                    e.id,
                    {nome_field} as nome,
                    COUNT(v.id) as num_vagas
                FROM {empresa_table} e
                LEFT JOIN vagas v ON e.cnpj = v.cnpj
                GROUP BY e.id
                ORDER BY num_vagas DESC
                LIMIT {limit_top}
            """)
            
            top_empresas = [
                TopItem(
                    id=row[0],
                    nome=row[1] or "Empresa sem nome",
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
        
        # Agregar ODS de profissionais e empresas
        ods_count = {}
        
        # ODS de interesse dos profissionais
        cursor.execute("SELECT ods_interesse FROM profissionais_esg WHERE ods_interesse IS NOT NULL")
        for row in cursor.fetchall():
            if row[0]:
                for ods in row[0].split(','):
                    ods = ods.strip()
                    ods_count[ods] = ods_count.get(ods, 0) + 1
        
        # ODS das empresas (se tabela existir)
        if empresa_table:
            try:
                cursor.execute(f"PRAGMA table_info({empresa_table})")
                emp_columns = [col[1] for col in cursor.fetchall()]
                if 'ods_tags' in emp_columns:
                    cursor.execute(f"SELECT ods_tags FROM {empresa_table} WHERE ods_tags IS NOT NULL")
                    for row in cursor.fetchall():
                        if row[0]:
                            for ods in row[0].split(','):
                                ods = ods.strip()
                                ods_count[ods] = ods_count.get(ods, 0) + 1
            except:
                pass
        
        ods_mais_buscados = [
            {"ods": ods, "count": count}
            for ods, count in sorted(ods_count.items(), key=lambda x: x[1], reverse=True)[:limit_top]
        ]
        
        # ========== ÁREAS MAIS DEMANDADAS ==========
        # Usar area_atuacao de profissionais como proxy
        areas_mais_demandadas = []
        try:
            cursor.execute(f"""
                SELECT 
                    area_atuacao,
                    COUNT(*) as count
                FROM profissionais_esg
                WHERE area_atuacao IS NOT NULL
                GROUP BY area_atuacao
                ORDER BY count DESC
                LIMIT {limit_top}
            """)
            
            areas_mais_demandadas = [
                {"area": row[0], "count": row[1]}
                for row in cursor.fetchall()
            ]
        except:
            pass
        
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
        
        # Detectar tabela de empresas
        total_empresas = 0
        for table_name in ['empresas_esg', 'empresas', 'empresas_verdes', 'empresa']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_empresas = cursor.fetchone()[0]
                break
            except:
                continue
        
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


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_kpis(request: Request):
    """
    Dashboard visual de KPIs
    Renderiza página HTML com gráficos interativos
    """
    return templates.TemplateResponse("kpis_dashboard.html", {"request": request})
