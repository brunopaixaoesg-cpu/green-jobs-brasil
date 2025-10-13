"""
Green Jobs Brasil - API com SQLite
Versão que funciona diretamente com SQLite sem SQLAlchemy ORM complexo
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import sqlite3
import uvicorn
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import os

app = FastAPI(
    title="Green Jobs Brasil API",
    description="API para consulta de empresas verdes no Brasil",
    version="2.0.0"
)

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="api/templates")
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Importar routers (importação local para evitar problemas de caminho)
import sys
sys.path.insert(0, os.path.dirname(__file__))
from routers import vagas, profissionais, matching

# Registrar routers
app.include_router(vagas.router)
app.include_router(profissionais.router)
app.include_router(matching.router)

import os

# Caminho para o banco - sempre usar o da pasta principal
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gjb_dev.db")
if not os.path.exists(DATABASE_PATH):
    # Fallback para pasta atual
    DATABASE_PATH = "gjb_dev.db"

def get_db_connection():
    """Obter conexão com banco SQLite"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para retornar dicts
        return conn
    except Exception as e:
        print(f"Erro de conexão: {e}")
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")

# === ROTAS WEB ===

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal do dashboard"""
    return templates.TemplateResponse("dashboard_moderno.html", {"request": request})

@app.get("/empresas", response_class=HTMLResponse)
async def empresas_page(request: Request):
    """Página de empresas verdes"""
    return templates.TemplateResponse("empresas_modernas.html", {"request": request})

@app.get("/cnaes", response_class=HTMLResponse)
async def cnaes_page(request: Request):
    """Página de CNAEs verdes"""
    return templates.TemplateResponse("cnaes_modernos.html", {"request": request})

@app.get("/vagas", response_class=HTMLResponse)
async def vagas_page(request: Request):
    """Página de vagas ESG"""
    return templates.TemplateResponse("vagas/lista.html", {"request": request})

@app.get("/vagas/publicar", response_class=HTMLResponse)
async def publicar_vaga_page(request: Request):
    """Página para publicar vaga"""
    return templates.TemplateResponse("vagas/publicar.html", {"request": request})

@app.get("/matching/empresa", response_class=HTMLResponse)
async def dashboard_empresa_page(request: Request):
    """Dashboard de matching para empresas"""
    return templates.TemplateResponse("matching/dashboard_empresa.html", {"request": request})

@app.get("/matching/profissional", response_class=HTMLResponse)
async def dashboard_profissional_page(request: Request):
    """Dashboard de matching para profissionais"""
    return templates.TemplateResponse("matching/dashboard_profissional.html", {"request": request})

@app.get("/vagas/detalhes", response_class=HTMLResponse)
async def detalhes_vaga_page(request: Request):
    """Página de detalhes da vaga"""
    return templates.TemplateResponse("vagas/detalhes.html", {"request": request})

@app.get("/profissionais", response_class=HTMLResponse)
async def profissionais_page(request: Request):
    """Página de lista de profissionais"""
    return templates.TemplateResponse("profissionais/lista.html", {"request": request})

@app.get("/profissionais/cadastro", response_class=HTMLResponse)
async def cadastro_profissional_page(request: Request):
    """Página de cadastro de profissional"""
    return templates.TemplateResponse("profissionais/cadastro.html", {"request": request})

@app.get("/profissionais/perfil", response_class=HTMLResponse)
async def perfil_profissional_page(request: Request):
    """Página de perfil do profissional"""
    return templates.TemplateResponse("profissionais/perfil.html", {"request": request})

# === ROTAS API ===

@app.get("/api/health")
def health():
    """Health check da API"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) as total FROM empresas_verdes")
        total_empresas = cursor.fetchone()["total"]
        conn.close()
        
        return {
            "status": "ok", 
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "total_empresas": total_empresas
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/api/empresas")
def listar_empresas(
    uf: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Listar empresas verdes com filtros"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query base
        query = """
        SELECT cnpj, razao_social, nome_fantasia, cnae_principal, 
               porte, uf, municipio, situacao_cadastral, score_verde as green_score,
               data_abertura, fonte_atualizacao, atualizado_em
        FROM empresas_verdes 
        WHERE 1=1
        """
        params = []
        
        # Adicionar filtros
        if uf:
            query += " AND uf = ?"
            params.append(uf.upper())
        
        if q:
            query += " AND (razao_social LIKE ? OR nome_fantasia LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%"])
        
        # Ordenação e paginação
        query += " ORDER BY score_verde DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        empresas = [dict(row) for row in cursor.fetchall()]
        
        # Contar total
        count_query = "SELECT count(*) as total FROM empresas_verdes WHERE 1=1"
        count_params = []
        
        if uf:
            count_query += " AND uf = ?"
            count_params.append(uf.upper())
        
        if q:
            count_query += " AND (razao_social LIKE ? OR nome_fantasia LIKE ?)"
            count_params.extend([f"%{q}%", f"%{q}%"])
        
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()["total"]
        
        conn.close()
        
        # Retornar apenas a lista de empresas para o dashboard
        return empresas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar empresas: {str(e)}")

