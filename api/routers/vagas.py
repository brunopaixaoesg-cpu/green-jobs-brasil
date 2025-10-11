"""
Router de Vagas ESG - Green Jobs Brasil
Endpoints para gerenciamento de vagas verdes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import sqlite3
import json
import os

router = APIRouter(prefix="/api/vagas", tags=["Vagas ESG"])

# Configuração do banco
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gjb_dev.db")

def get_db():
    """Conexão com banco SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============= SCHEMAS PYDANTIC =============

class VagaCreate(BaseModel):
    """Schema para criar vaga"""
    cnpj: str = Field(..., description="CNPJ da empresa")
    titulo: str = Field(..., min_length=5, max_length=200, description="Título da vaga")
    descricao: str = Field(..., min_length=20, description="Descrição completa")
    requisitos: Optional[str] = Field(None, description="Requisitos da vaga")
    beneficios: Optional[str] = Field(None, description="Benefícios oferecidos")
    
    ods_tags: List[int] = Field([], description="Lista de ODS relacionados")
    habilidades_requeridas: List[str] = Field([], description="Habilidades ESG necessárias")
    nivel_experiencia: str = Field(..., description="junior, pleno, senior, especialista")
    tipo_contratacao: str = Field(..., description="CLT, PJ, temporario, estagio, freelance")
    
    localizacao_uf: Optional[str] = Field(None, max_length=2, description="UF da vaga")
    localizacao_cidade: Optional[str] = Field(None, description="Cidade")
    remoto: bool = Field(False, description="Trabalho remoto")
    hibrido: bool = Field(False, description="Trabalho híbrido")
    
    salario_min: Optional[float] = Field(None, ge=0, description="Salário mínimo")
    salario_max: Optional[float] = Field(None, ge=0, description="Salário máximo")
    
    publicada_por: str = Field(..., description="Email de quem publicou")

class VagaUpdate(BaseModel):
    """Schema para atualizar vaga"""
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    ods_tags: Optional[List[int]] = None
    habilidades_requeridas: Optional[List[str]] = None
    nivel_experiencia: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    remoto: Optional[bool] = None
    hibrido: Optional[bool] = None
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    status: Optional[str] = None

class VagaResponse(BaseModel):
    """Schema de resposta"""
    id: int
    cnpj: str
    empresa_nome: Optional[str]
    titulo: str
    descricao: str
    requisitos: Optional[str]
    beneficios: Optional[str]
    ods_tags: List[int]
    habilidades_requeridas: List[str]
    nivel_experiencia: str
    tipo_contratacao: str
    localizacao_uf: Optional[str]
    localizacao_cidade: Optional[str]
    remoto: bool
    hibrido: bool
    salario_min: Optional[float]
    salario_max: Optional[float]
    status: str
    visualizacoes: int
    candidaturas: int
    publicada_por: str
    data_publicacao: Optional[str]
    criada_em: str
    atualizada_em: str

# ============= ENDPOINTS =============

