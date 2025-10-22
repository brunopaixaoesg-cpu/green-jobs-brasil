"""
Router de Profissionais ESG - Green Jobs Brasil
Endpoints para gerenciamento de profissionais verdes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import sqlite3
import json
import os

router = APIRouter(prefix="/api/profissionais", tags=["Profissionais ESG"])

# Configuração do banco
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gjb_dev.db")

def get_db():
    """Conexão com banco SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Models Pydantic
class ExperienciaProfissional(BaseModel):
    empresa: str
    cargo: str
    data_inicio: date
    data_fim: Optional[date] = None
    descricao: Optional[str] = None
    area_sustentabilidade: Optional[str] = None

class FormacaoAcademica(BaseModel):
    instituicao: str
    curso: str
    nivel: str  # graduacao, pos, mestrado, doutorado
    data_inicio: date
    data_fim: Optional[date] = None
    area_sustentabilidade: Optional[str] = None

class ProfissionalCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    telefone: Optional[str] = Field(None, max_length=20)
    localizacao: str = Field(..., max_length=100)
    
    # Campos profissionais
    cargo_atual: Optional[str] = Field(None, max_length=100)
    empresa_atual: Optional[str] = Field(None, max_length=100)
    nivel_experiencia: str = Field(..., pattern=r'^(junior|pleno|senior|especialista|diretor)$')
    area_interesse: str = Field(..., max_length=100)
    
    # Skills e competências
    skills_tecnicas: List[str] = Field(default_factory=list)
    skills_sustentabilidade: List[str] = Field(default_factory=list)
    certificacoes: List[str] = Field(default_factory=list)
    
    # Preferências de vaga
    salario_minimo: Optional[float] = Field(None, ge=0)
    modalidade_trabalho: str = Field(..., pattern=r'^(presencial|remoto|hibrido)$')
    disponibilidade_viagem: bool = Field(default=False)
    
    # Perfil sustentabilidade
    motivacao_sustentabilidade: Optional[str] = Field(None, max_length=500)
    experiencia_sustentabilidade: Optional[str] = Field(None, max_length=500)
    
    # Dados complementares
    experiencias: List[ExperienciaProfissional] = Field(default_factory=list)
    formacoes: List[FormacaoAcademica] = Field(default_factory=list)

class ProfissionalResponse(BaseModel):
    id: int
    email: str
    nome_completo: str
    telefone: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    aceita_remoto: Optional[bool] = True
    disponivel_mudanca: Optional[bool] = False
    anos_experiencia_total: Optional[int] = None
    anos_experiencia_esg: Optional[int] = None
    cargo_atual: Optional[str] = None
    empresa_atual: Optional[str] = None
    formacao_nivel: Optional[str] = None
    formacao_area: Optional[str] = None
    instituicao: Optional[str] = None
    ods_interesse: Optional[str] = None
    ods_experiencia: Optional[str] = None
    habilidades_esg: Optional[str] = None
    certificacoes: Optional[str] = None
    areas_interesse: Optional[str] = None
    nivel_desejado: Optional[str] = None
    tipo_contratacao_desejado: Optional[str] = None
    pretensao_salarial_min: Optional[float] = None
    pretensao_salarial_max: Optional[float] = None
    curriculo_url: Optional[str] = None
    carta_apresentacao: Optional[str] = None
    resumo_profissional: Optional[str] = None
    motivacao_esg: Optional[str] = None
    status: Optional[str] = 'ativo'
    perfil_completo: Optional[bool] = False
    aceita_contato: Optional[bool] = True
    disponibilidade: Optional[str] = None
    visualizacoes_perfil: Optional[int] = 0
    candidaturas_enviadas: Optional[int] = 0
    matches_recebidos: Optional[int] = 0
    criado_em: Optional[str] = None
    atualizado_em: Optional[str] = None
    ultimo_acesso: Optional[str] = None

# Função para calcular pontuação de sustentabilidade
def calcular_pontuacao_sustentabilidade(profissional_data):
    """Calcula pontuação de sustentabilidade do profissional (0-100)"""
    pontuacao = 0.0
    
    # Skills sustentabilidade (40%)
    skills_sustentabilidade = profissional_data.get('skills_sustentabilidade', [])
    if skills_sustentabilidade:
        pontuacao += min(len(skills_sustentabilidade) * 8, 40)
    
    # Certificações (25%)
    certificacoes = profissional_data.get('certificacoes', [])
    if certificacoes:
        pontuacao += min(len(certificacoes) * 5, 25)
    
    # Experiência em sustentabilidade (20%)
    if profissional_data.get('experiencia_sustentabilidade'):
        pontuacao += 20
    
    # Motivação sustentabilidade (15%)
    if profissional_data.get('motivacao_sustentabilidade'):
        pontuacao += 15
    
    return min(pontuacao, 100.0)

