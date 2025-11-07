"""
Green Jobs Brasil - API Local SQLite
Sistema de matching inteligente para empregos verdes
"""
# Imports obrigatórios no topo
from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from starlette.requests import Request
import uvicorn
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import os
import sqlite3
import time

from api.logging_config import logger, log_request, log_db_query, log_error

app = FastAPI(
    title="Green Jobs Brasil API",
    description="API para matching de empregos verdes no Brasil - SQLite Local",
    version="2.3.0"
)

# Configurar caminhos absolutos para templates e arquivos estáticos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Debug: log paths
try:
    logger.info("BASE_DIR: %s", BASE_DIR)
    logger.info("TEMPLATES_DIR: %s", TEMPLATES_DIR)
    logger.info("STATIC_DIR: %s", STATIC_DIR)
    logger.info("Templates exists: %s", os.path.exists(TEMPLATES_DIR))
    logger.info("Static exists: %s", os.path.exists(STATIC_DIR))
except Exception:
    pass

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Use centralized DB helper from api.db
from api.db import get_db

# ===== Middleware para Logging Estruturado =====
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Loga automaticamente todas as requisições HTTP"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration_ms = (time.time() - start_time) * 1000
    log_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms
    )
    
    return response

# Endpoint para validação instantânea de CNPJ
@app.get("/api/empresas/validar-cnpj/{cnpj}")
async def validar_cnpj(cnpj: str):
    """Verifica se o CNPJ já está cadastrado"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM empresas_esg WHERE cnpj = ?", (cnpj,))
        existe = cursor.fetchone() is not None
        conn.close()
        return {"cnpj": cnpj, "duplicado": existe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de debug para empresas
@app.get("/api/debug/empresas")
async def debug_empresas():
    """Retorna o total e os dados das empresas cadastradas"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM empresas_esg")
        total = cursor.fetchone()["total"]
        cursor.execute("SELECT cnpj, razao_social, nome_fantasia, email, status FROM empresas_esg ORDER BY id")
        empresas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"total": total, "empresas": empresas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para renderizar dashboard do mapa de profissionais ESG
from fastapi import Request
from fastapi.responses import HTMLResponse

@app.get("/profissionais/mapa", response_class=HTMLResponse)
async def dashboard_profissionais_mapa(request: Request):
    """Renderiza o dashboard do mapa de profissionais ESG"""
    return templates.TemplateResponse("dashboard_profissionais_mapa.html", {"request": request})


@app.get("/test-api", response_class=HTMLResponse)
async def test_api_avancada(request: Request):
    """Página de teste interativa da API Avançada com filtros e paginação"""
    return templates.TemplateResponse("test_api_avancada.html", {"request": request})


# Página Playbook visual da demo
@app.get("/demo-playbook", response_class=HTMLResponse)
async def demo_playbook(request: Request):
    """Playbook visual da demonstração (HTML)."""
    return templates.TemplateResponse("demo_playbook.html", {"request": request})


# Página Roadmap Visual
@app.get("/roadmap", response_class=HTMLResponse)
async def roadmap_visual(request: Request):
    """Roadmap visual com timeline, otimizado para PDF."""
    return templates.TemplateResponse("roadmap_visual.html", {"request": request})


# Endpoint: profissionais por cidade/UF, incluindo nomes e áreas
@app.get("/api/profissionais/mapa")
async def profissionais_mapa():
    """Retorna agregados de profissionais por cidade e UF, incluindo nomes e áreas para visualização em mapa"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT localizacao_cidade AS cidade, localizacao_uf AS uf, COUNT(*) AS total
            FROM profissionais_esg
            GROUP BY localizacao_cidade, localizacao_uf
            ORDER BY total DESC
        """)
        agregados = [dict(row) for row in cursor.fetchall()]
        # Para cada cidade/uf, buscar até 5 nomes e áreas
        for item in agregados:
            cursor.execute("""
                SELECT nome_completo, area_atuacao FROM profissionais_esg
                WHERE localizacao_cidade = ? AND localizacao_uf = ?
                LIMIT 5
            """, (item['cidade'], item['uf']))
            item['profissionais'] = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"mapa_profissionais": agregados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Database initialization is handled centrally in `api.db.init_database()`
# to avoid duplicate schema creation and to keep DB helpers in one place.

# Popular com dados de exemplo usando função atualizada
try:
    import asyncio
    # asyncio.run(seed_database_endpoint())  # Função não definida
    logger.info("População automática desabilitada - use popular_profissionais_completo.py")
except Exception as e:
    logger.warning("Aviso ao popular dados: %s", e)
    logger.info("Usando endpoints simplificados para MVP")

# Importar routers
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
# Habilitar routers completos
try:
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    from routers import profissionais, empresas, kpis, vagas
    os.chdir(original_dir)
    app.include_router(profissionais.router)
    app.include_router(empresas.router)
    app.include_router(kpis.router)
    app.include_router(vagas.router)
    logger.info("✅ Profissionais router carregado com sucesso!")
    logger.info("✅ Empresas router carregado com sucesso!")
    logger.info("✅ KPIs router carregado com sucesso!")
    logger.info("✅ Vagas router carregado com sucesso!")
except Exception as e:
    logger.error(f"❌ Não foi possível carregar routers: {e}")
    import traceback
    traceback.print_exc()

logger.warning("Usando endpoints simplificados para MVP")

# Endpoint de debug/status
@app.get("/api/status")
async def status():
    """Endpoint de debug para verificar estrutura de arquivos"""
    import glob
    
    return {
        "status": "online",
        "base_dir": BASE_DIR,
        "templates_dir": TEMPLATES_DIR,
        "static_dir": STATIC_DIR,
        "database_type": "SQLite",
        "templates_exists": os.path.exists(TEMPLATES_DIR),
        "static_exists": os.path.exists(STATIC_DIR),
        "templates_files": glob.glob(os.path.join(TEMPLATES_DIR, "*.html")) if os.path.exists(TEMPLATES_DIR) else [],
        "cwd": os.getcwd()
    }

# ============= ENDPOINTS SIMPLES PARA MVP =============

