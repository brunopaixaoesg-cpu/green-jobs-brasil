"""
Router de Vagas ESG - Green Jobs Brasil
"""
Router de Vagas ESG - Green Jobs Brasil
Endpoints para gerenciamento de vagas verdes
Arquivo limpo: normaliza nomes de tabelas/colunas e corrige indentação/erros.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

from api.db import get_db

router = APIRouter(prefix="/api/vagas", tags=["Vagas ESG"])


# ============= SCHEMAS PYDANTIC =============
class VagaCreate(BaseModel):
    cnpj: str = Field(..., description="CNPJ da empresa")
    titulo: str = Field(..., min_length=5, max_length=200)
    descricao: str = Field(..., min_length=20)
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    ods_tags: Optional[List[int]] = None
    habilidades_requeridas: Optional[List[str]] = None
    nivel_experiencia: str
    tipo_contratacao: str
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    remoto: bool = False
    hibrido: bool = False
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    publicada_por: str


class VagaUpdate(BaseModel):
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
    id: int
    cnpj: str
    titulo: str
    descricao: Optional[str] = None
    requisitos_adicionais: Optional[str] = None
    beneficios: Optional[str] = None
    ods_tags: Optional[List[int]] = None
    habilidades_requeridas: Optional[List[str]] = None
    nivel_experiencia: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    localizacao_uf: Optional[str] = None
    localizacao_cidade: Optional[str] = None
    remoto: Optional[bool] = False
    hibrido: Optional[bool] = False
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    status: Optional[str] = 'ativa'
    vagas_disponiveis: Optional[int] = 1
    candidaturas_recebidas: Optional[int] = 0
    diferenciais: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None


# ============= ENDPOINTS =============


@router.get("/", response_model=List[VagaResponse])
async def listar_vagas(
    status: Optional[str] = Query('ativa', description="Filtrar por status"),
    uf: Optional[str] = Query(None, description="Filtrar por UF"),
    remoto: Optional[bool] = Query(None, description="Apenas remotas"),
    nivel: Optional[str] = Query(None, description="Nível de experiência"),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
):
    """Listar vagas com filtros opcionais"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        query = "SELECT * FROM vagas WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if uf:
            query += " AND localizacao_uf = ?"
            params.append(uf)

        if remoto is not None:
            query += " AND remoto = ?"
            params.append(1 if remoto else 0)

        if nivel:
            query += " AND nivel_experiencia = ?"
            params.append(nivel)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        result = []
        for row in rows:
            vaga = dict(row)
            # parse JSON fields if present
            try:
                vaga['ods_tags'] = json.loads(vaga.get('ods_tags') or '[]')
            except Exception:
                vaga['ods_tags'] = []
            try:
                vaga['habilidades_requeridas'] = json.loads(vaga.get('habilidades_requeridas') or '[]')
            except Exception:
                vaga['habilidades_requeridas'] = []

            result.append(vaga)

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vagas: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.get("/{vaga_id}", response_model=VagaResponse)
async def obter_vaga(vaga_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT v.*, e.razao_social as empresa_nome
            FROM vagas v
            LEFT JOIN empresas_esg e ON v.cnpj = e.cnpj
            WHERE v.id = ?
            """,
            (vaga_id,),
        )

        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")

        vaga = dict(row)
        try:
            vaga['ods_tags'] = json.loads(vaga.get('ods_tags') or '[]')
        except Exception:
            vaga['ods_tags'] = []
        try:
            vaga['habilidades_requeridas'] = json.loads(vaga.get('habilidades_requeridas') or '[]')
        except Exception:
            vaga['habilidades_requeridas'] = []

        return vaga
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter vaga: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.post("/", response_model=VagaResponse, status_code=201)
async def criar_vaga(vaga: VagaCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Verificar se empresa existe (tabela canonical: empresas_esg)
        cursor.execute("SELECT razao_social FROM empresas_esg WHERE cnpj = ?", (vaga.cnpj,))
        empresa = cursor.fetchone()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada. Cadastre a empresa primeiro.")

        cursor.execute(
            """
            INSERT INTO vagas (
                cnpj, titulo, descricao, requisitos_adicionais, beneficios,
                ods_tags, habilidades_requeridas, nivel_experiencia, tipo_contratacao,
                localizacao_uf, localizacao_cidade, remoto, hibrido,
                salario_min, salario_max, status, vagas_disponiveis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa', 1)
            """,
            (
                vaga.cnpj,
                vaga.titulo,
                vaga.descricao,
                vaga.requisitos,
                vaga.beneficios,
                json.dumps(vaga.ods_tags or []),
                json.dumps(vaga.habilidades_requeridas or []),
                vaga.nivel_experiencia,
                vaga.tipo_contratacao,
                vaga.localizacao_uf,
                vaga.localizacao_cidade,
                1 if vaga.remoto else 0,
                1 if vaga.hibrido else 0,
                vaga.salario_min,
                vaga.salario_max,
            ),
        )

        vaga_id = cursor.lastrowid
        conn.commit()

        return await obter_vaga(vaga_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar vaga: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.put("/{vaga_id}", response_model=VagaResponse)
async def atualizar_vaga(vaga_id: int, vaga_update: VagaUpdate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM vagas WHERE id = ?", (vaga_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vaga não encontrada")

        updates = []
        params = []
        data = vaga_update.dict(exclude_unset=True)
        for campo, valor in data.items():
            if campo in ['ods_tags', 'habilidades_requeridas']:
                updates.append(f"{campo} = ?")
                params.append(json.dumps(valor or []))
            elif isinstance(valor, bool):
                updates.append(f"{campo} = ?")
                params.append(1 if valor else 0)
            else:
                updates.append(f"{campo} = ?")
                params.append(valor)

        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        query = f"UPDATE vagas SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params.append(vaga_id)
        cursor.execute(query, params)
        conn.commit()

        return await obter_vaga(vaga_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar vaga: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.delete("/{vaga_id}", status_code=204)
async def deletar_vaga(vaga_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("UPDATE vagas SET status = 'cancelada', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (vaga_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")

        conn.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar vaga: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.get("/stats/resumo")
async def estatisticas_vagas():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'ativa' THEN 1 ELSE 0 END) as ativas,
                SUM(CASE WHEN status = 'pausada' THEN 1 ELSE 0 END) as pausadas,
                SUM(CASE WHEN status = 'fechada' THEN 1 ELSE 0 END) as fechadas,
                SUM(CASE WHEN remoto = 1 THEN 1 ELSE 0 END) as remotas,
                SUM(vagas_disponiveis) as total_vagas_disponiveis,
                SUM(candidaturas_recebidas) as total_candidaturas
            FROM vagas
            """
        )

        row = cursor.fetchone()
        stats = dict(row) if row else {}

        cursor.execute("SELECT ods_tags FROM vagas WHERE status = 'ativa'")
        ods_counter = {}
        for r in cursor.fetchall():
            try:
                ods_list = json.loads(r['ods_tags'] or '[]')
            except Exception:
                ods_list = []
            for ods in ods_list:
                ods_counter[ods] = ods_counter.get(ods, 0) + 1

        stats['vagas_por_ods'] = ods_counter
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")
    finally:
        if conn:
            conn.close()