@router.get("/", response_model=List[VagaResponse])
async def listar_vagas(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    uf: Optional[str] = Query(None, description="Filtrar por UF"),
    remoto: Optional[bool] = Query(None, description="Apenas remotas"),
    ods: Optional[int] = Query(None, description="Filtrar por ODS"),
    nivel: Optional[str] = Query(None, description="Nível de experiência"),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Listar vagas com filtros opcionais"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Query base
        query = """
            SELECT v.*, e.razao_social as empresa_nome
            FROM vagas_esg v
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE 1=1
        """
        params = []
        
        # Aplicar filtros
        if status:
            query += " AND v.status = ?"
            params.append(status)
        
        if uf:
            query += " AND v.localizacao_uf = ?"
            params.append(uf)
        
        if remoto is not None:
            query += " AND v.remoto = ?"
            params.append(1 if remoto else 0)
        
        if nivel:
            query += " AND v.nivel_experiencia = ?"
            params.append(nivel)
        
        # Ordenar por mais recentes
        query += " ORDER BY v.data_publicacao DESC, v.criada_em DESC"
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        vagas = []
        for row in rows:
            vaga_dict = dict(row)
            
            # Parse JSON fields
            vaga_dict['ods_tags'] = json.loads(vaga_dict['ods_tags']) if vaga_dict['ods_tags'] else []
            vaga_dict['habilidades_requeridas'] = json.loads(vaga_dict['habilidades_requeridas']) if vaga_dict['habilidades_requeridas'] else []
            
            # Filtro por ODS (se aplicável)
            if ods and ods not in vaga_dict['ods_tags']:
                continue
            
            vagas.append(vaga_dict)
        
        conn.close()
        return vagas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vagas: {str(e)}")

@router.get("/{vaga_id}", response_model=VagaResponse)
async def obter_vaga(vaga_id: int):
    """Obter detalhes de uma vaga específica"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Incrementar visualizações
        cursor.execute("UPDATE vagas_esg SET visualizacoes = visualizacoes + 1 WHERE id = ?", (vaga_id,))
        conn.commit()
        
        # Buscar vaga
        cursor.execute("""
            SELECT v.*, e.razao_social as empresa_nome
            FROM vagas_esg v
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE v.id = ?
        """, (vaga_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        
        vaga_dict = dict(row)
        vaga_dict['ods_tags'] = json.loads(vaga_dict['ods_tags']) if vaga_dict['ods_tags'] else []
        vaga_dict['habilidades_requeridas'] = json.loads(vaga_dict['habilidades_requeridas']) if vaga_dict['habilidades_requeridas'] else []
        
        return vaga_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter vaga: {str(e)}")

@router.post("/", response_model=VagaResponse, status_code=201)
async def criar_vaga(vaga: VagaCreate):
    """Criar nova vaga ESG"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Verificar se empresa existe
        cursor.execute("SELECT razao_social FROM empresas_verdes WHERE cnpj = ?", (vaga.cnpj,))
        empresa = cursor.fetchone()
        
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada. Cadastre a empresa primeiro.")
        
        # Inserir vaga
        cursor.execute("""
            INSERT INTO vagas_esg (
                cnpj, empresa_nome, titulo, descricao, requisitos, beneficios,
                ods_tags, habilidades_requeridas, nivel_experiencia, tipo_contratacao,
                localizacao_uf, localizacao_cidade, remoto, hibrido,
                salario_min, salario_max, publicada_por, data_publicacao, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, DATE('now'), 'ativa')
        """, (
            vaga.cnpj,
            empresa['razao_social'],
            vaga.titulo,
            vaga.descricao,
            vaga.requisitos,
            vaga.beneficios,
            json.dumps(vaga.ods_tags),
            json.dumps(vaga.habilidades_requeridas),
            vaga.nivel_experiencia,
            vaga.tipo_contratacao,
            vaga.localizacao_uf,
            vaga.localizacao_cidade,
            1 if vaga.remoto else 0,
            1 if vaga.hibrido else 0,
            vaga.salario_min,
            vaga.salario_max,
            vaga.publicada_por
        ))
        
        vaga_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Retornar vaga criada
        return await obter_vaga(vaga_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar vaga: {str(e)}")

@router.put("/{vaga_id}", response_model=VagaResponse)
async def atualizar_vaga(vaga_id: int, vaga_update: VagaUpdate):
    """Atualizar vaga existente"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Verificar se vaga existe
        cursor.execute("SELECT id FROM vagas_esg WHERE id = ?", (vaga_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        
        # Construir query de update dinamicamente
        updates = []
        params = []
        
        update_data = vaga_update.dict(exclude_unset=True)
        
        for campo, valor in update_data.items():
            if valor is not None:
                if campo in ['ods_tags', 'habilidades_requeridas']:
                    updates.append(f"{campo} = ?")
                    params.append(json.dumps(valor))
                elif isinstance(valor, bool):
                    updates.append(f"{campo} = ?")
                    params.append(1 if valor else 0)
                else:
                    updates.append(f"{campo} = ?")
                    params.append(valor)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        # Executar update
        query = f"UPDATE vagas_esg SET {', '.join(updates)} WHERE id = ?"
        params.append(vaga_id)
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return await obter_vaga(vaga_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar vaga: {str(e)}")

@router.delete("/{vaga_id}", status_code=204)
async def deletar_vaga(vaga_id: int):
    """Deletar vaga (soft delete - muda status para cancelada)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE vagas_esg SET status = 'cancelada' WHERE id = ?", (vaga_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        
        conn.commit()
        conn.close()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar vaga: {str(e)}")

@router.get("/stats/resumo")
async def estatisticas_vagas():
    """Estatísticas gerais de vagas"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'ativa' THEN 1 ELSE 0 END) as ativas,
                SUM(CASE WHEN status = 'pausada' THEN 1 ELSE 0 END) as pausadas,
                SUM(CASE WHEN status = 'fechada' THEN 1 ELSE 0 END) as fechadas,
                SUM(CASE WHEN remoto = 1 THEN 1 ELSE 0 END) as remotas,
                AVG(visualizacoes) as media_visualizacoes,
                SUM(candidaturas) as total_candidaturas
            FROM vagas_esg
        """)
        
        stats = dict(cursor.fetchone())
        
        # Vagas por ODS
        cursor.execute("SELECT ods_tags FROM vagas_esg WHERE status = 'ativa'")
        ods_counter = {}
        for row in cursor.fetchall():
            if row['ods_tags']:
                ods_list = json.loads(row['ods_tags'])
                for ods in ods_list:
                    ods_counter[ods] = ods_counter.get(ods, 0) + 1
        
        stats['vagas_por_ods'] = ods_counter
        
        conn.close()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")