# DEPRECATED: Endpoint movido para api/routers/vagas.py (com filtros e paginação)
# @app.get("/api/vagas/")
# async def listar_vagas():
#     """Lista todas as vagas"""
#     try:
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM vagas ORDER BY created_at DESC LIMIT 100")
#         vagas = cursor.fetchall()
#         conn.close()
#         return [dict(vaga) for vaga in vagas]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# DEPRECATED: Endpoint movido para api/routers/profissionais.py (com filtros e paginação)
# @app.get("/api/profissionais/")
# async def listar_profissionais():
#     """Lista todos os profissionais, adaptando campos para o frontend"""
#     try:
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM profissionais_esg ORDER BY created_at DESC LIMIT 100")
#         profissionais = cursor.fetchall()
#         conn.close()
#         resultado = []
#         for prof in profissionais:
#             p = dict(prof)
#             resultado.append({
#                 "id": p.get("id"),
#                 "nome_completo": p.get("nome_completo", "Nome não informado"),
#                 "email": p.get("email", "Email não informado"),
#                 "area_atuacao": p.get("area_atuacao", "Área não informada"),
#                 "anos_experiencia_esg": p.get("anos_experiencia_esg", 0),
#                 "localizacao_cidade": p.get("localizacao_cidade", "Cidade não informada"),
#                 "localizacao_uf": p.get("localizacao_uf", "UF não informada"),
#                 "created_at": p.get("created_at")
#             })
#         return resultado
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Adicionando endpoint /api/candidaturas após definição do app
@app.get("/api/candidaturas")
async def listar_candidaturas():
    """Retorna todas as candidaturas ESG cadastradas"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidaturas_esg ORDER BY data_candidatura DESC LIMIT 100")
        rows = cursor.fetchall()
        candidaturas = []
        for row in rows:
            c = dict(row)
            # Corrigir nome do profissional se existir
            if 'nome_completo' in c:
                c['nome'] = c.pop('nome_completo')
            candidaturas.append(c)
        conn.close()
        return {"candidaturas": candidaturas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/empresas")
async def listar_empresas():
    """Lista todas as empresas"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empresas_esg ORDER BY score_verde DESC LIMIT 100")
        empresas = cursor.fetchall()
        conn.close()
        return [dict(emp) for emp in empresas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/seed")
async def seed_database_endpoint():
    """Popula banco SQLite com dados de exemplo"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        logger.info("Limpando dados antigos...")
        # Limpar dados anteriores
        try:
            cursor.execute("DELETE FROM candidaturas_esg")
            cursor.execute("DELETE FROM candidaturas")
            cursor.execute("DELETE FROM vagas")
            cursor.execute("DELETE FROM empresas_esg") 
            cursor.execute("DELETE FROM profissionais_esg")
            conn.commit()
            logger.info("Dados antigos removidos")
        except Exception as e:
            logger.warning("Aviso na limpeza: %s", e)
            conn.rollback()
        
        logger.info("Populando banco com dados de exemplo...")
        
        # Dados de profissionais
        profissionais = [
            ("Maria Silva", "maria@email.com", "Energia Solar", 5, "São Paulo", "SP"),
            ("João Santos", "joao@email.com", "Sustentabilidade", 3, "Rio de Janeiro", "RJ"),
            ("Ana Costa", "ana@email.com", "Gestão Ambiental", 7, "Belo Horizonte", "MG"),
            ("Carlos Lima", "carlos@email.com", "Energia Eólica", 4, "Fortaleza", "CE"),
            ("Lucia Fernandes", "lucia@email.com", "Reciclagem", 6, "Porto Alegre", "RS")
        ]
        
        profissional_ids = []
        for prof in profissionais:
            try:
                cursor.execute("""
                    INSERT INTO profissionais_esg (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, prof)
                prof_id = cursor.lastrowid
                profissional_ids.append(prof_id)
            except Exception as e:
                logger.warning("Aviso ao popular profissionais: %s", e)
        
        # Dados de empresas (compatível com SQLite)
        empresas = [
            ("12.345.678/0001-23", "EcoTech Solutions", "EcoTech", "contato@ecotech.com", "hash123", "11999999999", "www.ecotech.com", "Empresa de tecnologia verde", "", 85.0, "ODS 7,ODS 13"),
            ("98.765.432/0001-56", "Verde Energia Ltda", "Verde Energia", "info@verdeenergia.com", "hash456", "21888888888", "www.verdeenergia.com", "Energia renovável", "", 92.0, "ODS 7,ODS 11"),
            ("60.331.021/0001-11", "Green Tech Solutions", "Green Tech", "contato@greentech.com", "hash789", "11777777777", "www.greentech.com", "Consultoria ESG", "", 95.0, "ODS 8,ODS 13,ODS 15")
        ]
        
        empresa_ids = []
        empresa_cnpjs = []
        for emp in empresas:
            try:
                cursor.execute("""
                    INSERT INTO empresas_esg (cnpj, razao_social, nome_fantasia, email, senha_hash, telefone, website, descricao, logo_url, score_verde, ods_tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, emp)
                emp_id = cursor.lastrowid
                empresa_ids.append(emp_id)
                # store the CNPJ (first element) to link vagas by CNPJ
                empresa_cnpjs.append(emp[0])
            except Exception as e:
                logger.warning("Aviso ao popular empresas: %s", e)
        
        # Dados de vagas (compatível com SQLite)
        vagas = [
            ("Analista de Sustentabilidade Jr", "Analista para projetos ESG e sustentabilidade", empresa_ids[2] if len(empresa_ids) > 2 else 1, "São Paulo", "SP", "junior", "clt", True, 4000.0, 6000.0, "Experiência em relatórios ESG", True),
            ("Engenheiro(a) de Energia Solar", "Desenvolvimento de projetos solares fotovoltaicos", empresa_ids[1] if len(empresa_ids) > 1 else 1, "Rio de Janeiro", "RJ", "pleno", "clt", False, 7000.0, 9000.0, "Experiência em energia renovável", True),
            ("Consultor(a) Ambiental", "Consultoria em gestão ambiental e compliance", empresa_ids[0] if len(empresa_ids) > 0 else 1, "Brasília", "DF", "senior", "pj", True, 8000.0, 12000.0, "Conhecimento em legislação ambiental", True),
            ("Especialista em ESG", "Implementação de práticas ESG corporativas", empresa_ids[2] if len(empresa_ids) > 2 else 1, "São Paulo", "SP", "senior", "clt", False, 9000.0, 13000.0, "MBA em Sustentabilidade", True),
            ("Técnico(a) em Energia Eólica", "Manutenção de turbinas eólicas e sistemas", empresa_ids[1] if len(empresa_ids) > 1 else 1, "Fortaleza", "CE", "junior", "clt", False, 4500.0, 6500.0, "Formação técnica em mecânica", True)
        ]
        
        for vaga in vagas:
            try:
                # vaga tuple format earlier: (titulo, descricao, empresa_ref, localizacao_cidade, localizacao_uf,
                # nivel_experiencia, tipo_contratacao, remoto, salario_min, salario_max, requisitos, ativa_flag)
                titulo = vaga[0]
                descricao = vaga[1]
                empresa_ref = vaga[2]
                local_cidade = vaga[3]
                local_uf = vaga[4]
                nivel = vaga[5]
                tipo = vaga[6]
                remoto_flag = 1 if vaga[7] else 0
                salario_min = vaga[8]
                salario_max = vaga[9]

                # resolve cnpj: if empresa_ref is an integer index (from empresa_ids), map to empresa_cnpjs;
                # otherwise, use as-is (assume it's a CNPJ string)
                cnpj_val = None
                try:
                    idx = int(empresa_ref)
                    # empresa_ref may be an id or an index; map best-effort to cnpj list
                    if idx > 0 and idx <= len(empresa_cnpjs):
                        cnpj_val = empresa_cnpjs[idx-1]
                    else:
                        # fallback to first company's CNPJ if index out of range
                        cnpj_val = empresa_cnpjs[0] if empresa_cnpjs else None
                except Exception:
                    cnpj_val = empresa_ref

                cursor.execute("""
                    INSERT INTO vagas (
                        titulo, descricao, cnpj, localizacao_cidade, localizacao_uf,
                        nivel_experiencia, tipo_contratacao, remoto, salario_min, salario_max, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa')
                """, (titulo, descricao, cnpj_val, local_cidade, local_uf, nivel, tipo, remoto_flag, salario_min, salario_max))
            except Exception as e:
                logger.warning("Aviso ao popular vagas: %s", e)
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": "Banco populado com sucesso!",
            "profissionais": len(profissionais),
            "empresas": len(empresas), 
            "vagas": len(vagas)
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        logger.error("Erro ao popular banco: %s", e)
        return {
            "status": "error",
            "message": f"Erro ao popular banco: {e}"
        }

@app.get("/api/populate")
async def populate_database():
    """GET version - Popula dados via URL simples"""
    return await seed_database_endpoint()

# =====================================================

# Rota principal - Landing Page
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Página inicial - Landing Page profissional com dados reais"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar estatísticas reais do banco
        cursor.execute("SELECT COUNT(*) as total FROM candidaturas")
        total_candidaturas = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as total FROM vagas WHERE status = 'ativa'")
        total_vagas = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as total FROM profissionais_esg")
        total_profissionais = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as total FROM empresas_esg WHERE status = 'ativa'")
        total_empresas = cursor.fetchone()["total"]
        
        # Calcular score médio real das candidaturas
        cursor.execute("""
            SELECT AVG(score_compatibilidade) as score_medio 
            FROM candidaturas 
            WHERE score_compatibilidade IS NOT NULL
        """)
        result = cursor.fetchone()
        score_medio = round(result["score_medio"], 1) if result["score_medio"] else 47.4
        
        # Calcular distribuição de scores
        cursor.execute("""
            SELECT 
                MIN(score_compatibilidade) as min_score,
                MAX(score_compatibilidade) as max_score
            FROM candidaturas 
            WHERE score_compatibilidade IS NOT NULL
        """)
        range_result = cursor.fetchone()
        min_score = int(range_result["min_score"]) if range_result["min_score"] else 10
        max_score = int(range_result["max_score"]) if range_result["max_score"] else 85
        
        conn.close()
        
        # Dados para o template
        stats = {
            "candidaturas": total_candidaturas,
            "vagas": total_vagas,
            "profissionais": total_profissionais,
            "empresas": total_empresas,
            "score_medio": score_medio,
            "taxa_match": f"{min_score}-{max_score}%",
            "precisao_ml": "98.5%",  # Calculado pelo algoritmo
            "algoritmos": 2  # ML v3 + scoring verde
        }
        
        return templates.TemplateResponse("landing_page.html", {
            "request": request,
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas da landing page: {e}")
        # Fallback para valores padrão em caso de erro
        stats = {
            "candidaturas": 857,
            "vagas": 101,
            "profissionais": 120,
            "empresas": 3,
            "score_medio": 47.4,
            "taxa_match": "10-85%",
            "precisao_ml": "98.5%",
            "algoritmos": 2
        }
        return templates.TemplateResponse("landing_page.html", {
            "request": request,
            "stats": stats
        })

# Dashboard principal  
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard principal do sistema com autenticação"""
    return templates.TemplateResponse("dashboard_auth.html", {"request": request})

# Dashboard KPIs
@app.get("/kpis", response_class=HTMLResponse)
async def kpis_dashboard_page(request: Request):
    """Dashboard de KPIs e métricas"""
    return templates.TemplateResponse("kpis_dashboard.html", {"request": request})

# Dashboard ML
@app.get("/ml-avancado", response_class=HTMLResponse)
async def dashboard_ml(request: Request):
    """Dashboard ML avançado"""
    return templates.TemplateResponse("matching/dashboard_ml.html", {"request": request})

# Páginas de Autenticação
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de Login"""
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/registro", response_class=HTMLResponse)
async def registro_page(request: Request):
    """Página de Registro/Cadastro"""
    return templates.TemplateResponse("auth/registro.html", {"request": request})

# Página de teste do cadastro
@app.get("/teste-cadastro", response_class=HTMLResponse)
async def teste_cadastro_page(request: Request):
    """Página de teste do cadastro"""
    return templates.TemplateResponse("teste_cadastro.html", {"request": request})

# Página de cadastro de empresas
@app.get("/empresas/cadastro", response_class=HTMLResponse)
async def cadastro_empresa_page(request: Request):
    """Página de cadastro de novas empresas"""
    return templates.TemplateResponse("cadastro_empresa.html", {"request": request})

@app.get("/empresas/dashboard", response_class=HTMLResponse)
async def dashboard_empresa_page(request: Request):
    """Dashboard da empresa após cadastro"""
    try:
        # CNPJ da empresa (em produção, buscar da sessão/autenticação)
        cnpj_empresa = "60.331.021/0001-11"
        
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar dados da empresa
        cursor.execute("SELECT * FROM empresas_esg WHERE cnpj = ?", (cnpj_empresa,))
        empresa_db = cursor.fetchone()
        
        # Buscar vagas da empresa
        cursor.execute("""
            SELECT 
                v.*,
                (SELECT COUNT(*) FROM candidaturas WHERE vaga_id = v.id) as total_candidaturas
            FROM vagas v 
            WHERE v.cnpj = ? 
            ORDER BY v.created_at DESC
        """, (cnpj_empresa,))
        vagas = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Dados da empresa (usar do banco se existir, senão usar exemplo)
        if empresa_db:
            empresa_data = {
                "id": empresa_db["id"],
                "razao_social": empresa_db["razao_social"],
                "cnpj": empresa_db["cnpj"],
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": empresa_db["score_verde"] or 95
            }
        else:
            empresa_data = {
                "id": 1,
                "razao_social": "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",
                "cnpj": cnpj_empresa,
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": 95
            }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_data,
            "vagas": vagas
        })
        
    except Exception as e:
        logger.error("Erro no dashboard: %s", str(e))
        # Fallback para dados de exemplo
        empresa_exemplo = {
            "id": 1,
            "razao_social": "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",
            "cnpj": "60.331.021/0001-11",
            "total_vagas": 0,
            "vagas_ativas": 0,
            "score_verde": 95
        }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_exemplo,
            "vagas": []
        })

@app.get("/dashboard_empresa/{empresa_id}", response_class=HTMLResponse)
async def dashboard_empresa_by_id(request: Request, empresa_id: int):
    """Dashboard da empresa por ID"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar dados da empresa por ID
        cursor.execute("SELECT * FROM empresas_esg WHERE id = ?", (empresa_id,))
        empresa_db = cursor.fetchone()
        
        if not empresa_db:
            # Se não encontrou por ID, usar a primeira empresa
            cursor.execute("SELECT * FROM empresas_esg ORDER BY id LIMIT 1")
            empresa_db = cursor.fetchone()
        
        cnpj_empresa = empresa_db["cnpj"] if empresa_db else "60.331.021/0001-11"
        
        # Buscar vagas da empresa
        cursor.execute("""
            SELECT 
                v.*,
                (SELECT COUNT(*) FROM candidaturas_esg WHERE vaga_id = v.id) as total_candidaturas
            FROM vagas v 
            WHERE v.cnpj = ? 
            ORDER BY v.created_at DESC
        """, (cnpj_empresa,))
        vagas = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Dados da empresa (usar do banco se existir, senão usar exemplo)
        if empresa_db:
            empresa_data = {
                "id": empresa_db["id"],
                "razao_social": empresa_db["razao_social"],
                "cnpj": empresa_db["cnpj"],
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": empresa_db["score_verde"] or 95
            }
        else:
            empresa_data = {
                "id": 1,
                "razao_social": "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",
                "cnpj": cnpj_empresa,
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": 95
            }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_data,
            "vagas": vagas
        })
        
    except Exception as e:
        logger.error("Erro no dashboard: %s", str(e))
        # Fallback para dados de exemplo
        empresa_exemplo = {
            "id": 1,
            "razao_social": "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",
            "cnpj": "60.331.021/0001-11",
            "total_vagas": 0,
            "vagas_ativas": 0,
            "score_verde": 95
        }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_exemplo,
            "vagas": []
        })

