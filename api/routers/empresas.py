"""
Router de Empresas ESG - Green Jobs Brasil
Endpoints para gerenciamento de empresas e suas vagas
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import hashlib
import os

from api.db import get_db

router = APIRouter(prefix="/empresas", tags=["Empresas ESG"])

# Templates
templates = Jinja2Templates(directory="api/templates")

# --- Cadastro de empresa (endpoint de API) ---
from fastapi import Body
import requests

class EmpresaCadastro(BaseModel):
    cnpj: str
    email: str
    senha: str
    telefone: str = ""
    website: str = ""
    descricao: str = ""
    logo_url: str = ""


@router.post("/api/cadastro")
async def cadastrar_empresa(dados: EmpresaCadastro = Body(...)):
    """Cadastro de empresa ESG com validação de CNPJ e Receita Federal"""
    conn = get_db()
    cursor = conn.cursor()
    cnpj_clean = ''.join(filter(str.isdigit, dados.cnpj))
    # Verificar duplicidade
    cursor.execute("SELECT id FROM empresas_esg WHERE cnpj = ?", (dados.cnpj,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Empresa já cadastrada com esse CNPJ")

    # Consultar Receita Federal
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                razao_social = data.get('nome', '')
                nome_fantasia = data.get('fantasia', '')
                cidade = data.get('municipio', '')
                estado = data.get('uf', '')
                setor = (data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '')
            else:
                razao_social = nome_fantasia = cidade = estado = setor = ''
        else:
            razao_social = nome_fantasia = cidade = estado = setor = ''
    except Exception:
        razao_social = nome_fantasia = cidade = estado = setor = ''

    senha_hash = hashlib.sha256(dados.senha.encode()).hexdigest()
    cursor.execute("""
        INSERT INTO empresas_esg (cnpj, razao_social, nome_fantasia, email, senha_hash, telefone, website, descricao, logo_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (dados.cnpj, razao_social, nome_fantasia, dados.email, senha_hash, dados.telefone, dados.website, dados.descricao, dados.logo_url, 'ativa'))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Empresa cadastrada com sucesso", "cnpj": dados.cnpj, "razao_social": razao_social, "nome_fantasia": nome_fantasia}

# ==================== MODELS ====================

class LoginRequest(BaseModel):
    email: str
    senha: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    empresa_id: Optional[int] = None
    razao_social: Optional[str] = None

class EmpresaInfo(BaseModel):
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str]
    email: str
    cidade: Optional[str]
    estado: Optional[str]
    setor: Optional[str]
    total_vagas: int
    vagas_ativas: int
    total_candidaturas: int

class CandidaturaEmpresa(BaseModel):
    id: int
    vaga_id: int
    vaga_titulo: str
    profissional_id: int
    profissional_nome: str
    profissional_email: str
    compatibilidade_score: float
    status: str
    data_candidatura: datetime
    observacoes: Optional[str]

# ==================== ENDPOINTS ====================

@router.get("/login", response_class=HTMLResponse, name="empresa_login_page")
async def login_page(request: Request):
    """Página de login para empresas"""
    return templates.TemplateResponse("login_empresa.html", {"request": request})


@router.post("/api/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Autenticação de empresa"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Hash da senha
    senha_hash = hashlib.sha256(credentials.senha.encode()).hexdigest()
    
    # Buscar empresa
    cursor.execute("""
        SELECT id, razao_social, nome_fantasia, status 
        FROM empresas_esg 
        WHERE email=? AND senha_hash=?
    """, (credentials.email, senha_hash))
    
    empresa = cursor.fetchone()
    conn.close()
    
    if not empresa:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    if empresa['status'] != 'ativa':
        raise HTTPException(status_code=403, detail="Empresa inativa")
    
    return LoginResponse(
        success=True,
        message="Login realizado com sucesso",
        empresa_id=empresa['id'],
        razao_social=empresa['razao_social']
    )


@router.get("/dashboard", response_class=HTMLResponse, name="empresa_dashboard")
async def dashboard(request: Request, empresa_id: Optional[int] = None):
    """Dashboard da empresa"""
    if not empresa_id:
        # Redirecionar para login se não autenticado
        return templates.TemplateResponse("login_empresa.html", {"request": request})
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar dados da empresa
    cursor.execute("""
        SELECT e.*, 
               (SELECT COUNT(*) FROM vagas WHERE cnpj=e.cnpj) as total_vagas,
               (SELECT COUNT(*) FROM vagas WHERE cnpj=e.cnpj AND status='ativa') as vagas_ativas
        FROM empresas_esg e
        WHERE e.id=?
    """, (empresa_id,))
    
    empresa = cursor.fetchone()
    
    if not empresa:
        conn.close()
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    # Buscar vagas da empresa
    cursor.execute("""
        SELECT v.*, 
               (SELECT COUNT(*) FROM candidaturas_esg WHERE vaga_id=v.id) as total_candidaturas,
               (SELECT COUNT(*) FROM candidaturas_esg WHERE vaga_id=v.id AND status='pendente') as candidaturas_pendentes
        FROM vagas v
        WHERE v.cnpj=?
        ORDER BY v.created_at DESC
    """, (empresa['cnpj'],))
    
    vagas = cursor.fetchall()
    
    conn.close()
    
    return templates.TemplateResponse("dashboard_empresa.html", {
        "request": request,
        "empresa": dict(empresa),
        "vagas": [dict(v) for v in vagas]
    })


@router.get("/api/info/{empresa_id}", response_model=EmpresaInfo)
async def get_empresa_info(empresa_id: int):
    """Obter informações da empresa"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.*, 
               (SELECT COUNT(*) FROM vagas WHERE cnpj=e.cnpj) as total_vagas,
               (SELECT COUNT(*) FROM vagas WHERE cnpj=e.cnpj AND status='ativa') as vagas_ativas,
               (SELECT COUNT(*) FROM candidaturas_esg c 
                JOIN vagas v ON c.vaga_id=v.id 
                WHERE v.cnpj=e.cnpj) as total_candidaturas
        FROM empresas_esg e
        WHERE e.id=?
    """, (empresa_id,))
    
    empresa = cursor.fetchone()
    conn.close()
    
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    return EmpresaInfo(**dict(empresa))


