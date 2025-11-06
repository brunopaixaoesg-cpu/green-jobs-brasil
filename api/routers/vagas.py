"""
Router de Vagas ESG - Green Jobs Brasil
Endpoints para gerenciamento de vagas verdes
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
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


@router.get("/")
async def listar_vagas(
    # Paginação
    page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
    limit: int = Query(20, ge=1, le=100, description="Items por página (máx 100)"),
    
    # Filtros compostos
    status: Optional[str] = Query(None, description="Status da vaga (aberta, fechada, pausada)"),
    ods: Optional[str] = Query(None, description="ODS (ex: 7,13,15)"),
    uf: Optional[str] = Query(None, description="Estados (ex: SP,RJ,MG)"),
    area: Optional[str] = Query(None, description="Área/competências"),
    remoto: Optional[bool] = Query(None, description="Apenas remotas"),
    hibrido: Optional[bool] = Query(None, description="Aceita híbrido"),
    nivel: Optional[str] = Query(None, description="Nível experiência (junior,pleno,senior)"),
    salario_min: Optional[float] = Query(None, ge=0, description="Salário mínimo"),
    tipo_contratacao: Optional[str] = Query(None, description="Tipo contratação (CLT,PJ,etc)"),
    
    # Sorting
    sort: Optional[str] = Query(None, description="Campo ordenação (titulo,salario_min,created_at)"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Direção ordenação")
):
    """
    Lista vagas com filtros compostos, paginação e ordenação
    
    **Filtros Compostos:**
    - `status`: Status da vaga (ativa, fechada, pausada)
    - `ods`: ODS relacionados (valores separados por vírgula: 7,13,15)
    - `uf`: Estados (SP,RJ,MG)
    - `area`: Área ou competências necessárias
    - `remoto`: Apenas vagas remotas (true/false)
    - `hibrido`: Aceita trabalho híbrido (true/false)
    - `nivel`: Nível de experiência (junior, pleno, senior)
    - `salario_min`: Salário mínimo desejado
    - `tipo_contratacao`: Tipo de contratação
    
    **Paginação:**
    - `page`: Número da página (default: 1)
    - `limit`: Items por página (default: 20, máx: 100)
    
    **Ordenação:**
    - `sort`: Campo para ordenar (titulo, salario_min, salario_max, created_at)
    - `order`: Direção (asc ou desc)
    
    **Exemplo:**
    ```
    /api/vagas?ods=7,13&uf=SP,RJ&remoto=true&salario_min=5000&sort=salario_max&order=desc&page=1&limit=20
    ```
    """
    try:
        from api.utils.pagination import parse_comma_separated, create_pagination_headers
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Query base
        base_query = "SELECT * FROM vagas WHERE 1=1"
        count_query = "SELECT COUNT(*) as total FROM vagas WHERE 1=1"
        params = []
        
        # === APLICAR FILTROS ===
        
        # Filtro: Status
        if status:
            base_query += " AND status = ?"
            count_query += " AND status = ?"
            params.append(status)
        
        # Filtro: UF (múltiplos valores)
        if uf:
            ufs = parse_comma_separated(uf)
            if ufs:
                placeholders = ','.join('?' * len(ufs))
                base_query += f" AND localizacao_uf IN ({placeholders})"
                count_query += f" AND localizacao_uf IN ({placeholders})"
                params.extend(ufs)
        
        # Filtro: Remoto
        if remoto is not None:
            base_query += " AND remoto = ?"
            count_query += " AND remoto = ?"
            params.append(1 if remoto else 0)
        
        # Filtro: Híbrido
        if hibrido is not None:
            base_query += " AND hibrido = ?"
            count_query += " AND hibrido = ?"
            params.append(1 if hibrido else 0)
        
        # Filtro: Nível experiência
        if nivel:
            base_query += " AND nivel_experiencia = ?"
            count_query += " AND nivel_experiencia = ?"
            params.append(nivel.lower())
        
        # Filtro: Salário mínimo
        if salario_min is not None:
            base_query += " AND (salario_max IS NULL OR salario_max >= ?)"
            count_query += " AND (salario_max IS NULL OR salario_max >= ?)"
            params.append(salario_min)
        
        # Filtro: Tipo contratação
        if tipo_contratacao:
            base_query += " AND tipo_contratacao = ?"
            count_query += " AND tipo_contratacao = ?"
            params.append(tipo_contratacao)
        
        # Filtro: ODS (busca em campo JSON/texto)
        ods_filters = []
        if ods:
            ods_list = parse_comma_separated(ods)
            for ods_num in ods_list:
                ods_filters.append(f"ods_tags LIKE '%{ods_num}%'")
        
        if ods_filters:
            ods_condition = " OR ".join(ods_filters)
            base_query += f" AND ({ods_condition})"
            count_query += f" AND ({ods_condition})"
        
        # Filtro: Área/competências
        if area:
            areas = parse_comma_separated(area)
            area_filters = []
            for a in areas:
                area_filters.append(f"habilidades_requeridas LIKE '%{a}%'")
            
            if area_filters:
                area_condition = " OR ".join(area_filters)
                base_query += f" AND ({area_condition})"
                count_query += f" AND ({area_condition})"
        
        # === CONTAR TOTAL (antes de paginação) ===
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # === APLICAR ORDENAÇÃO ===
        campos_permitidos = ['titulo', 'salario_min', 'salario_max', 'created_at', 'nivel_experiencia']
        sort_field = sort if sort in campos_permitidos else 'created_at'
        order_direction = order.upper()
        
        base_query += f" ORDER BY {sort_field} {order_direction}"
        
        # === APLICAR PAGINAÇÃO ===
        offset = (page - 1) * limit
        base_query += f" LIMIT {limit} OFFSET {offset}"
        
        # Executar query
        cursor.execute(base_query, params)
        vagas = cursor.fetchall()
        
        # Processar resultados
        result = []
        for vaga in vagas:
            vaga_dict = dict(vaga)
            
            # Parse JSON fields
            try:
                vaga_dict['ods_tags'] = json.loads(vaga_dict.get('ods_tags') or '[]')
            except:
                vaga_dict['ods_tags'] = []
            
            try:
                vaga_dict['habilidades_requeridas'] = json.loads(vaga_dict.get('habilidades_requeridas') or '[]')
            except:
                vaga_dict['habilidades_requeridas'] = []
            
            # Buscar dados da empresa
            try:
                cursor.execute("""
                    SELECT razao_social, nome_fantasia, score_verde
                    FROM empresas_esg
                    WHERE cnpj = ?
                """, (vaga_dict['cnpj'],))
                empresa = cursor.fetchone()
                
                if empresa:
                    vaga_dict['empresa_nome'] = empresa['nome_fantasia'] or empresa['razao_social']
                    vaga_dict['empresa_score'] = empresa.get('score_verde', 0)
            except Exception as e:
                print(f"⚠️ Erro ao buscar empresa {vaga_dict['cnpj']}: {e}")
                # Continuar sem dados da empresa
                pass
            
            # Contar candidaturas
            try:
                cursor.execute("""
                    SELECT COUNT(*) as total_candidaturas
                    FROM candidaturas
                    WHERE vaga_id = ?
                """, (vaga_dict['id'],))
                cand_stats = cursor.fetchone()
                vaga_dict['total_candidaturas'] = cand_stats['total_candidaturas'] or 0
            except Exception as e:
                print(f"⚠️ Erro ao contar candidaturas da vaga {vaga_dict['id']}: {e}")
                vaga_dict['total_candidaturas'] = 0
            
            result.append(vaga_dict)
        
        conn.close()
        
        # Calcular páginas
        pages = (total + limit - 1) // limit
        
        # Metadados de paginação
        meta = {
            "total": total,
            "page": page,
            "pages": pages,
            "limit": limit,
            "has_next": page < pages,
            "has_prev": page > 1
        }
        
        # Headers de paginação
        headers = create_pagination_headers(meta)
        
        return JSONResponse(
            content={
                "data": result,
                "pagination": meta,
                "filtros_aplicados": {
                    "status": status,
                    "ods": parse_comma_separated(ods) if ods else None,
                    "uf": parse_comma_separated(uf) if uf else None,
                    "area": parse_comma_separated(area) if area else None,
                    "remoto": remoto,
                    "hibrido": hibrido,
                    "nivel": nivel,
                    "salario_min": salario_min,
                    "tipo_contratacao": tipo_contratacao
                },
                "ordenacao": {
                    "campo": sort_field,
                    "direcao": order
                }
            },
            headers=headers
        )
        
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(f"❌ Erro em listar_vagas: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


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