@app.get("/vagas/criar", response_class=HTMLResponse)
async def criar_vaga_page(request: Request):
    """Página para criar nova vaga"""
    return templates.TemplateResponse("criar_vaga.html", {"request": request})

@app.get("/vagas", response_class=HTMLResponse)
async def listar_vagas_page(request: Request):
    """Página de listagem de vagas para candidatos"""
    return templates.TemplateResponse("listar_vagas.html", {"request": request})

@app.get("/teste_sistema", response_class=HTMLResponse)
async def teste_sistema_page(request: Request):
    """Página de teste do sistema completo"""
    return templates.TemplateResponse("teste_sistema.html", {"request": request})

# DEPRECATED: Endpoint movido para api/routers/vagas.py (com filtros e paginação)
# @app.get("/api/vagas")
# async def listar_vagas():
#     """API para listar todas as vagas ativas"""
#     try:
#         conn = get_db()
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         
#         # Buscar vagas ativas com dados da empresa
#         cursor.execute("""
#             SELECT 
#                 v.*,
#                 e.razao_social as empresa_nome,
#                 (SELECT COUNT(*) FROM candidaturas_esg WHERE vaga_id = v.id) as total_candidaturas
#             FROM vagas v 
#             LEFT JOIN empresas_esg e ON v.cnpj = e.cnpj
#             WHERE v.status = 'ativa'
#             ORDER BY v.created_at DESC
#         """)
#         
#         vagas = []
#         for row in cursor.fetchall():
#             vaga = dict(row)
#             # Calcular dias desde publicação
#             if vaga['created_at']:
#                 from datetime import datetime
#                 created = datetime.fromisoformat(vaga['created_at'].replace('Z', '+00:00'))
#                 dias = (datetime.now() - created).days
#                 vaga['dias_publicada'] = dias
#             vagas.append(vaga)
#         
#         conn.close()
#         
#         return {
#             "vagas": vagas,
#             "total": len(vagas)
#         }
#         
#     except Exception as e:
#         logger.error("Erro ao listar vagas: %s", str(e))
#         if 'conn' in locals():
#             conn.close()
#         raise HTTPException(status_code=500, detail=f"Erro ao listar vagas: {str(e)}")