@router.get("/api/candidaturas/{empresa_id}", response_model=List[CandidaturaEmpresa])
async def get_candidaturas(
    empresa_id: int,
    vaga_id: Optional[int] = None,
    status: Optional[str] = None,
    score_min: Optional[float] = None
):
    """Listar candidaturas recebidas pela empresa"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar CNPJ da empresa
    cursor.execute("SELECT cnpj FROM empresas_esg WHERE id=?", (empresa_id,))
    empresa = cursor.fetchone()
    
    if not empresa:
        conn.close()
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    # Query base
    query = """
        SELECT c.*, 
               v.titulo as vaga_titulo,
               p.nome_completo as profissional_nome,
               p.email as profissional_email
        FROM candidaturas_esg c
        JOIN vagas v ON c.vaga_id = v.id
        JOIN profissionais_esg p ON c.profissional_id = p.id
        WHERE v.cnpj = ?
    """
    params = [empresa['cnpj']]
    
    # Filtros opcionais
    if vaga_id:
        query += " AND c.vaga_id = ?"
        params.append(vaga_id)
    
    if status:
        query += " AND c.status = ?"
        params.append(status)
    
    if score_min:
        query += " AND c.compatibilidade_score >= ?"
        params.append(score_min)
    
    query += " ORDER BY c.compatibilidade_score DESC, c.data_candidatura DESC"
    
    cursor.execute(query, params)
    candidaturas = cursor.fetchall()
    conn.close()
    
    return [CandidaturaEmpresa(**dict(c)) for c in candidaturas]


@router.put("/api/candidatura/{candidatura_id}/status")
async def update_candidatura_status(
    candidatura_id: int,
    novo_status: str,
    observacoes: Optional[str] = None
):
    """Atualizar status de uma candidatura"""
    
    status_validos = ['pendente', 'em_analise', 'entrevista', 'aprovada', 'rejeitada']
    if novo_status not in status_validos:
        raise HTTPException(status_code=400, detail=f"Status inválido. Use: {', '.join(status_validos)}")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar se candidatura existe
    cursor.execute("SELECT id FROM candidaturas_esg WHERE id=?", (candidatura_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    
    # Atualizar status
    cursor.execute("""
        UPDATE candidaturas_esg 
        SET status=?, observacoes=?, data_atualizacao=CURRENT_TIMESTAMP
        WHERE id=?
    """, (novo_status, observacoes, candidatura_id))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Status atualizado para '{novo_status}'",
        "candidatura_id": candidatura_id,
        "novo_status": novo_status
    }


@router.get("/api/estatisticas/{empresa_id}")
async def get_estatisticas(empresa_id: int):
    """Obter estatísticas da empresa"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar CNPJ
    cursor.execute("SELECT cnpj FROM empresas_esg WHERE id=?", (empresa_id,))
    empresa = cursor.fetchone()
    
    if not empresa:
        conn.close()
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    # Estatísticas
    stats = {}
    
    # Total de vagas
    cursor.execute("SELECT COUNT(*) as total FROM vagas WHERE cnpj=?", (empresa['cnpj'],))
    stats['total_vagas'] = cursor.fetchone()['total']
    
    # Candidaturas por status
    cursor.execute("""
        SELECT c.status, COUNT(*) as total
        FROM candidaturas_esg c
        JOIN vagas v ON c.vaga_id = v.id
        WHERE v.cnpj = ?
        GROUP BY c.status
    """, (empresa['cnpj'],))
    
    stats['candidaturas_por_status'] = {row['status']: row['total'] for row in cursor.fetchall()}
    
    # Score médio
    cursor.execute("""
        SELECT AVG(c.compatibilidade_score) as score_medio
        FROM candidaturas_esg c
        JOIN vagas v ON c.vaga_id = v.id
        WHERE v.cnpj = ?
    """, (empresa['cnpj'],))
    
    score_row = cursor.fetchone()
    stats['score_medio'] = round(score_row['score_medio'], 1) if score_row['score_medio'] else 0
    
    # Top 5 candidatos
    cursor.execute("""
        SELECT p.nome_completo, p.email, c.compatibilidade_score, v.titulo as vaga
        FROM candidaturas_esg c
        JOIN vagas v ON c.vaga_id = v.id
        JOIN profissionais_esg p ON c.profissional_id = p.id
        WHERE v.cnpj = ?
        ORDER BY c.compatibilidade_score DESC
        LIMIT 5
    """, (empresa['cnpj'],))
    
    stats['top_candidatos'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return stats