@app.get("/api/empresas/{cnpj}")
def obter_empresa(cnpj: str):
    """Obter detalhes de uma empresa específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar empresa
        cursor.execute("""
            SELECT cnpj, razao_social, nome_fantasia, cnae_principal, 
                   porte, uf, municipio, situacao_cadastral, score_verde,
                   data_abertura, fonte_atualizacao, atualizado_em, ods_tags,
                   cnaes_secundarias
            FROM empresas_verdes 
            WHERE cnpj = ?
        """, (cnpj,))
        
        empresa = cursor.fetchone()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        empresa_dict = dict(empresa)
        
        # Buscar CNAEs relacionados
        cursor.execute("""
            SELECT codigo_cnae
            FROM empresa_cnae 
            WHERE cnpj = ?
        """, (cnpj,))
        
        cnaes = [row["codigo_cnae"] for row in cursor.fetchall()]
        empresa_dict["cnaes_relacionados"] = cnaes
        
        conn.close()
        
        return empresa_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar empresa: {str(e)}")

@app.get("/api/cnaes")
def listar_cnaes(categoria: Optional[str] = None, prioridade: Optional[str] = None):
    """Listar CNAEs verdes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT cnae as codigo, titulo as descricao, categoria as classificacao, 
               prioridade, ods_raw as ods, observacoes, created_at
        FROM cnae_green 
        WHERE 1=1
        """
        params = []
        
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        
        if prioridade:
            query += " AND prioridade = ?"
            params.append(prioridade)
        
        query += " ORDER BY prioridade, categoria"
        
        cursor.execute(query, params)
        cnaes = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Retornar apenas a lista de CNAEs para o dashboard  
        return cnaes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar CNAEs: {str(e)}")

@app.get("/api/cnaes/{codigo}")
def obter_cnae(codigo: str):
    """Obter detalhes de um CNAE específico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cnae, titulo, categoria, prioridade, ods_raw, 
                   observacoes, created_at
            FROM cnae_green 
            WHERE cnae = ?
        """, (codigo,))
        
        cnae = cursor.fetchone()
        if not cnae:
            raise HTTPException(status_code=404, detail="CNAE não encontrado")
        
        conn.close()
        
        return dict(cnae)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar CNAE: {str(e)}")

@app.get("/api/stats")
def estatisticas():
    """Estatísticas gerais do sistema"""
    try:
        print("=== Iniciando estatisticas ===")
        conn = get_db_connection()
        cursor = conn.cursor()
        print("Conexão estabelecida")
        
        # Total de empresas
        cursor.execute("SELECT count(*) as total FROM empresas_verdes")
        result1 = cursor.fetchone()
        total_empresas = result1["total"]
        print(f"Total empresas: {total_empresas}")
        
        # Total de CNAEs
        cursor.execute("SELECT count(*) as total FROM cnae_green")
        result2 = cursor.fetchone()
        total_cnaes = result2["total"]
        print(f"Total CNAEs: {total_cnaes}")
        
        # Score médio das empresas
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
        result3 = cursor.fetchone()
        score_medio = result3["media"] or 0
        print(f"Score médio: {score_medio}")
        
        # Total de relações empresa-cnae
        cursor.execute("SELECT count(*) as total FROM empresa_cnae")
        result4 = cursor.fetchone()
        total_relacoes = result4["total"]
        print(f"Total relações: {total_relacoes}")
        
        conn.close()
        print("Conexão fechada")
        
        response = {
            "total_empresas": total_empresas,
            "total_cnaes_verdes": total_cnaes,
            "score_medio": float(score_medio),
            "total_relacoes": total_relacoes,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Response: {response}")
        return response
        
    except Exception as e:
        error_msg = f"Erro ao obter estatísticas: {str(e)}"
        print(f"ERRO em stats: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

# Importar rotas de busca
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from etl.real_data_processor import RealDataProcessor
from fastapi import Form

@app.post("/add-company")
async def add_company(cnpj: str = Form(...)):
    """Adiciona empresa via CNPJ"""
    try:
        processor = RealDataProcessor()
        
        # Busca empresa
        result = processor.search_cnpj_receita_ws(cnpj)
        
        if not result:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        if result['situacao'] != 'ATIVA':
            raise HTTPException(status_code=400, detail=f"Empresa inativa: {result['situacao']}")
        
        # Coleta CNAEs
        all_cnaes = []
        if result['atividade_principal']:
            all_cnaes.append(result['atividade_principal'])
        if result['atividades_secundarias']:
            all_cnaes.extend(result['atividades_secundarias'])
        
        # Calcula score
        score = processor.calculate_green_score(all_cnaes)
        
        if score > 0:
            # Salva empresa verde
            green_cnaes = []
            for cnae in all_cnaes:
                if processor.calculate_green_score([cnae]) > 0:
                    green_cnaes.append(cnae)
            
            result['green_score'] = score
            result['green_cnaes'] = green_cnaes
            processor.save_green_companies([result])
            
            return {
                "success": True,
                "message": f"Empresa verde adicionada com sucesso!",
                "company": {
                    "nome": result['nome'],
                    "cnpj": result['cnpj'],
                    "score": score,
                    "cnaes_verdes": green_cnaes
                }
            }
        else:
            return {
                "success": False,
                "message": "Empresa não é verde (nenhum CNAE verde identificado)",
                "company": {
                    "nome": result['nome'],
                    "cnpj": result['cnpj'],
                    "score": 0,
                    "cnaes": all_cnaes
                }
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search-company/{cnpj}")
async def search_company(cnpj: str):
    """Busca empresa por CNPJ sem adicionar"""
    try:
        processor = RealDataProcessor()
        result = processor.search_cnpj_receita_ws(cnpj)
        
        if not result:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        # Coleta CNAEs
        all_cnaes = []
        if result['atividade_principal']:
            all_cnaes.append(result['atividade_principal'])
        if result['atividades_secundarias']:
            all_cnaes.extend(result['atividades_secundarias'])
        
        # Calcula score
        score = processor.calculate_green_score(all_cnaes)
        
        return {
            "nome": result['nome'],
            "cnpj": result['cnpj'],
            "situacao": result['situacao'],
            "municipio": result.get('municipio'),
            "uf": result.get('uf'),
            "cnaes": all_cnaes,
            "green_score": score,
            "is_green": score > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Iniciando Green Jobs Brasil API...")
    print("API: http://127.0.0.1:8000")
    print("Docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)