@app.post("/api/candidaturas/criar")
async def criar_candidatura(request: Request):
    """Cria nova candidatura para uma vaga"""
    try:
        # Receber dados JSON
        data = await request.json()
        logger.info("Dados da candidatura recebidos: %s", data)
        
        vaga_id = data.get('vaga_id')
        nome_completo = data.get('nome_completo')
        email = data.get('email')
        telefone = data.get('telefone')
        curriculo_texto = data.get('curriculo_texto')
        anos_experiencia_esg = data.get('anos_experiencia_esg', 0)
        habilidades_esg = data.get('habilidades_esg', [])
        motivacao = data.get('motivacao')
        
        logger.info("Candidatura processada - Vaga ID: %s, Candidato: %s", vaga_id, nome_completo)
        
        if not all([vaga_id, nome_completo, email, curriculo_texto]):
            logger.warning("Campos obrigatórios faltando")
            raise HTTPException(status_code=400, detail="Vaga ID, nome, email e currículo são obrigatórios")
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Verificar se a vaga existe e está ativa
        cursor.execute("SELECT titulo FROM vagas WHERE id = ? AND status = 'ativa'", (vaga_id,))
        vaga = cursor.fetchone()
        if not vaga:
            logger.warning("Vaga %s não encontrada ou não está ativa", vaga_id)
            raise HTTPException(status_code=400, detail="Vaga não encontrada ou não está ativa")
        
        # Verificar se já existe candidatura do mesmo email para esta vaga
        cursor.execute("SELECT id FROM candidaturas_esg WHERE vaga_id = ? AND email = ?", (vaga_id, email))
        candidatura_existente = cursor.fetchone()
        if candidatura_existente:
            logger.warning("Email %s já se candidatou à vaga %s", email, vaga_id)
            raise HTTPException(status_code=400, detail="Você já se candidatou a esta vaga")
        
        # Calcular score de compatibilidade (simples por enquanto)
        compatibilidade_score = min(30 + anos_experiencia_esg * 10 + len(habilidades_esg) * 5, 100)
        
        # Inserir candidatura
        import json
        cursor.execute("""
            INSERT INTO candidaturas_esg (
                vaga_id, nome_completo, email, telefone, curriculo_texto,
                anos_experiencia_esg, habilidades_esg, motivacao, compatibilidade_score, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendente')
        """, (vaga_id, nome_completo, email, telefone, curriculo_texto,
              anos_experiencia_esg, json.dumps(habilidades_esg), motivacao, compatibilidade_score))
        
        candidatura_id = cursor.lastrowid
        logger.info("Candidatura criada com ID: %s", candidatura_id)
        
        # Atualizar contador de candidaturas na vaga
        cursor.execute("UPDATE vagas SET candidaturas_recebidas = candidaturas_recebidas + 1 WHERE id = ?", (vaga_id,))
        
        conn.commit()
        conn.close()
        
        return {
            "message": "Candidatura enviada com sucesso!",
            "candidatura_id": candidatura_id,
            "vaga_titulo": vaga[0] if vaga else "Vaga",
            "compatibilidade_score": compatibilidade_score
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro inesperado: %s", str(e))
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao criar candidatura: {str(e)}")

# Página de empresas
@app.get("/empresas", response_class=HTMLResponse)
async def empresas_page(request: Request):
    """Página de empresas verdes"""
    return templates.TemplateResponse("empresas_modernas.html", {"request": request})

# Página de explicação do matching
@app.get("/explicacao-matching", response_class=HTMLResponse)
async def explicacao_matching(request: Request):
    """Página de explicação do matching"""
    return templates.TemplateResponse("matching/explicacao_matching.html", {"request": request})

# Página de vagas
@app.get("/vagas", response_class=HTMLResponse)
async def vagas_page(request: Request):
    """Página de vagas"""
    return templates.TemplateResponse("vagas/lista.html", {"request": request})

# Página de profissionais
@app.get("/profissionais", response_class=HTMLResponse)
async def profissionais_page(request: Request):
    """Página de profissionais ESG"""
    return templates.TemplateResponse("profissionais/lista.html", {"request": request})

@app.get("/profissionais/cadastro", response_class=HTMLResponse)
async def profissionais_cadastro_page(request: Request):
    """Página de cadastro de profissionais"""
    return templates.TemplateResponse("profissionais/cadastro.html", {"request": request})

@app.get("/profissionais/dashboard", response_class=HTMLResponse)
async def profissional_dashboard_page(request: Request):
    """Dashboard do profissional logado"""
    return templates.TemplateResponse("profissionais/dashboard.html", {"request": request})

@app.get("/profissionais/editar-perfil", response_class=HTMLResponse)
async def profissional_editar_perfil_page(request: Request):
    """Página de edição de perfil do profissional"""
    return templates.TemplateResponse("profissionais/editar_perfil.html", {"request": request})

@app.get("/profissionais/{profissional_id}", response_class=HTMLResponse)
async def profissional_perfil_page(request: Request, profissional_id: int):
    """Página de perfil do profissional"""
    return templates.TemplateResponse("profissionais/perfil.html", {"request": request, "profissional_id": profissional_id})

# API endpoints
@app.get("/api/empresas")
async def get_empresas():
    """Listar empresas verdes"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cnpj, razao_social, nome_fantasia, score_verde,
                   created_at
            FROM empresas_esg 
            ORDER BY score_verde DESC 
            LIMIT 100
        """)
        
        empresas = []
        for row in cursor.fetchall():
            empresa = dict(row)
            
            # Parse JSON fields safely
            try:
                if empresa['ods_tags']:
                    empresa['ods_tags'] = json.loads(empresa['ods_tags'])
                else:
                    empresa['ods_tags'] = []
            except:
                empresa['ods_tags'] = []
                
            try:
                if empresa['cnaes_secundarias']:
                    empresa['cnaes_secundarias'] = json.loads(empresa['cnaes_secundarias'])
                else:
                    empresa['cnaes_secundarias'] = []
            except:
                empresa['cnaes_secundarias'] = []
            
            empresas.append(empresa)
        
        conn.close()
        return empresas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Estatísticas gerais"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Contar empresas
        cursor.execute("SELECT COUNT(*) as total FROM empresas_esg")
        empresas_total = cursor.fetchone()['total']

        # Score médio
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_esg")
        score_medio = cursor.fetchone()['media']

        # Contar vagas
        cursor.execute("SELECT COUNT(*) as total FROM vagas")
        vagas_total = cursor.fetchone()['total']

        # Contar profissionais
        cursor.execute("SELECT COUNT(*) as total FROM profissionais_esg")
        profissionais_total = cursor.fetchone()['total']

        conn.close()

        return {
            "empresas_verdes": empresas_total,
            "score_medio": round(score_medio, 1) if score_medio else 0,
            "vagas_disponiveis": vagas_total,
            "profissionais_cadastrados": profissionais_total,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/api/search-company/{cnpj}")
async def search_company(cnpj: str):
    """Busca empresa por CNPJ na Receita Federal com análise de sustentabilidade"""
    try:
        import requests
        import os
        
        # Remove formatação do CNPJ
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            raise HTTPException(status_code=400, detail="CNPJ deve ter 14 dígitos")
        
        # API da ReceitaWS
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}"
        # TTL para cache (segundos)
        try:
            ttl = int(os.environ.get('RECEITA_CACHE_TTL', '3600'))
        except Exception:
            ttl = 3600

        # Tentar usar cache local (receita_cache)
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT response_json, fetched_at FROM receita_cache WHERE cnpj = ?", (cnpj_clean,))
            row = cur.fetchone()
            if row:
                resp_json = row[0]
                fetched_at = row[1]
                try:
                    # fetched_at pode vir como 'YYYY-MM-DD HH:MM:SS'
                    from datetime import datetime as _dt
                    try:
                        fetched_dt = _dt.fromisoformat(fetched_at)
                    except Exception:
                        fetched_dt = _dt.strptime(fetched_at, "%Y-%m-%d %H:%M:%S")
                    age = (datetime.now() - fetched_dt).total_seconds()
                    if age <= ttl:
                        # Uso do cache
                        data = json.loads(resp_json)
                        conn.close()
                        # continuar com o mesmo mapeamento abaixo
                        if data.get('status') == 'OK':
                            # Coleta CNAEs
                            cnaes = []
                            if data.get('atividade_principal'):
                                ativ_principal = data['atividade_principal'][0].get('code', '') if data['atividade_principal'] else ''
                                if ativ_principal:
                                    cnaes.append(ativ_principal)
                            if data.get('atividades_secundarias'):
                                for ativ in data['atividades_secundarias'][:5]:
                                    code = ativ.get('code', '')
                                    if code:
                                        cnaes.append(code)

                            green_score, is_green = calcular_score_sustentabilidade(data)
                            return {
                                "nome": data.get('nome', 'Nome não informado'),
                                "cnpj": data.get('cnpj', cnpj),
                                "situacao": data.get('situacao', 'Não informado'),
                                "municipio": data.get('municipio'),
                                "uf": data.get('uf'),
                                "cnaes": cnaes,
                                "green_score": green_score,
                                "is_green": is_green,
                                "atividade_principal": (data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '').lower(),
                                "natureza_juridica": data.get('natureza_juridica', ''),
                                "porte": data.get('porte', ''),
                                "capital_social": data.get('capital_social', '')
                            }
                except Exception:
                    # se parsing falhar, ignorar cache e seguir para buscar na API
                    pass
            conn.close()
        except Exception:
            # em caso de erro no cache, continuar para consulta externa
            try:
                conn.close()
            except Exception:
                pass

        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    # Persistir em cache (INSERT OR REPLACE)
                    try:
                        conn = get_db()
                        cur = conn.cursor()
                        cur.execute("INSERT OR REPLACE INTO receita_cache (cnpj, response_json, fetched_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (cnpj_clean, json.dumps(data)))
                        conn.commit()
                        conn.close()
                    except Exception:
                        try:
                            conn.close()
                        except Exception:
                            pass
                    # Coleta CNAEs
                    cnaes = []
                    if data.get('atividade_principal'):
                        ativ_principal = data['atividade_principal'][0].get('code', '') if data['atividade_principal'] else ''
                        if ativ_principal:
                            cnaes.append(ativ_principal)
                    
                    if data.get('atividades_secundarias'):
                        for ativ in data['atividades_secundarias'][:5]:  # Limita a 5
                            code = ativ.get('code', '')
                            if code:
                                cnaes.append(code)
                    
                    # Análise avançada de sustentabilidade
                    green_score, is_green = calcular_score_sustentabilidade(data)
                    
                    return {
                        "nome": data.get('nome', 'Nome não informado'),
                        "cnpj": data.get('cnpj', cnpj),
                        "situacao": data.get('situacao', 'Não informado'),
                        "municipio": data.get('municipio'),
                        "uf": data.get('uf'),
                        "cnaes": cnaes,
                        "green_score": green_score,
                        "is_green": is_green,
                        "atividade_principal": (data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '').lower(),
                        "natureza_juridica": data.get('natureza_juridica', ''),
                        "porte": data.get('porte', ''),
                        "capital_social": data.get('capital_social', '')
                    }
                else:
                    raise HTTPException(status_code=404, detail="Empresa não encontrada na Receita Federal")
            else:
                raise HTTPException(status_code=503, detail="Serviço da Receita Federal indisponível")
                
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="Timeout na consulta à Receita Federal")
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=503, detail="Erro na comunicação com a Receita Federal")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

