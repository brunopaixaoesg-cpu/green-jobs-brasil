"""
Router de API para Profissionais ESG
Endpoints para CRUD de profissionais verdes
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
import sqlite3
import json

router = APIRouter(
    prefix="/api/profissionais",
    tags=["profissionais"]
)

# Database connection
DB_PATH = "gjb_dev.db"

# ===== SCHEMAS =====

class ExperienciaProfissional(BaseModel):
    empresa: str
    cargo: str
    descricao: Optional[str] = None
    data_inicio: str  # Format: YYYY-MM-DD
    data_fim: Optional[str] = None
    emprego_atual: bool = False
    ods_relacionados: List[int] = []
    conquistas: Optional[str] = None

class FormacaoAcademica(BaseModel):
    nivel: str  # medio, tecnico, superior, pos-graduacao, mestrado, doutorado
    curso: str
    instituicao: str
    ano_inicio: Optional[int] = None
    ano_conclusao: Optional[int] = None
    em_andamento: bool = False
    descricao: Optional[str] = None

class ProfissionalCreate(BaseModel):
    email: EmailStr
    nome_completo: str
    telefone: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    aceita_remoto: bool = True
    disponivel_mudanca: bool = False
    
    anos_experiencia_total: Optional[int] = None
    anos_experiencia_esg: Optional[int] = None
    cargo_atual: Optional[str] = None
    empresa_atual: Optional[str] = None
    
    formacao_nivel: Optional[str] = None
    formacao_area: Optional[str] = None
    instituicao: Optional[str] = None
    
    ods_interesse: List[int] = []
    ods_experiencia: dict = {}  # {"7": 3, "13": 5}
    habilidades_esg: List[str] = []
    certificacoes: List[dict] = []  # [{"nome": "ISO 14001", "ano": 2023}]
    
    areas_interesse: List[str] = []
    nivel_desejado: Optional[str] = None
    tipo_contratacao_desejado: List[str] = []
    pretensao_salarial_min: Optional[float] = None
    pretensao_salarial_max: Optional[float] = None
    
    curriculo_url: Optional[str] = None
    carta_apresentacao: Optional[str] = None
    resumo_profissional: Optional[str] = None
    motivacao_esg: Optional[str] = None
    
    disponibilidade: str = "imediata"

class ProfissionalUpdate(BaseModel):
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    aceita_remoto: Optional[bool] = None
    disponivel_mudanca: Optional[bool] = None
    
    anos_experiencia_total: Optional[int] = None
    anos_experiencia_esg: Optional[int] = None
    cargo_atual: Optional[str] = None
    empresa_atual: Optional[str] = None
    
    formacao_nivel: Optional[str] = None
    formacao_area: Optional[str] = None
    instituicao: Optional[str] = None
    
    ods_interesse: Optional[List[int]] = None
    ods_experiencia: Optional[dict] = None
    habilidades_esg: Optional[List[str]] = None
    certificacoes: Optional[List[dict]] = None
    
    areas_interesse: Optional[List[str]] = None
    nivel_desejado: Optional[str] = None
    tipo_contratacao_desejado: Optional[List[str]] = None
    pretensao_salarial_min: Optional[float] = None
    pretensao_salarial_max: Optional[float] = None
    
    curriculo_url: Optional[str] = None
    carta_apresentacao: Optional[str] = None
    resumo_profissional: Optional[str] = None
    motivacao_esg: Optional[str] = None
    
    status: Optional[str] = None
    disponibilidade: Optional[str] = None

class ProfissionalResponse(BaseModel):
    id: int
    email: str
    nome_completo: str
    telefone: Optional[str]
    linkedin_url: Optional[str]
    portfolio_url: Optional[str]
    
    localizacao_uf: Optional[str]
    localizacao_cidade: Optional[str]
    aceita_remoto: bool
    disponivel_mudanca: bool
    
    anos_experiencia_total: Optional[int]
    anos_experiencia_esg: Optional[int]
    cargo_atual: Optional[str]
    empresa_atual: Optional[str]
    
    formacao_nivel: Optional[str]
    formacao_area: Optional[str]
    instituicao: Optional[str]
    
    ods_interesse: List[int]
    ods_experiencia: dict
    habilidades_esg: List[str]
    certificacoes: List[dict]
    
    areas_interesse: List[str]
    nivel_desejado: Optional[str]
    tipo_contratacao_desejado: List[str]
    pretensao_salarial_min: Optional[float]
    pretensao_salarial_max: Optional[float]
    
    curriculo_url: Optional[str]
    carta_apresentacao: Optional[str]
    resumo_profissional: Optional[str]
    motivacao_esg: Optional[str]
    
    status: str
    perfil_completo: bool
    aceita_contato: bool
    disponibilidade: str
    
    visualizacoes_perfil: int
    candidaturas_enviadas: int
    matches_recebidos: int
    
    criado_em: str
    atualizado_em: str
    ultimo_acesso: Optional[str]

# ===== HELPER FUNCTIONS =====

def dict_factory(cursor, row):
    """Converte row do SQLite para dict"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def parse_json_field(value):
    """Parse de campos JSON"""
    if value is None:
        return []
    if isinstance(value, str):
        try:
            return json.loads(value)
        except:
            return []
    return value

