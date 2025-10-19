"""
Router de API para Sistema de Matching
Conecta vagas com profissionais usando algoritmo de compatibilidade
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import sqlite3
import sys
import os

# Adicionar path para services
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.unified_matching import unified_matching
from services.match_calculator import MatchCalculator

# Instanciar o match calculator
match_calculator = MatchCalculator()

router = APIRouter(
    prefix="/api/matching",
    tags=["matching"]
)

# Database connection
DB_PATH = "gjb_dev.db"

# ===== SCHEMAS =====

class MatchRequest(BaseModel):
    vaga_id: int
    profissional_id: int

class MatchResponse(BaseModel):
    vaga_id: int
    profissional_id: int
    score_total: float
    classificacao: str
    breakdown: dict

# ===== HELPER FUNCTIONS =====

def dict_factory(cursor, row):
    """Converte row do SQLite para dict"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_vaga(vaga_id: int):
    """Busca vaga no banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vagas_esg WHERE id = ? AND status = 'ativa'", (vaga_id,))
    vaga = cursor.fetchone()
    conn.close()
    
    return vaga

def get_profissional(profissional_id: int):
    """Busca profissional no banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM profissionais_esg WHERE id = ? AND status = 'ativo'", (profissional_id,))
    prof = cursor.fetchone()
    conn.close()
    
    return prof

def get_todas_vagas_ativas():
    """Busca todas as vagas ativas"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.*, e.razao_social as empresa_nome
        FROM vagas_esg v
        LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
        WHERE v.status = 'ativa' 
        ORDER BY v.criada_em DESC
    """)
    vagas = cursor.fetchall()
    conn.close()
    
    return vagas

