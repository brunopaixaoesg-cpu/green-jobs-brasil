"""
Router de Profissionais ESG - Green Jobs Brasil
Endpoints para gerenciamento de profissionais verdes
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import sqlite3
import json
import os

router = APIRouter(prefix="/api/profissionais", tags=["Profissionais ESG"])

# Importar autenticação
try:
    from .auth import get_current_active_user, UserResponse
except ImportError:
    get_current_active_user = None
    UserResponse = None

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


# ==========================================
# ENDPOINTS PARA DASHBOARD DO PROFISSIONAL
# ==========================================

@router.get("/me/perfil")
async def obter_meu_perfil(current_user: UserResponse = Depends(get_current_active_user)):
    """Obtém perfil completo do profissional logado"""
    if not get_current_active_user:
        raise HTTPException(status_code=501, detail="Autenticação não disponível")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar profissional vinculado ao usuário
        cursor.execute("""
            SELECT p.* FROM profissionais_esg p
            INNER JOIN users u ON p.id = u.profissional_id
            WHERE u.id = ? AND p.status = 'ativo'
        """, (current_user.id,))
        
        profissional = cursor.fetchone()
        
        if not profissional:
            conn.close()
            raise HTTPException(status_code=404, detail="Perfil de profissional não encontrado")
        
        prof_dict = dict(profissional)
        profissional_id = prof_dict['id']
        
        # Buscar experiências (se a tabela existir)
        experiencias = []
        try:
            cursor.execute("""
                SELECT * FROM experiencias_profissionais 
                WHERE profissional_id = ? 
                ORDER BY data_inicio DESC
            """, (profissional_id,))
            experiencias = [dict(exp) for exp in cursor.fetchall()]
        except:
            pass
        
        # Buscar formações (se a tabela existir)
        formacoes = []
        try:
            cursor.execute("""
                SELECT * FROM formacoes_academicas 
                WHERE profissional_id = ? 
                ORDER BY data_inicio DESC
            """, (profissional_id,))
            formacoes = [dict(form) for form in cursor.fetchall()]
        except:
            pass
        
        conn.close()
        
        # Parse JSON fields
        if prof_dict.get('habilidades_esg'):
            try:
                prof_dict['habilidades_esg'] = json.loads(prof_dict['habilidades_esg'])
            except:
                prof_dict['habilidades_esg'] = []
        
        if prof_dict.get('ods_interesse'):
            try:
                prof_dict['ods_interesse'] = json.loads(prof_dict['ods_interesse'])
            except:
                prof_dict['ods_interesse'] = []
        
        if prof_dict.get('certificacoes'):
            try:
                prof_dict['certificacoes'] = json.loads(prof_dict['certificacoes'])
            except:
                prof_dict['certificacoes'] = []
        
        return {
            "perfil": prof_dict,
            "experiencias": experiencias,
            "formacoes": formacoes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/me/candidaturas")
async def obter_minhas_candidaturas(current_user: UserResponse = Depends(get_current_active_user)):
    """Lista candidaturas do profissional logado"""
    if not get_current_active_user:
        raise HTTPException(status_code=501, detail="Autenticação não disponível")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar profissional vinculado ao usuário
        cursor.execute("""
            SELECT profissional_id FROM users WHERE id = ?
        """, (current_user.id,))
        
        result = cursor.fetchone()
        if not result or not result['profissional_id']:
            conn.close()
            raise HTTPException(status_code=404, detail="Profissional não vinculado ao usuário")
        
        profissional_id = result['profissional_id']
        
        # Buscar candidaturas com dados da vaga e empresa
        cursor.execute("""
            SELECT 
                c.id, c.vaga_id, c.compatibilidade_score, c.status, 
                c.data_candidatura, c.data_atualizacao,
                v.titulo as vaga_titulo, v.descricao as vaga_descricao,
                v.salario_min, v.salario_max, v.nivel_experiencia,
                v.localizacao_cidade, v.localizacao_uf, v.remoto, v.hibrido,
                v.ods_tags, v.habilidades_requeridas,
                e.nome_fantasia as empresa_nome, e.razao_social as empresa_razao
            FROM candidaturas_esg c
            INNER JOIN vagas_esg v ON c.vaga_id = v.id
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE c.profissional_id = ?
            ORDER BY c.data_candidatura DESC
        """, (profissional_id,))
        
        candidaturas = []
        for row in cursor.fetchall():
            cand = dict(row)
            
            # Parse JSON fields
            if cand.get('ods_tags'):
                try:
                    cand['ods_tags'] = json.loads(cand['ods_tags'])
                except:
                    cand['ods_tags'] = []
            
            if cand.get('habilidades_requeridas'):
                try:
                    cand['habilidades_requeridas'] = json.loads(cand['habilidades_requeridas'])
                except:
                    cand['habilidades_requeridas'] = []
            
            candidaturas.append(cand)
        
        conn.close()
        
        # Estatísticas
        total = len(candidaturas)
        por_status = {}
        for cand in candidaturas:
            status = cand['status']
            por_status[status] = por_status.get(status, 0) + 1
        
        score_medio = sum(c['compatibilidade_score'] for c in candidaturas) / total if total > 0 else 0
        
        return {
            "candidaturas": candidaturas,
            "estatisticas": {
                "total": total,
                "por_status": por_status,
                "score_medio": round(score_medio, 1)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/me/recomendacoes")
async def obter_vagas_recomendadas(
    current_user: UserResponse = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=50)
):
    """Lista vagas recomendadas para o profissional logado baseado em ML"""
    if not get_current_active_user:
        raise HTTPException(status_code=501, detail="Autenticação não disponível")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar profissional vinculado ao usuário
        cursor.execute("""
            SELECT p.* FROM profissionais_esg p
            INNER JOIN users u ON p.id = u.profissional_id
            WHERE u.id = ? AND p.status = 'ativo'
        """, (current_user.id,))
        
        profissional = cursor.fetchone()
        if not profissional:
            conn.close()
            raise HTTPException(status_code=404, detail="Perfil de profissional não encontrado")
        
        prof_dict = dict(profissional)
        profissional_id = prof_dict['id']
        
        # Parse habilidades e ODS
        habilidades_prof = []
        if prof_dict.get('habilidades_esg'):
            try:
                habilidades_prof = json.loads(prof_dict['habilidades_esg'])
            except:
                pass
        
        ods_prof = []
        if prof_dict.get('ods_interesse'):
            try:
                ods_prof = json.loads(prof_dict['ods_interesse'])
            except:
                pass
        
        # Buscar vagas ativas que ainda não foram candidatadas
        cursor.execute("""
            SELECT 
                v.id, v.titulo, v.descricao, v.salario_min, v.salario_max,
                v.nivel_experiencia, v.localizacao_cidade, v.localizacao_uf,
                v.remoto, v.hibrido, v.ods_tags, v.habilidades_requeridas,
                v.criada_em,
                e.nome_fantasia as empresa_nome, e.razao_social as empresa_razao,
                e.score_verde as empresa_score
            FROM vagas_esg v
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE v.status = 'ativa'
            AND v.id NOT IN (
                SELECT vaga_id FROM candidaturas_esg WHERE profissional_id = ?
            )
            ORDER BY v.criada_em DESC
            LIMIT 50
        """, (profissional_id,))
        
        vagas = []
        for row in cursor.fetchall():
            vaga = dict(row)
            
            # Parse JSON fields
            habilidades_vaga = []
            if vaga.get('habilidades_requeridas'):
                try:
                    habilidades_vaga = json.loads(vaga['habilidades_requeridas'])
                except:
                    pass
            
            ods_vaga = []
            if vaga.get('ods_tags'):
                try:
                    ods_vaga = json.loads(vaga['ods_tags'])
                except:
                    pass
            
            # Calcular score de compatibilidade simples
            score = 0.0
            
            # Habilidades (50%)
            if habilidades_prof and habilidades_vaga:
                habilidades_match = len(set(habilidades_prof) & set(habilidades_vaga))
                habilidades_total = len(set(habilidades_vaga))
                if habilidades_total > 0:
                    score += (habilidades_match / habilidades_total) * 50
            
            # ODS (30%)
            if ods_prof and ods_vaga:
                ods_match = len(set(ods_prof) & set(ods_vaga))
                ods_total = len(set(ods_vaga))
                if ods_total > 0:
                    score += (ods_match / ods_total) * 30
            
            # Localização (20%)
            if prof_dict.get('aceita_remoto') and vaga.get('remoto'):
                score += 20
            elif prof_dict.get('localizacao_uf') == vaga.get('localizacao_uf'):
                score += 15
            
            vaga['compatibilidade_score'] = round(score, 1)
            vaga['habilidades_requeridas'] = habilidades_vaga
            vaga['ods_tags'] = ods_vaga
            
            vagas.append(vaga)
        
        conn.close()
        
        # Ordenar por score e limitar
        vagas_ordenadas = sorted(vagas, key=lambda x: x['compatibilidade_score'], reverse=True)[:limit]
        
        return {
            "vagas_recomendadas": vagas_ordenadas,
            "total_disponiveis": len(vagas),
            "algoritmo": "matching_ml_v1",
            "criterios": {
                "habilidades": "50%",
                "ods_alinhamento": "30%",
                "localizacao": "20%"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


class ProfissionalUpdate(BaseModel):
    """Schema para atualização de perfil"""
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    localizacao_uf: Optional[str] = None
    aceita_remoto: Optional[bool] = None
    disponivel_mudanca: Optional[bool] = None
    cargo_atual: Optional[str] = None
    empresa_atual: Optional[str] = None
    anos_experiencia_esg: Optional[int] = None
    formacao_nivel: Optional[str] = None
    formacao_area: Optional[str] = None
    habilidades_esg: Optional[List[str]] = None
    ods_interesse: Optional[List[int]] = None
    certificacoes: Optional[List[str]] = None
    areas_interesse: Optional[List[str]] = None
    pretensao_salarial_min: Optional[float] = None
    pretensao_salarial_max: Optional[float] = None
    resumo_profissional: Optional[str] = None
    motivacao_esg: Optional[str] = None
    disponibilidade: Optional[str] = None


@router.put("/me/perfil")
async def atualizar_meu_perfil(
    dados: ProfissionalUpdate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualiza perfil do profissional logado"""
    if not get_current_active_user:
        raise HTTPException(status_code=501, detail="Autenticação não disponível")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar profissional vinculado ao usuário
        cursor.execute("""
            SELECT profissional_id FROM users WHERE id = ?
        """, (current_user.id,))
        
        result = cursor.fetchone()
        if not result or not result['profissional_id']:
            conn.close()
            raise HTTPException(status_code=404, detail="Profissional não vinculado ao usuário")
        
        profissional_id = result['profissional_id']
        
        # Construir query dinâmica
        campos_update = []
        valores = []
        
        dados_dict = dados.dict(exclude_unset=True)
        
        for campo, valor in dados_dict.items():
            if valor is not None:
                # Converter listas para JSON
                if isinstance(valor, list):
                    valor = json.dumps(valor, ensure_ascii=False)
                campos_update.append(f"{campo} = ?")
                valores.append(valor)
        
        if not campos_update:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        # Adicionar timestamp de atualização
        campos_update.append("atualizado_em = CURRENT_TIMESTAMP")
        
        # Executar update
        query = f"""
            UPDATE profissionais_esg 
            SET {', '.join(campos_update)}
            WHERE id = ?
        """
        valores.append(profissional_id)
        
        cursor.execute(query, valores)
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Perfil atualizado com sucesso",
            "campos_atualizados": list(dados_dict.keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/me/estatisticas")
async def obter_minhas_estatisticas(current_user: UserResponse = Depends(get_current_active_user)):
    """Estatísticas pessoais do profissional logado"""
    if not get_current_active_user:
        raise HTTPException(status_code=501, detail="Autenticação não disponível")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar profissional vinculado ao usuário
        cursor.execute("""
            SELECT profissional_id FROM users WHERE id = ?
        """, (current_user.id,))
        
        result = cursor.fetchone()
        if not result or not result['profissional_id']:
            conn.close()
            return {
                "candidaturas_enviadas": 0,
                "candidaturas_por_status": {},
                "score_medio_compatibilidade": 0,
                "vagas_disponiveis": 0,
                "perfil_completo": False,
                "visualizacoes_perfil": 0
            }
        
        profissional_id = result['profissional_id']
        
        # Total de candidaturas
        cursor.execute("""
            SELECT COUNT(*) as total FROM candidaturas_esg WHERE profissional_id = ?
        """, (profissional_id,))
        total_candidaturas = cursor.fetchone()['total']
        
        # Por status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM candidaturas_esg 
            WHERE profissional_id = ?
            GROUP BY status
        """, (profissional_id,))
        por_status = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Score médio
        cursor.execute("""
            SELECT AVG(compatibilidade_score) as media 
            FROM candidaturas_esg 
            WHERE profissional_id = ?
        """, (profissional_id,))
        score_medio = cursor.fetchone()['media'] or 0
        
        # Vagas disponíveis (que ainda não candidatou)
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM vagas_esg 
            WHERE status = 'ativa' 
            AND id NOT IN (
                SELECT vaga_id FROM candidaturas_esg WHERE profissional_id = ?
            )
        """, (profissional_id,))
        vagas_disponiveis = cursor.fetchone()['total']
        
        # Dados do perfil
        cursor.execute("""
            SELECT perfil_completo, visualizacoes_perfil 
            FROM profissionais_esg 
            WHERE id = ?
        """, (profissional_id,))
        perfil_data = cursor.fetchone()
        
        conn.close()
        
        return {
            "candidaturas_enviadas": total_candidaturas,
            "candidaturas_por_status": por_status,
            "score_medio_compatibilidade": round(score_medio, 1),
            "vagas_disponiveis": vagas_disponiveis,
            "perfil_completo": bool(perfil_data['perfil_completo']) if perfil_data else False,
            "visualizacoes_perfil": perfil_data['visualizacoes_perfil'] if perfil_data else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
