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
from services.match_calculator import match_calculator

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
    
    # Calcular match
    match_data = match_calculator.calcular_match(vaga, profissional)
    
    return {
        "vaga_id": request.vaga_id,
        "profissional_id": request.profissional_id,
        "score_total": match_data['score_total'],
        "classificacao": match_data['classificacao'],
        "breakdown": match_data['breakdown']
    }

@router.get("/vaga/{vaga_id}/candidatos")
def ranquear_candidatos_para_vaga(
    vaga_id: int,
    min_score: float = 40.0,
    limit: int = 50
):
    """
    Retorna profissionais ranqueados por compatibilidade com uma vaga
    
    Parâmetros:
    - min_score: Score mínimo para aparecer nos resultados (default: 40)
    - limit: Número máximo de resultados (default: 50)
    
    Retorna profissionais ordenados do maior para o menor score
    """
    
    # Buscar vaga
    vaga = get_vaga(vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada ou inativa")
    
    # Buscar todos os profissionais ativos
    profissionais = get_todos_profissionais_ativos()
    
    # Rankear
    matches = match_calculator.rankear_candidatos(vaga, profissionais, min_score)
    
    # Limitar resultados
    matches = matches[:limit]
    
    # Formatar resposta
    resultados = []
    for prof, match_data in matches:
        resultados.append({
            'profissional': {
                'id': prof['id'],
                'nome_completo': prof['nome_completo'],
                'email': prof['email'],
                'cargo_atual': prof['cargo_atual'],
                'nivel_desejado': prof['nivel_desejado'],
                'anos_experiencia_esg': prof['anos_experiencia_esg'],
                'localizacao_uf': prof['localizacao_uf'],
                'localizacao_cidade': prof['localizacao_cidade'],
                'aceita_remoto': prof['aceita_remoto'],
                'ods_interesse': match_calculator._parse_json_field(prof.get('ods_interesse')),
                'habilidades_esg': match_calculator._parse_json_field(prof.get('habilidades_esg'))
            },
            'match': match_data
        })
    
    return {
        'vaga_id': vaga_id,
        'vaga_titulo': vaga.get('titulo'),
        'total_candidatos': len(resultados),
        'candidatos': resultados
    }

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
    
    # Rankear
    matches = match_calculator.rankear_vagas(profissional, vagas, min_score)
    
    # Limitar resultados
    matches = matches[:limit]
    
    # Formatar resposta
    resultados = []
    for vaga, match_data in matches:
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
                'ods_tags': match_calculator._parse_json_field(vaga.get('ods_tags')),
                'habilidades_requeridas': match_calculator._parse_json_field(vaga.get('habilidades_requeridas'))
            },
            'match': match_data
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
            match_data = match_calculator.calcular_match(vaga, prof)
            score = match_data['score_total']
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
    
    matches = match_calculator.rankear_candidatos(vaga, profissionais, min_score=0)
    
    if not matches:
        raise HTTPException(status_code=404, detail="Nenhum match calculado")
    
    melhor_prof, melhor_match = matches[0]
    
    return {
        'vaga_id': vaga_id,
        'vaga_titulo': vaga.get('titulo'),
        'profissional': {
            'id': melhor_prof['id'],
            'nome_completo': melhor_prof['nome_completo'],
            'email': melhor_prof['email'],
            'cargo_atual': melhor_prof['cargo_atual'],
            'anos_experiencia_esg': melhor_prof['anos_experiencia_esg']
        },
        'match': melhor_match
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
    
    matches = match_calculator.rankear_vagas(profissional, vagas, min_score=0)
    
    if not matches:
        raise HTTPException(status_code=404, detail="Nenhum match calculado")
    
    melhor_vaga, melhor_match = matches[0]
    
    return {
        'profissional_id': profissional_id,
        'profissional_nome': profissional.get('nome_completo'),
        'vaga': {
            'id': melhor_vaga['id'],
            'titulo': melhor_vaga['titulo'],
            'empresa_nome': melhor_vaga.get('empresa_nome'),
            'nivel_experiencia': melhor_vaga['nivel_experiencia'],
            'salario_min': melhor_vaga['salario_min'],
            'salario_max': melhor_vaga['salario_max']
        },
        'match': melhor_match
    }