def profissional_to_response(row: dict) -> dict:
    """Converte row do banco para response"""
    row['ods_interesse'] = parse_json_field(row.get('ods_interesse'))
    row['ods_experiencia'] = parse_json_field(row.get('ods_experiencia'))
    if not isinstance(row['ods_experiencia'], dict):
        row['ods_experiencia'] = {}
    
    row['habilidades_esg'] = parse_json_field(row.get('habilidades_esg'))
    row['certificacoes'] = parse_json_field(row.get('certificacoes'))
    row['areas_interesse'] = parse_json_field(row.get('areas_interesse'))
    row['tipo_contratacao_desejado'] = parse_json_field(row.get('tipo_contratacao_desejado'))
    
    return row

# ===== ENDPOINTS =====

@router.get("/", response_model=List[ProfissionalResponse])
def listar_profissionais(
    ods: Optional[int] = None,
    uf: Optional[str] = None,
    nivel: Optional[str] = None,
    remoto: Optional[bool] = None,
    min_exp_esg: Optional[int] = None,
    habilidade: Optional[str] = None,
    status: str = "ativo",
    limit: int = 50,
    offset: int = 0
):
    """
    Lista profissionais ESG com filtros
    
    Filtros disponíveis:
    - ods: Filtra por ODS de interesse
    - uf: Filtra por estado (SP, RJ, etc)
    - nivel: Filtra por nível desejado (junior, pleno, senior, especialista, gerencial)
    - remoto: Filtra profissionais que aceitam trabalho remoto
    - min_exp_esg: Anos mínimos de experiência ESG
    - habilidade: Filtra por habilidade específica
    - status: Status do profissional (ativo, inativo, pausado)
    """
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    query = "SELECT * FROM profissionais_esg WHERE status = ?"
    params = [status]
    
    # Aplicar filtros
    if uf:
        query += " AND localizacao_uf = ?"
        params.append(uf)
    
    if nivel:
        query += " AND nivel_desejado = ?"
        params.append(nivel)
    
    if remoto is not None:
        query += " AND aceita_remoto = ?"
        params.append(1 if remoto else 0)
    
    if min_exp_esg:
        query += " AND anos_experiencia_esg >= ?"
        params.append(min_exp_esg)
    
    query += " ORDER BY anos_experiencia_esg DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    profissionais = cursor.fetchall()
    conn.close()
    
    # Filtros que precisam de JSON parsing
    result = []
    for prof in profissionais:
        prof = profissional_to_response(prof)
        
        # Filtro ODS
        if ods and ods not in prof['ods_interesse']:
            continue
        
        # Filtro habilidade
        if habilidade:
            habs = [h.lower() for h in prof['habilidades_esg']]
            if habilidade.lower() not in habs:
                continue
        
        result.append(prof)
    
    return result