@router.post("/", response_model=dict)
async def criar_profissional(profissional: ProfissionalCreate):
    """Cadastra novo profissional ESG"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Calcular pontuação de sustentabilidade
        pontuacao = calcular_pontuacao_sustentabilidade(profissional.dict())
        
        # Inserir profissional principal
        query = """
        INSERT INTO profissionais_esg (
            nome, email, telefone, localizacao, cargo_atual, empresa_atual,
            nivel_experiencia, area_interesse, skills_tecnicas, skills_sustentabilidade,
            certificacoes, salario_minimo, modalidade_trabalho, disponibilidade_viagem,
            motivacao_sustentabilidade, experiencia_sustentabilidade, pontuacao_sustentabilidade
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            profissional.nome,
            profissional.email,
            profissional.telefone,
            profissional.localizacao,
            profissional.cargo_atual,
            profissional.empresa_atual,
            profissional.nivel_experiencia,
            profissional.area_interesse,
            json.dumps(profissional.skills_tecnicas, ensure_ascii=False),
            json.dumps(profissional.skills_sustentabilidade, ensure_ascii=False),
            json.dumps(profissional.certificacoes, ensure_ascii=False),
            profissional.salario_minimo,
            profissional.modalidade_trabalho,
            profissional.disponibilidade_viagem,
            profissional.motivacao_sustentabilidade,
            profissional.experiencia_sustentabilidade,
            pontuacao
        ))
        
        profissional_id = cursor.lastrowid
        
        # Inserir experiências
        for exp in profissional.experiencias:
            exp_query = """
            INSERT INTO experiencias_profissionais (
                profissional_id, empresa, cargo, data_inicio, data_fim, descricao, area_sustentabilidade
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(exp_query, (
                profissional_id, exp.empresa, exp.cargo, exp.data_inicio,
                exp.data_fim, exp.descricao, exp.area_sustentabilidade
            ))
        
        # Inserir formações
        for form in profissional.formacoes:
            form_query = """
            INSERT INTO formacoes_academicas (
                profissional_id, instituicao, curso, nivel, data_inicio, data_fim, area_sustentabilidade
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(form_query, (
                profissional_id, form.instituicao, form.curso, form.nivel,
                form.data_inicio, form.data_fim, form.area_sustentabilidade
            ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Profissional cadastrado com sucesso!",
            "id": profissional_id,
            "pontuacao_sustentabilidade": pontuacao
        }
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=List[ProfissionalResponse])
async def listar_profissionais(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    nivel_desejado: Optional[str] = Query(None),
    localizacao_uf: Optional[str] = Query(None),
    areas_interesse: Optional[str] = Query(None)
):
    """Lista profissionais com filtros opcionais"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM profissionais_esg WHERE status = 'ativo'"
        params = []
        
        if nivel_desejado:
            query += " AND nivel_desejado = ?"
            params.append(nivel_desejado)
        
        if localizacao_uf:
            query += " AND localizacao_uf LIKE ?"
            params.append(f"%{localizacao_uf}%")
        
        if areas_interesse:
            query += " AND areas_interesse LIKE ?"
            params.append(f"%{areas_interesse}%")
        
        query += " ORDER BY criado_em DESC LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        profissionais = cursor.fetchall()
        conn.close()
        
        # Converter para formato de response
        result = []
        for prof in profissionais:
            prof_dict = dict(prof)
            result.append(prof_dict)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{profissional_id}", response_model=ProfissionalResponse)
async def obter_profissional(profissional_id: int):
    """Obtém profissional por ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM profissionais_esg WHERE id = ? AND status = 'ativo'", (profissional_id,))
        profissional = cursor.fetchone()
        
        if not profissional:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        conn.close()
        
        prof_dict = dict(profissional)
        return prof_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{profissional_id}/experiencias")
async def obter_experiencias(profissional_id: int):
    """Obtém experiências do profissional"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM experiencias_profissionais WHERE profissional_id = ? ORDER BY data_inicio DESC",
            (profissional_id,)
        )
        experiencias = cursor.fetchall()
        conn.close()
        
        return [dict(exp) for exp in experiencias]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{profissional_id}/formacoes")
async def obter_formacoes(profissional_id: int):
    """Obtém formações do profissional"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM formacoes_academicas WHERE profissional_id = ? ORDER BY data_inicio DESC",
            (profissional_id,)
        )
        formacoes = cursor.fetchall()
        conn.close()
        
        return [dict(form) for form in formacoes]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{profissional_id}")
async def excluir_profissional(profissional_id: int):
    """Exclui profissional (soft delete)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE profissionais_esg SET status = 'inativo', atualizado_em = CURRENT_TIMESTAMP WHERE id = ?",
            (profissional_id,)
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Profissional excluído com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/stats/resumo")
async def stats_profissionais():
    """Estatísticas dos profissionais"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total de profissionais
        cursor.execute("SELECT COUNT(*) as total FROM profissionais_esg WHERE status = 'ativo'")
        total = cursor.fetchone()['total']
        
        # Por nível desejado
        cursor.execute("""
            SELECT nivel_desejado, COUNT(*) as quantidade 
            FROM profissionais_esg 
            WHERE status = 'ativo' AND nivel_desejado IS NOT NULL
            GROUP BY nivel_desejado
        """)
        por_nivel = {row['nivel_desejado']: row['quantidade'] for row in cursor.fetchall()}
        
        # Por UF
        cursor.execute("""
            SELECT localizacao_uf, COUNT(*) as quantidade 
            FROM profissionais_esg 
            WHERE status = 'ativo' AND localizacao_uf IS NOT NULL
            GROUP BY localizacao_uf
            ORDER BY quantidade DESC
            LIMIT 10
        """)
        por_uf = {row['localizacao_uf']: row['quantidade'] for row in cursor.fetchall()}
        
        # Aceita remoto
        cursor.execute("SELECT COUNT(*) as aceita_remoto FROM profissionais_esg WHERE status = 'ativo' AND aceita_remoto = 1")
        aceita_remoto = cursor.fetchone()['aceita_remoto']
        
        conn.close()
        
        return {
            "total_profissionais": total,
            "por_nivel_desejado": por_nivel,
            "por_uf": por_uf,
            "aceita_remoto": aceita_remoto,
            "porcentagem_remoto": round((aceita_remoto / total * 100) if total > 0 else 0, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