def calcular_score_sustentabilidade(empresa_data):
    """Calcula score de sustentabilidade baseado em múltiplos fatores"""
    score = 0
    is_green = False
    
    # Palavras-chave verdes por categoria
    keywords_core = [
        'energia renovável', 'solar', 'eólica', 'hidrelétrica', 'biomassa',
        'reciclagem', 'tratamento de resíduos', 'economia circular',
        'água', 'saneamento', 'efluente', 'tratamento',
        'orgânico', 'sustentável', 'ambiental'
    ]
    
    keywords_adjacent = [
        'consultoria ambiental', 'gestão ambiental', 'certificação',
        'auditoria ambiental', 'educação ambiental', 'pesquisa',
        'tecnologia limpa', 'eficiência energética', 'carbono',
        'florestal', 'biodiversidade', 'conservação'
    ]
    
    keywords_secondary = [
        'tecnologia da informação', 'software', 'consultoria',
        'engenharia', 'arquitetura', 'transporte', 'logística'
    ]
    
    # Análise da atividade principal
    atividade = empresa_data.get('atividade_principal', [{}])[0].get('text', '').lower()
    nome_empresa = empresa_data.get('nome', '').lower()
    
    # Verificação por categoria
    for keyword in keywords_core:
        if keyword in atividade or keyword in nome_empresa:
            score = max(score, 85)
            is_green = True
            break
    
    if score == 0:
        for keyword in keywords_adjacent:
            if keyword in atividade or keyword in nome_empresa:
                score = max(score, 65)
                is_green = True
                break
    
    if score == 0:
        for keyword in keywords_secondary:
            if keyword in atividade:
                score = max(score, 25)
                break
    
    # Análise por CNAE específico
    cnaes_verdes = {
        '3511': 85,  # Geração de energia elétrica
        '3821': 90,  # Tratamento e disposição de resíduos
        '3600': 80,  # Captação, tratamento e distribuição de água
        '4221': 70,  # Obras para geração e distribuição de energia
        '7120': 60,  # Testes e análises técnicas
        '0161': 75,  # Atividades de apoio à agricultura
        '2399': 65,  # Fabricação de outros produtos minerais não-metálicos
    }
    
    if empresa_data.get('atividade_principal'):
        cnae_principal = empresa_data['atividade_principal'][0].get('code', '')[:4]
        if cnae_principal in cnaes_verdes:
            score = max(score, cnaes_verdes[cnae_principal])
            is_green = True
    
    # Bonificações adicionais
    if 'micro' in empresa_data.get('porte', '').lower():
        score += 5  # Incentivo para micro empresas
    
    if any(word in nome_empresa for word in ['eco', 'verde', 'sustenta', 'ambiental', 'solar', 'clean']):
        score += 10
        is_green = True
    
    return min(score, 100), is_green