@router.get("/{profissional_id}", response_model=ProfissionalResponse)
def obter_profissional(profissional_id: int, incrementar_visualizacao: bool = True):
    """Obtém detalhes de um profissional específico"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    # Incrementar visualizações
    if incrementar_visualizacao:
        cursor.execute(
            "UPDATE profissionais_esg SET visualizacoes_perfil = visualizacoes_perfil + 1, ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?",
            (profissional_id,)
        )
        conn.commit()
    
    # Buscar profissional
    cursor.execute("SELECT * FROM profissionais_esg WHERE id = ?", (profissional_id,))
    prof = cursor.fetchone()
    conn.close()
    
    if not prof:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    
    return profissional_to_response(prof)

@router.post("/", response_model=ProfissionalResponse, status_code=201)
def criar_profissional(profissional: ProfissionalCreate):
    """Cria um novo cadastro de profissional"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        # Verificar email duplicado
        cursor.execute("SELECT id FROM profissionais_esg WHERE email = ?", (profissional.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        # Converter listas/dicts para JSON
        ods_interesse_json = json.dumps(profissional.ods_interesse)
        ods_experiencia_json = json.dumps(profissional.ods_experiencia)
        habilidades_json = json.dumps(profissional.habilidades_esg)
        certificacoes_json = json.dumps(profissional.certificacoes)
        areas_json = json.dumps(profissional.areas_interesse)
        contratacao_json = json.dumps(profissional.tipo_contratacao_desejado)
        
        # Inserir profissional
        cursor.execute("""
            INSERT INTO profissionais_esg (
                email, nome_completo, telefone, linkedin_url, portfolio_url,
                localizacao_uf, localizacao_cidade, aceita_remoto, disponivel_mudanca,
                anos_experiencia_total, anos_experiencia_esg, cargo_atual, empresa_atual,
                formacao_nivel, formacao_area, instituicao,
                ods_interesse, ods_experiencia, habilidades_esg, certificacoes,
                areas_interesse, nivel_desejado, tipo_contratacao_desejado,
                pretensao_salarial_min, pretensao_salarial_max,
                curriculo_url, carta_apresentacao, resumo_profissional, motivacao_esg,
                disponibilidade, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profissional.email, profissional.nome_completo, profissional.telefone,
            profissional.linkedin_url, profissional.portfolio_url,
            profissional.localizacao_uf, profissional.localizacao_cidade,
            profissional.aceita_remoto, profissional.disponivel_mudanca,
            profissional.anos_experiencia_total, profissional.anos_experiencia_esg,
            profissional.cargo_atual, profissional.empresa_atual,
            profissional.formacao_nivel, profissional.formacao_area, profissional.instituicao,
            ods_interesse_json, ods_experiencia_json, habilidades_json, certificacoes_json,
            areas_json, profissional.nivel_desejado, contratacao_json,
            profissional.pretensao_salarial_min, profissional.pretensao_salarial_max,
            profissional.curriculo_url, profissional.carta_apresentacao,
            profissional.resumo_profissional, profissional.motivacao_esg,
            profissional.disponibilidade, "ativo"
        ))
        
        profissional_id = cursor.lastrowid
        conn.commit()
        
        # Buscar profissional criado
        cursor.execute("SELECT * FROM profissionais_esg WHERE id = ?", (profissional_id,))
        novo_prof = cursor.fetchone()
        conn.close()
        
        return profissional_to_response(novo_prof)
        
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Erro de integridade: {str(e)}")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao criar profissional: {str(e)}")

@router.put("/{profissional_id}", response_model=ProfissionalResponse)
def atualizar_profissional(profissional_id: int, profissional: ProfissionalUpdate):
    """Atualiza dados de um profissional"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        # Verificar se profissional existe
        cursor.execute("SELECT id FROM profissionais_esg WHERE id = ?", (profissional_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        # Construir UPDATE dinamicamente
        updates = []
        params = []
        
        data_dict = profissional.dict(exclude_unset=True)
        
        for field, value in data_dict.items():
            if field in ['ods_interesse', 'ods_experiencia', 'habilidades_esg', 'certificacoes', 'areas_interesse', 'tipo_contratacao_desejado']:
                value = json.dumps(value)
            
            updates.append(f"{field} = ?")
            params.append(value)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        params.append(profissional_id)
        
        query = f"UPDATE profissionais_esg SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        # Buscar profissional atualizado
        cursor.execute("SELECT * FROM profissionais_esg WHERE id = ?", (profissional_id,))
        prof_atualizado = cursor.fetchone()
        conn.close()
        
        return profissional_to_response(prof_atualizado)
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar profissional: {str(e)}")

@router.delete("/{profissional_id}")
def deletar_profissional(profissional_id: int, soft_delete: bool = True):
    """
    Deleta um profissional (soft delete por padrão)
    
    - soft_delete=True: Marca como inativo
    - soft_delete=False: Remove do banco permanentemente
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        if soft_delete:
            cursor.execute(
                "UPDATE profissionais_esg SET status = 'inativo' WHERE id = ?",
                (profissional_id,)
            )
            message = "Profissional marcado como inativo"
        else:
            cursor.execute("DELETE FROM profissionais_esg WHERE id = ?", (profissional_id,))
            message = "Profissional removido permanentemente"
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        conn.commit()
        conn.close()
        
        return {"message": message, "profissional_id": profissional_id}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar profissional: {str(e)}")

@router.get("/stats/resumo")
def estatisticas_profissionais():
    """Retorna estatísticas gerais dos profissionais"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total de profissionais
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg WHERE status = 'ativo'")
    total = cursor.fetchone()[0]
    
    # Por nível
    cursor.execute("""
        SELECT nivel_desejado, COUNT(*) 
        FROM profissionais_esg 
        WHERE status = 'ativo' AND nivel_desejado IS NOT NULL
        GROUP BY nivel_desejado
    """)
    por_nivel = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Por UF
    cursor.execute("""
        SELECT localizacao_uf, COUNT(*) 
        FROM profissionais_esg 
        WHERE status = 'ativo' AND localizacao_uf IS NOT NULL
        GROUP BY localizacao_uf
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)
    por_uf = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Aceitam remoto
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg WHERE status = 'ativo' AND aceita_remoto = 1")
    remotos = cursor.fetchone()[0]
    
    # Experiência média ESG
    cursor.execute("SELECT AVG(anos_experiencia_esg) FROM profissionais_esg WHERE status = 'ativo' AND anos_experiencia_esg IS NOT NULL")
    exp_media = cursor.fetchone()[0]
    
    # Perfis completos
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg WHERE status = 'ativo' AND perfil_completo = 1")
    completos = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_profissionais": total,
        "por_nivel": por_nivel,
        "por_uf": por_uf,
        "aceitam_remoto": remotos,
        "experiencia_media_esg": round(exp_media, 1) if exp_media else 0,
        "perfis_completos": completos,
        "taxa_perfil_completo": round((completos / total * 100), 1) if total > 0 else 0
    }

@router.post("/{profissional_id}/experiencia", status_code=201)
def adicionar_experiencia(profissional_id: int, experiencia: ExperienciaProfissional):
    """Adiciona uma experiência profissional ao currículo"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar se profissional existe
        cursor.execute("SELECT id FROM profissionais_esg WHERE id = ?", (profissional_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        ods_json = json.dumps(experiencia.ods_relacionados)
        
        cursor.execute("""
            INSERT INTO experiencias_profissionais (
                profissional_id, empresa, cargo, descricao,
                data_inicio, data_fim, emprego_atual,
                ods_relacionados, conquistas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profissional_id, experiencia.empresa, experiencia.cargo, experiencia.descricao,
            experiencia.data_inicio, experiencia.data_fim, experiencia.emprego_atual,
            ods_json, experiencia.conquistas
        ))
        
        exp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"message": "Experiência adicionada", "experiencia_id": exp_id}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar experiência: {str(e)}")

@router.post("/{profissional_id}/formacao", status_code=201)
def adicionar_formacao(profissional_id: int, formacao: FormacaoAcademica):
    """Adiciona uma formação acadêmica ao currículo"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar se profissional existe
        cursor.execute("SELECT id FROM profissionais_esg WHERE id = ?", (profissional_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        cursor.execute("""
            INSERT INTO formacoes_academicas (
                profissional_id, nivel, curso, instituicao,
                ano_inicio, ano_conclusao, em_andamento, descricao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profissional_id, formacao.nivel, formacao.curso, formacao.instituicao,
            formacao.ano_inicio, formacao.ano_conclusao, formacao.em_andamento, formacao.descricao
        ))
        
        formacao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"message": "Formação adicionada", "formacao_id": formacao_id}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar formação: {str(e)}")