def get_todos_profissionais_ativos():
    """Busca todos os profissionais ativos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM profissionais_esg WHERE status = 'ativo' ORDER BY criado_em DESC")
    profs = cursor.fetchall()
    conn.close()
    
    return profs

# ===== ENDPOINTS =====

@router.post("/calcular", response_model=MatchResponse)
def calcular_match(request: MatchRequest):
    """
    Calcula score de compatibilidade entre uma vaga e um profissional
    
    Retorna score de 0-100 e breakdown detalhado por critério:
    - ODS (40%)
    - Habilidades (30%)
    - Experiência (15%)
    - Localização (10%)
    - Salário (5%)
    """
    
    # Buscar vaga
    vaga = get_vaga(request.vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada ou inativa")
    
    # Buscar profissional
    profissional = get_profissional(request.profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado ou inativo")
    
    # Calcular match usando ML
    score = unified_matching.calculate_compatibility(vaga, profissional)
    
    return {
        "vaga_id": request.vaga_id,
        "profissional_id": request.profissional_id,
        "score_total": score,
        "score_compatibilidade": score,
        "model_used": "ML_ensemble",
        "breakdown": match_data['breakdown']
    }

@router.get("/vaga/{vaga_id}/candidatos")
def ranquear_candidatos_para_vaga(
    vaga_id: int,
    min_score: float = 40.0,
    limit: int = 50
):
    """
    Retorna profissionais que se candidataram a uma vaga, ranqueados por compatibilidade
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # Buscar vaga
        cursor.execute("SELECT * FROM vagas_esg WHERE id = ? AND status = 'ativa'", (vaga_id,))
        vaga = cursor.fetchone()
        
        if not vaga:
            conn.close()
            raise HTTPException(status_code=404, detail="Vaga não encontrada ou inativa")
        
        # Buscar candidatos que se candidataram a esta vaga
        query = """
            SELECT 
                p.*,
                c.data_candidatura,
                c.status as candidatura_status
            FROM candidaturas_esg c
            JOIN profissionais_esg p ON c.profissional_id = p.id
            WHERE c.vaga_id = ? 
            AND p.status = 'ativo'
            ORDER BY c.data_candidatura DESC
            LIMIT ?
        """
        
        cursor.execute(query, (vaga_id, limit * 2))  # Buscar mais para filtrar depois
        candidatos_raw = cursor.fetchall()
        conn.close()
        
        # Calcular compatibilidade usando ML para cada candidato
        candidatos = []
        for candidato in candidatos_raw:
            try:
                # Usar o sistema ML unificado para calcular compatibilidade
                match_result = unified_matching.calculate_compatibility(candidato['id'], vaga_id)
                score = match_result['score_total']
                
                # Filtrar por score mínimo
                if score >= min_score:
                    candidatos.append({
                        'profissional': {
                            'id': candidato['id'],
                            'nome_completo': candidato['nome_completo'],
                            'email': candidato['email'],
                            'cargo_atual': candidato['cargo_atual'],
                            'empresa_atual': candidato['empresa_atual'],
                            'anos_experiencia_esg': candidato['anos_experiencia_esg'],
                            'localizacao_uf': candidato['localizacao_uf'],
                            'localizacao_cidade': candidato['localizacao_cidade'],
                            'aceita_remoto': candidato['aceita_remoto']
                        },
                        'match': {
                            'score_total': score,
                            'classificacao': match_result['classificacao'],
                            'data_candidatura': candidato['data_candidatura'],
                            'status': candidato['candidatura_status'],
                            'model_used': match_result.get('model_used', 'unknown'),
                            'breakdown': match_result.get('breakdown', {})
                        }
                    })
            except Exception as e:
                # Em caso de erro no ML, usar score padrão
                candidatos.append({
                    'profissional': {
                        'id': candidato['id'],
                        'nome_completo': candidato['nome_completo'],
                        'email': candidato['email'],
                        'cargo_atual': candidato['cargo_atual'],
                        'empresa_atual': candidato['empresa_atual'],
                        'anos_experiencia_esg': candidato['anos_experiencia_esg'],
                        'localizacao_uf': candidato['localizacao_uf'],
                        'localizacao_cidade': candidato['localizacao_cidade'],
                        'aceita_remoto': candidato['aceita_remoto']
                    },
                    'match': {
                        'score_total': 45,
                        'classificacao': 'regular',
                        'data_candidatura': candidato['data_candidatura'],
                        'status': candidato['candidatura_status'],
                        'model_used': 'error_fallback',
                        'error': str(e)
                    }
                })
        
        # Ordenar por score (maior primeiro) e limitar
        candidatos.sort(key=lambda x: x['match']['score_total'], reverse=True)
        candidatos = candidatos[:limit]
        
        return {
            'vaga_id': vaga_id,
            'vaga_titulo': vaga.get('titulo'),
            'total_candidatos': len(candidatos),
            'candidatos': candidatos
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no matching: {str(e)}")

@router.get("/profissional/{profissional_id}/vagas")
def ranquear_vagas_para_profissional(
    profissional_id: int,
    min_score: float = 40.0,
    limit: int = 50
):
    """
    Retorna vagas ranqueadas por compatibilidade com um profissional
    
    Parâmetros:
    - min_score: Score mínimo para aparecer nos resultados (default: 40)
    - limit: Número máximo de resultados (default: 50)
    
    Retorna vagas ordenadas do maior para o menor score
    """
    
    # Buscar profissional
    profissional = get_profissional(profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado ou inativo")
    
    # Buscar todas as vagas ativas
    vagas = get_todas_vagas_ativas()
    
    # Rankear usando ML
    results = []
    for vaga in vagas:
        try:
            # Usar sistema unificado de matching (ML + tradicional)
            score = unified_matching.calculate_compatibility(vaga, profissional)
            
            if score >= min_score:
                results.append({
                    'vaga': vaga,
                    'score_compatibilidade': score,
                    'model_used': 'ML_ensemble'
                })
        except Exception as e:
            print(f"Erro no cálculo para vaga {vaga.get('id')}: {e}")
            continue
    
    # Ordenar por score (maior primeiro)
    results.sort(key=lambda x: x['score_compatibilidade'], reverse=True)
    
    # Limitar resultados
    results = results[:limit]
    
    # Formatar resposta
    resultados = []
    for result in results:
        vaga = result['vaga']
        resultados.append({
            'vaga': {
                'id': vaga['id'],
                'titulo': vaga['titulo'],
                'cnpj': vaga['cnpj'],
                'empresa_nome': vaga.get('empresa_nome'),
                'descricao': vaga['descricao'],
                'nivel_experiencia': vaga['nivel_experiencia'],
                'tipo_contratacao': vaga['tipo_contratacao'],
                'localizacao_uf': vaga['localizacao_uf'],
                'localizacao_cidade': vaga['localizacao_cidade'],
                'remoto': vaga['remoto'],
                'salario_min': vaga['salario_min'],
                'salario_max': vaga['salario_max'],
                'ods_tags': vaga.get('ods_tags'),
                'habilidades_requeridas': vaga.get('habilidades_requeridas')
            },
            'score_compatibilidade': result['score_compatibilidade'],
            'model_used': result['model_used']
        })
    
    return {
        'profissional_id': profissional_id,
        'profissional_nome': profissional.get('nome_completo'),
        'total_vagas': len(resultados),
        'vagas': resultados
    }

@router.get("/stats/geral")
def estatisticas_matching():
    """
    Retorna estatísticas gerais do sistema de matching
    
    - Total de matches possíveis
    - Distribuição de scores
    - Taxa de compatibilidade média
    """
    
    vagas = get_todas_vagas_ativas()
    profissionais = get_todos_profissionais_ativos()
    
    total_vagas = len(vagas)
    total_profissionais = len(profissionais)
    total_combinacoes = total_vagas * total_profissionais
    
    # Calcular sample de matches para estatísticas
    # (limitar para não sobrecarregar - max 100 matches)
    sample_size = min(100, total_combinacoes)
    
    if total_vagas == 0 or total_profissionais == 0:
        return {
            'total_vagas': total_vagas,
            'total_profissionais': total_profissionais,
            'total_combinacoes': 0,
            'matches_excelentes': 0,
            'matches_bons': 0,
            'matches_regulares': 0,
            'matches_baixos': 0,
            'score_medio': 0,
            'taxa_compatibilidade': 0
        }
    
    # Sample de vagas e profissionais
    import random
    sample_vagas = vagas[:min(10, len(vagas))]
    sample_profs = profissionais[:min(10, len(profissionais))]
    
    scores = []
    excelentes = 0
    bons = 0
    regulares = 0
    baixos = 0
    
    for vaga in sample_vagas:
        for prof in sample_profs:
            score = unified_matching.calculate_compatibility(vaga, prof)
            scores.append(score)
            
            if score >= 80:
                excelentes += 1
            elif score >= 60:
                bons += 1
            elif score >= 40:
                regulares += 1
            else:
                baixos += 1
    
    score_medio = sum(scores) / len(scores) if scores else 0
    taxa_compat = ((excelentes + bons) / len(scores) * 100) if scores else 0
    
    return {
        'total_vagas': total_vagas,
        'total_profissionais': total_profissionais,
        'total_combinacoes': total_combinacoes,
        'sample_analisado': len(scores),
        'matches_excelentes': excelentes,
        'matches_bons': bons,
        'matches_regulares': regulares,
        'matches_baixos': baixos,
        'score_medio': round(score_medio, 2),
        'taxa_compatibilidade': round(taxa_compat, 2)
    }

@router.get("/vaga/{vaga_id}/melhor-candidato")
def obter_melhor_candidato(vaga_id: int):
    """
    Retorna o candidato com maior score para uma vaga específica
    """
    
    vaga = get_vaga(vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    
    profissionais = get_todos_profissionais_ativos()
    
    if not profissionais:
        raise HTTPException(status_code=404, detail="Nenhum profissional ativo encontrado")
    
    # Rankear usando ML
    results = []
    for prof in profissionais:
        try:
            # Usar sistema unificado de matching (ML + tradicional)
            score = unified_matching.calculate_compatibility(vaga, prof)
            
            if score >= 0:  # min_score = 0 para candidatos
                results.append({
                    'profissional': prof,
                    'score_compatibilidade': score,
                    'model_used': 'ML_ensemble'
                })
        except Exception as e:
            print(f"Erro no cálculo para profissional {prof.get('id')}: {e}")
            continue
    
    # Ordenar por score (maior primeiro)
    results.sort(key=lambda x: x['score_compatibilidade'], reverse=True)
    
    if not results:
        raise HTTPException(status_code=404, detail="Nenhum match calculado")
    
    melhor_result = results[0]
    
    return {
        'vaga_id': vaga_id,
        'vaga_titulo': vaga.get('titulo'),
        'profissional': {
            'id': melhor_result['profissional']['id'],
            'nome_completo': melhor_result['profissional']['nome_completo'],
            'email': melhor_result['profissional']['email'],
            'cargo_atual': melhor_result['profissional']['cargo_atual'],
            'anos_experiencia_esg': melhor_result['profissional']['anos_experiencia_esg']
        },
        'score_compatibilidade': melhor_result['score_compatibilidade'],
        'model_used': melhor_result['model_used']
    }

@router.get("/profissional/{profissional_id}/melhor-vaga")
def obter_melhor_vaga(profissional_id: int):
    """
    Retorna a vaga com maior score para um profissional específico
    """
    
    profissional = get_profissional(profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    
    vagas = get_todas_vagas_ativas()
    
    if not vagas:
        raise HTTPException(status_code=404, detail="Nenhuma vaga ativa encontrada")
    
    # Rankear usando ML
    results = []
    for vaga in vagas:
        try:
            score = unified_matching.calculate_compatibility(vaga, profissional)
            results.append({
                'vaga': vaga,
                'score_compatibilidade': score,
                'model_used': 'ML_ensemble'
            })
        except Exception as e:
            print(f"Erro no cálculo para vaga {vaga.get('id')}: {e}")
            continue
    
    # Ordenar por score (maior primeiro)
    results.sort(key=lambda x: x['score_compatibilidade'], reverse=True)
    
    if not results:
        raise HTTPException(status_code=404, detail="Nenhum match calculado")
    
    melhor_result = results[0]
    
    return {
        'profissional_id': profissional_id,
        'profissional_nome': profissional.get('nome_completo'),
        'vaga': {
            'id': melhor_result['vaga']['id'],
            'titulo': melhor_result['vaga']['titulo'],
            'empresa_nome': melhor_result['vaga'].get('empresa_nome'),
            'nivel_experiencia': melhor_result['vaga']['nivel_experiencia'],
            'salario_min': melhor_result['vaga']['salario_min'],
            'salario_max': melhor_result['vaga']['salario_max']
        },
        'score_compatibilidade': melhor_result['score_compatibilidade'],
        'model_used': melhor_result['model_used']
    }

@router.get("/status")
async def get_matching_status():
    """Status do sistema de matching"""
    return unified_matching.get_service_status()

@router.get("/test-ml/{profissional_id}/{vaga_id}")
async def test_ml_matching(profissional_id: int, vaga_id: int):
    """Testar matching ML vs tradicional"""
    try:
        ml_result = unified_matching.calculate_compatibility(profissional_id, vaga_id)
        return {
            'profissional_id': profissional_id,
            'vaga_id': vaga_id,
            'ml_result': ml_result,
            'system_status': unified_matching.get_service_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