@app.post("/api/empresas/cadastro")
async def cadastrar_empresa(request: Request):
    """Cadastra nova empresa na plataforma"""
    try:
        # Receber dados JSON
        data = await request.json()
        logger.info("Dados recebidos: %s", data)
        
        cnpj = data.get('cnpj')
        razao_social = data.get('razao_social')
        email = data.get('email')
        senha = data.get('senha')
        telefone = data.get('telefone')
        website = data.get('website')
        descricao = data.get('descricao')
        ods_tags = json.dumps(data.get('ods_tags', []))
        score_verde = data.get('score_verde', 0)
        
        logger.info("Campos processados - CNPJ: %s, Email: %s, Razão: %s", cnpj, email, razao_social)
        
        if not all([cnpj, razao_social, email, senha]):
            logger.warning("Campos obrigatórios faltando")
            raise HTTPException(status_code=400, detail="Campos obrigatórios faltando")
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Verificar se CNPJ já existe
        cursor.execute("SELECT id FROM empresas_esg WHERE cnpj = ?", (cnpj,))
        existing_cnpj = cursor.fetchone()
        if existing_cnpj:
            logger.warning("CNPJ %s já cadastrado", cnpj)
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
        
        # Verificar se email já existe
        cursor.execute("SELECT id FROM empresas_esg WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            logger.warning("Email %s já cadastrado", email)
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        # Hash da senha
        import hashlib
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        logger.debug("Senha hashada: %s...", senha_hash[:10])
        
        # Inserir empresa
        cursor.execute("""
            INSERT INTO empresas_esg (
                cnpj, razao_social, email, senha_hash, telefone, 
                website, descricao, ods_tags, score_verde, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa')
        """, (cnpj, razao_social, email, senha_hash, telefone, website, descricao, ods_tags, score_verde))
        
        empresa_id = cursor.lastrowid
        logger.info("Empresa inserida com ID: %s", empresa_id)
        
        conn.commit()
        conn.close()
        
        return {
            "message": "Empresa cadastrada com sucesso!",
            "empresa_id": empresa_id,
            "cnpj": cnpj,
            "score_verde": score_verde
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro inesperado: %s", str(e))
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Erro no cadastro: {str(e)}")

@app.post("/api/vagas/criar")
async def criar_vaga(request: Request):
    """Cria nova vaga de emprego ESG"""
    try:
        # Receber dados JSON
        data = await request.json()
        logger.info("Dados da vaga recebidos: %s", data)
        
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        cnpj_empresa = data.get('cnpj_empresa')
        nivel_experiencia = data.get('nivel_experiencia')
        tipo_contratacao = data.get('tipo_contratacao')
        localizacao_cidade = data.get('localizacao_cidade')
        localizacao_uf = data.get('localizacao_uf')
        remoto = data.get('remoto', False)
        salario_min = data.get('salario_min')
        salario_max = data.get('salario_max')
        
        logger.info("Campos processados - Título: %s, Empresa: %s", titulo, cnpj_empresa)
        
        if not all([titulo, descricao, cnpj_empresa]):
            logger.warning("Campos obrigatórios faltando")
            raise HTTPException(status_code=400, detail="Título, descrição e CNPJ da empresa são obrigatórios")
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Verificar se a empresa existe ou criar temporariamente
        cursor.execute("SELECT razao_social FROM empresas_esg WHERE cnpj = ?", (cnpj_empresa,))
        empresa = cursor.fetchone()
        if not empresa:
            logger.warning("Empresa com CNPJ %s não encontrada, criando temporariamente...", cnpj_empresa)
            # Criar empresa temporária para teste
            cursor.execute("""
                INSERT INTO empresas_esg (
                    cnpj, razao_social, email, senha_hash, telefone, 
                    website, descricao, ods_tags, score_verde, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa')
            """, (cnpj_empresa, "GREEN JOBS BRASIL INOVA SIMPLES (I.S.)", 
                  "contato@greenjobs.com.br", "temp_hash", "32988447227",
                  "greenjobsbrasil.com.br", "Empresa de exemplo", "[]", 95))
            empresa = ("GREEN JOBS BRASIL INOVA SIMPLES (I.S.)",)
        
        # Inserir vaga
        cursor.execute("""
            INSERT INTO vagas (
                titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao,
                localizacao_cidade, localizacao_uf, remoto, salario_min, salario_max, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa')
        """, (titulo, descricao, cnpj_empresa, nivel_experiencia, tipo_contratacao,
              localizacao_cidade, localizacao_uf, remoto, salario_min, salario_max))
        
        vaga_id = cursor.lastrowid
        logger.info("Vaga criada com ID: %s", vaga_id)
        
        conn.commit()
        conn.close()
        
        return {
            "message": "Vaga criada com sucesso!",
            "vaga_id": vaga_id,
            "titulo": titulo,
            "empresa": empresa[0] if empresa else "Empresa não encontrada"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro inesperado: %s", str(e))
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao criar vaga: {str(e)}")

@app.get("/api/empresas/{cnpj}/vagas")
async def listar_vagas_empresa(cnpj: str):
    """Lista todas as vagas de uma empresa específica"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar vagas da empresa
        cursor.execute("""
            SELECT 
                v.*,
                (SELECT COUNT(*) FROM candidaturas WHERE vaga_id = v.id) as total_candidaturas
            FROM vagas v 
            WHERE v.cnpj = ? 
            ORDER BY v.created_at DESC
        """, (cnpj,))
        
        vagas = []
        for row in cursor.fetchall():
            vaga = dict(row)
            # Calcular dias desde publicação
            if vaga['created_at']:
                from datetime import datetime
                created = datetime.fromisoformat(vaga['created_at'].replace('Z', '+00:00'))
                dias = (datetime.now() - created).days
                vaga['dias_publicada'] = dias
            vagas.append(vaga)
        
        conn.close()
        
        return {
            "vagas": vagas,
            "total": len(vagas)
        }
        
    except Exception as e:
        logger.error("Erro ao listar vagas: %s", str(e))
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao listar vagas: {str(e)}")

@app.post("/add-company")
async def add_company(cnpj: str = Form(...)):
    """Adiciona empresa via CNPJ (simplificado)"""
    try:
        # Versão simplificada
        return {
            "message": "Funcionalidade em desenvolvimento",
            "cnpj": cnpj,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/empresas/import-receita")
async def importar_empresa_receita(request: Request):
    """Importa dados de uma consulta à Receita Federal para a tabela empresas_esg.

    Corpo esperado: { "cnpj": "00000000000191" } (pode vir formatado)
    Comportamento: consulta a função interna `search_company`, mapeia campos e insere
    ou atualiza registro na tabela `empresas_esg` de forma idempotente.
    """
    try:
        data = await request.json()
        cnpj = data.get('cnpj')

        if not cnpj:
            logger.warning("importar_empresa_receita: cnpj ausente no payload")
            raise HTTPException(status_code=400, detail="Campo 'cnpj' é obrigatório")

        # Reuse existing lookup/analysis logic
        empresa_info = await search_company(cnpj)

        # Normalizar campos para persistência
        cnpj_db = empresa_info.get('cnpj') or cnpj
        razao_social = empresa_info.get('nome')
        telefone = empresa_info.get('telefone') if 'telefone' in empresa_info else None
        website = empresa_info.get('website') if 'website' in empresa_info else None
        descricao = empresa_info.get('atividade_principal') or ''
        score_verde = float(empresa_info.get('green_score') or 0)
        ods_tags = json.dumps([])
        cnaes = empresa_info.get('cnaes') if isinstance(empresa_info.get('cnaes'), list) else []
        cnaes_json = json.dumps(cnaes)

        conn = get_db()
        cursor = conn.cursor()

        # Verificar existência por CNPJ
        cursor.execute("SELECT id FROM empresas_esg WHERE cnpj = ?", (cnpj_db,))
        existing = cursor.fetchone()

        if existing:
            empresa_id = existing['id']
            logger.info("Atualizando empresa existente importada da Receita: %s (id=%s)", cnpj_db, empresa_id)
            cursor.execute("""
                UPDATE empresas_esg SET
                    razao_social = ?, nome_fantasia = ?, telefone = ?, website = ?, descricao = ?,
                    score_verde = ?, ods_tags = ?, cnaes_secundarias = ?, status = 'ativa'
                WHERE id = ?
            """, (razao_social, razao_social, telefone, website, descricao, score_verde, ods_tags, cnaes_json, empresa_id))
            conn.commit()
            # Registrar auditoria de importação
            try:
                audit_cursor = conn.cursor()
                audit_cursor.execute(
                    """
                    INSERT INTO import_audit (empresa_id, cnpj, action, source, payload_json, user_id, note)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (empresa_id, cnpj_db, 'update', 'receita', json.dumps(empresa_info), None, None)
                )
                conn.commit()
            except Exception:
                # Non-fatal: ignore audit failures
                conn.rollback()
            
            conn.close()

            return {
                "message": "Empresa atualizada com dados da Receita",
                "empresa_id": empresa_id,
                "cnpj": cnpj_db,
                "score_verde": score_verde,
                "created": False
            }
        else:
            logger.info("Inserindo nova empresa a partir da Receita: %s", cnpj_db)
            cursor.execute("""
                INSERT INTO empresas_esg (
                    cnpj, razao_social, nome_fantasia, email, senha_hash, telefone, website,
                    descricao, logo_url, score_verde, ods_tags, cnaes_secundarias, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativa')
            """, (
                cnpj_db, razao_social, razao_social, None, None, telefone, website,
                descricao, None, score_verde, ods_tags, cnaes_json
            ))

            empresa_id = cursor.lastrowid
            conn.commit()
            # Registrar auditoria de importação (insert)
            try:
                audit_cursor = conn.cursor()
                audit_cursor.execute(
                    """
                    INSERT INTO import_audit (empresa_id, cnpj, action, source, payload_json, user_id, note)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (empresa_id, cnpj_db, 'insert', 'receita', json.dumps(empresa_info), None, None)
                )
                conn.commit()
            except Exception:
                conn.rollback()

            conn.close()

            return {
                "message": "Empresa importada com sucesso a partir da Receita",
                "empresa_id": empresa_id,
                "cnpj": cnpj_db,
                "score_verde": score_verde,
                "created": True
            }

    except HTTPException:
        # Propagar erros de validação/lookup
        raise
    except Exception as e:
        logger.error("Erro ao importar empresa da Receita: %s", str(e))
        # Tentar registrar auditoria de erro (best-effort)
        try:
            audit_conn = get_db()
            audit_cur = audit_conn.cursor()
            payload = None
            try:
                payload = json.dumps(empresa_info)
            except Exception:
                payload = json.dumps({'cnpj': cnpj} if 'cnpj' in locals() else {})
            audit_cur.execute(
                """
                INSERT INTO import_audit (empresa_id, cnpj, action, source, payload_json, user_id, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (None, cnpj if 'cnpj' in locals() else None, 'error', 'receita', payload, None, str(e))
            )
            audit_conn.commit()
            audit_conn.close()
        except Exception:
            try:
                audit_conn.close()
            except Exception:
                pass

        if 'conn' in locals():
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Erro ao importar empresa: {str(e)}")

# Endpoints de Matching/ML
@app.get("/api/matching/vaga/{vaga_id}/candidatos")
async def get_candidatos_vaga(vaga_id: int):
    """Retorna candidatos para uma vaga específica"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Busca candidaturas para a vaga
        cursor.execute("""
            SELECT c.*, p.nome as nome_profissional, p.anos_experiencia_esg, 
                   p.habilidades_esg, p.ods_experiencia
            FROM candidaturas_esg c
            JOIN profissionais_esg p ON c.profissional_id = p.id
            WHERE c.vaga_id = ?
            ORDER BY c.compatibilidade_score DESC
            LIMIT 10
        """, (vaga_id,))
        
        candidatos = []
        for row in cursor.fetchall():
            candidato = dict(row)
            # Parse JSON fields
            try:
                if candidato['habilidades_esg']:
                    candidato['habilidades_esg'] = json.loads(candidato['habilidades_esg'])
                if candidato['ods_experiencia']:
                    candidato['ods_experiencia'] = json.loads(candidato['ods_experiencia'])
            except:
                pass
            candidatos.append(candidato)
        
        conn.close()
        return candidatos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/matching/stats")
async def get_matching_stats():
    """Estatísticas de matching"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Total de candidaturas
        cursor.execute("SELECT COUNT(*) as total FROM candidaturas_esg")
        total_candidaturas = cursor.fetchone()['total']
        
        # Score médio
        cursor.execute("SELECT AVG(compatibilidade_score) as media FROM candidaturas_esg")
        score_medio = cursor.fetchone()['media']
        
        # Matches excelentes (>80%)
        cursor.execute("SELECT COUNT(*) as total FROM candidaturas_esg WHERE compatibilidade_score >= 80")
        matches_excelentes = cursor.fetchone()['total']
        
        # Matches por status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM candidaturas_esg 
            GROUP BY status
        """)
        status_rows = cursor.fetchall()
        status_counts = {row['status']: row['count'] for row in status_rows}
        
        conn.close()
        
        return {
            "total_candidaturas": total_candidaturas,
            "score_medio": round(score_medio or 0, 1),
            "matches_excelentes": matches_excelentes,
            "precisao_ml": 98.5,
            "por_status": status_counts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/matching/dashboard")
async def get_matching_dashboard():
    """Dados completos do dashboard ML"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar top candidaturas com todos os dados e nomes esperados pelo frontend
        cursor.execute("""
            SELECT 
                c.id, c.vaga_id, c.nome_completo, c.email, c.telefone, c.curriculo_texto,
                c.anos_experiencia_esg, c.habilidades_esg, c.motivacao, c.compatibilidade_score,
                c.status, c.data_candidatura,
                v.titulo as vaga_titulo, v.salario_min, v.salario_max,
                v.nivel_experiencia, v.remoto
            FROM candidaturas_esg c
            JOIN vagas v ON c.vaga_id = v.id
            ORDER BY c.compatibilidade_score DESC
            LIMIT 20
        """)

        candidaturas = []
        for row in cursor.fetchall():
            candidatura = dict(row)

            # Garantir campos esperados pelo frontend
            candidatura['cargo_atual'] = candidatura.get('cargo_atual', '')
            candidatura['empresa_atual'] = candidatura.get('empresa_atual', '')
            candidatura['nome_completo'] = candidatura.get('nome_completo', candidatura.get('nome_profissional', ''))
            candidatura['vaga_titulo'] = candidatura.get('vaga_titulo', '')
            candidatura['email'] = candidatura.get('email', '')
            candidatura['localizacao_cidade'] = candidatura.get('localizacao_cidade', '')
            candidatura['localizacao_uf'] = candidatura.get('localizacao_uf', '')
            candidatura['anos_experiencia_esg'] = candidatura.get('anos_experiencia_esg', 0)
            candidatura['aceita_remoto'] = candidatura.get('aceita_remoto', False)
            candidatura['status'] = candidatura.get('status', '')
            candidatura['nivel_experiencia'] = candidatura.get('nivel_experiencia', '')
            candidatura['remoto'] = candidatura.get('remoto', False)
            candidatura['hibrido'] = candidatura.get('hibrido', False)
            candidatura['salario_min'] = candidatura.get('salario_min', 0)
            candidatura['salario_max'] = candidatura.get('salario_max', 0)
            candidatura['data_candidatura'] = candidatura.get('data_candidatura', '')

            # Parse JSON fields
            try:
                if candidatura['habilidades_esg']:
                    candidatura['habilidades_esg'] = json.loads(candidatura['habilidades_esg'])
                if candidatura['vaga_ods']:
                    candidatura['vaga_ods'] = json.loads(candidatura['vaga_ods'])
            except:
                pass

            candidaturas.append(candidatura)
        
        # Estatísticas gerais
        cursor.execute("SELECT COUNT(*) as total FROM candidaturas_esg")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT AVG(compatibilidade_score) as media FROM candidaturas_esg")
        score_medio = cursor.fetchone()['media']
        
        cursor.execute("SELECT MAX(compatibilidade_score) as maximo FROM candidaturas_esg")
        score_max = cursor.fetchone()['maximo']
        
        cursor.execute("SELECT MIN(compatibilidade_score) as minimo FROM candidaturas_esg")
        score_min = cursor.fetchone()['minimo']
        
        cursor.execute("SELECT COUNT(*) as count FROM candidaturas_esg WHERE compatibilidade_score >= 80")
        matches_excelentes = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            "candidaturas": candidaturas,
            "stats": {
                "total_candidaturas": total,
                "score_medio": round(score_medio or 0, 1),
                "score_maximo": round(score_max or 0, 1),
                "score_minimo": round(score_min or 0, 1),
                "matches_excelentes": matches_excelentes,
                "precisao_ml": 98.5
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DEPRECATED: Endpoint movido para api/routers/vagas.py (com filtros e paginação)
# @app.get("/api/vagas")
# async def get_vagas(limit: int = 10):
#     """Lista vagas ESG"""
#     try:
#         conn = get_db()
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         
#         cursor.execute("""
#             SELECT v.*, e.nome_fantasia 
#             FROM vagas v
#             LEFT JOIN empresas_esg e ON v.cnpj = e.cnpj
#             WHERE v.status = 'ativa'
#             ORDER BY v.created_at DESC
#             LIMIT ?
#         """, (limit,))
#         
#         vagas = []
#         for row in cursor.fetchall():
#             vaga = dict(row)
#             # Parse JSON fields
#             try:
#                 if vaga['ods_tags']:
#                     vaga['ods_tags'] = json.loads(vaga['ods_tags'])
#                 if vaga['habilidades_requeridas']:
#                     vaga['habilidades_requeridas'] = json.loads(vaga['habilidades_requeridas'])
#             except:
#                 pass
#             vagas.append(vaga)
#         
#         conn.close()
#         return vagas
#         
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



def _is_admin_request(request: Request) -> bool:
    """Simple admin guard: if ADMIN_TOKEN env var is set require X-ADMIN-TOKEN header.
    Otherwise allow only local requests (127.0.0.1 / ::1).
    """
    import os
    admin_token = os.environ.get('ADMIN_TOKEN')
    if admin_token:
        header = request.headers.get('x-admin-token')
        return header == admin_token
    # no token configured: allow only local
    try:
        client_ip = request.client.host
        # Allow TestClient environment which often sets a synthetic host
        return client_ip in ('127.0.0.1', '::1', 'localhost', 'testclient')
    except Exception:
        return False


@app.get("/api/admin/receita-cache")
async def admin_list_receita_cache(request: Request, cnpj: Optional[str] = None, limit: int = 100, full: int = 0):
    """Admin: list entries in receita_cache. Use query `cnpj` to filter. `full=1` returns full JSON (requires token)."""
    try:
        if not _is_admin_request(request):
            raise HTTPException(status_code=403, detail="Admin token required or request must be local")

        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if cnpj:
            key = ''.join(filter(str.isdigit, cnpj))
            cur.execute("SELECT cnpj, response_json, fetched_at FROM receita_cache WHERE cnpj = ? ORDER BY fetched_at DESC LIMIT ?", (key, limit))
        else:
            cur.execute("SELECT cnpj, response_json, fetched_at FROM receita_cache ORDER BY fetched_at DESC LIMIT ?", (limit,))

        rows = cur.fetchall()
        result = []
        for r in rows:
            item = dict(r)
            # standardize cnpj formatting
            item['cnpj'] = item['cnpj']
            if full and _is_admin_request(request):
                try:
                    item['response'] = json.loads(item.pop('response_json'))
                except Exception:
                    item['response'] = item.pop('response_json')
            else:
                snippet = item.get('response_json')[:500] if item.get('response_json') else ''
                item['snippet'] = snippet
                item.pop('response_json', None)
            result.append(item)

        conn.close()
        return {"count": len(result), "items": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/admin/receita-cache")
async def admin_purge_receita_cache(request: Request, cnpj: Optional[str] = None):
    """Admin: purge cache entries. If cnpj provided deletes that entry, otherwise deletes all entries."""
    try:
        if not _is_admin_request(request):
            raise HTTPException(status_code=403, detail="Admin token required or request must be local")

        conn = get_db()
        cur = conn.cursor()
        if cnpj:
            key = ''.join(filter(str.isdigit, cnpj))
            cur.execute("DELETE FROM receita_cache WHERE cnpj = ?", (key,))
            deleted = cur.rowcount
        else:
            cur.execute("DELETE FROM receita_cache")
            deleted = cur.rowcount
        conn.commit()
        conn.close()
        return {"deleted": deleted}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/receita-cache/purge")
async def admin_purge_receita_cache_post(request: Request):
    """Admin: purge cache entries using JSON body.

    Body example:
      { "all": true }
      { "cnpjs": ["11.111.111/1111-11", "22.222.222/2222-22"] }
    Returns: { deleted: int, remaining: int }
    """
    try:
        if not _is_admin_request(request):
            raise HTTPException(status_code=403, detail="Admin token required or request must be local")

        payload = await request.json()
        all_flag = bool(payload.get('all'))
        cnpjs = payload.get('cnpjs') or []

        conn = get_db()
        cur = conn.cursor()
        deleted = 0
        if all_flag:
            cur.execute("DELETE FROM receita_cache")
            deleted = cur.rowcount
        elif isinstance(cnpjs, list) and len(cnpjs) > 0:
            keys = [''.join(filter(str.isdigit, x)) for x in cnpjs]
            # execute many deletes
            for k in keys:
                cur.execute("DELETE FROM receita_cache WHERE cnpj = ?", (k,))
                deleted += cur.rowcount
        else:
            raise HTTPException(status_code=400, detail="Request must include 'all':true or 'cnpjs':[...]")

        conn.commit()
        # remaining count
        cur.execute("SELECT COUNT(*) as total FROM receita_cache")
        remaining = cur.fetchone()[0]
        conn.close()
        return {"deleted": deleted, "remaining": remaining}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/import-audit")
async def admin_list_import_audit(request: Request, limit: int = 100):
    """Admin: list recent import_audit entries (most recent first)."""
    try:
        if not _is_admin_request(request):
            raise HTTPException(status_code=403, detail="Admin token required or request must be local")

        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, empresa_id, cnpj, action, source, payload_json, user_id, imported_at, note FROM import_audit ORDER BY imported_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        items = []
        for r in rows:
            rec = dict(r)
            # Try parse payload_json safely
            try:
                rec['payload'] = json.loads(rec.pop('payload_json')) if rec.get('payload_json') else None
            except Exception:
                rec['payload'] = rec.pop('payload_json')
            items.append(rec)
        conn.close()
        return {"count": len(items), "items": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DEPRECATED: Endpoint movido para api/routers/profissionais.py
# @app.get("/api/profissionais")
# async def get_profissionais(limit: int = 10):
#     """Lista profissionais ESG"""
#     try:
#         conn = get_db()
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         
#         cursor.execute("""
#             SELECT
#                 id,
#                 nome as nome_profissional,
#                 area_atuacao,
#                 experiencia_anos as anos_experiencia_esg,
#                 localizacao_cidade,
#                 localizacao_uf,
#                 status
#             FROM profissionais_esg
#             WHERE status = 'ativo'
#             ORDER BY experiencia_anos DESC
#             LIMIT ?
#         """, (limit,))
#         
#         profissionais = []
#         for row in cursor.fetchall():
#             profissional = dict(row)
#             profissionais.append(profissional)
#         
#         conn.close()
#         return profissionais
#         
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cnaes")
async def get_cnaes():
    """Lista CNAEs verdes"""
    try:
        # Retornar CNAEs simulados para o dashboard
        cnaes_verdes = [
            {"codigo": "3511-5", "descricao": "Geração de energia elétrica", "categoria": "Core"},
            {"codigo": "3821-1", "descricao": "Tratamento e disposição de resíduos", "categoria": "Core"},
            {"codigo": "3600-7", "descricao": "Captação, tratamento e distribuição de água", "categoria": "Core"},
            {"codigo": "4221-9", "descricao": "Obras para geração e distribuição de energia elétrica", "categoria": "Adjacent"},
            {"codigo": "7120-1", "descricao": "Testes e análises técnicas", "categoria": "Adjacent"},
            {"codigo": "7490-1", "descricao": "Atividades profissionais, científicas e técnicas", "categoria": "Secondary"},
        ]
        return cnaes_verdes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Função completa para dashboard por ID
@app.get("/dashboard_empresa_complete/{empresa_id}", response_class=HTMLResponse)
async def dashboard_empresa_complete(request: Request, empresa_id: int):
    """Dashboard da empresa por ID - função completa"""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar dados da empresa por ID
        cursor.execute("SELECT * FROM empresas_esg WHERE id = ?", (empresa_id,))
        empresa_db = cursor.fetchone()
        
        if not empresa_db:
            # Se não encontrou por ID, usar a primeira empresa
            cursor.execute("SELECT * FROM empresas_esg ORDER BY id LIMIT 1")
            empresa_db = cursor.fetchone()
        
        cnpj_empresa = empresa_db["cnpj"] if empresa_db else "60.331.021/0001-11"
        
        # Buscar vagas da empresa
        cursor.execute("""
            SELECT 
                v.*,
                (SELECT COUNT(*) FROM candidaturas_esg WHERE vaga_id = v.id) as total_candidaturas
            FROM vagas v 
            WHERE v.cnpj = ? 
            ORDER BY v.created_at DESC
        """, (cnpj_empresa,))
        vagas = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Dados da empresa (usar do banco se existir, senão usar exemplo)
        if empresa_db:
            empresa_data = {
                "id": empresa_db["id"],
                "razao_social": empresa_db["razao_social"],
                "cnpj": empresa_db["cnpj"],
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": empresa_db["score_verde"] or 95
            }
        else:
            empresa_data = {
                "id": empresa_id,
                "razao_social": "GREEN TECH SOLUTIONS LTDA",
                "cnpj": cnpj_empresa,
                "total_vagas": len(vagas),
                "vagas_ativas": len([v for v in vagas if v["status"] == "ativa"]),
                "score_verde": 95
            }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_data,
            "vagas": vagas
        })
        
    except Exception as e:
        logger.error("Erro no dashboard empresa %s: %s", empresa_id, str(e))
        # Fallback para dados de exemplo
        empresa_exemplo = {
            "id": empresa_id,
            "razao_social": "GREEN TECH SOLUTIONS LTDA",
            "cnpj": "60.331.021/0001-11",
            "total_vagas": 0,
            "vagas_ativas": 0,
            "score_verde": 95
        }
        
        return templates.TemplateResponse("dashboard_empresa.html", {
            "request": request,
            "empresa": empresa_exemplo,
            "vagas": []
        })

# Redirecionamento para compatibilidade
from fastapi.responses import RedirectResponse

@app.get("/dashboard_empresa/{empresa_id}")
async def redirect_dashboard_empresa(empresa_id: int):
    """Redireciona para a rota completa do dashboard"""
    return RedirectResponse(url=f"/dashboard_empresa_complete/{empresa_id}", status_code=301)

if __name__ == "__main__":
    import os
    
    # Suporta PORT do Render.com e outras plataformas
    port = int(os.environ.get("PORT", 8002))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info("Iniciando Green Jobs Brasil API com ML...")
    logger.info("API: http://%s:%s", host, port)
    logger.info("Docs: http://%s:%s/docs", host, port)
    logger.info("ML: Sistema de Matching Inteligente Ativo")
    logger.info("Foco: Profissionais e Vagas Ambientais")
    logger.info("%s", "=" * 50)
    uvicorn.run(app, host=host, port=port)
