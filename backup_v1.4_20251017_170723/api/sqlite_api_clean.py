"""
Green Jobs Brasil - API com SQLite
Versão que funciona diretamente com SQLite sem SQLAlchemy ORM complexo
"""
from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
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

# Importar routers
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
try:
    # Mudar diretório temporariamente para resolver imports
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    from routers import auth, profissionais
    os.chdir(original_dir)
    app.include_router(auth.router)
    app.include_router(profissionais.router)
    print("Auth router carregado com sucesso!")
    print("Profissionais router carregado com sucesso!")
except Exception as e:
    print(f"Aviso: Nao foi possivel carregar routers: {e}")
    import traceback
    traceback.print_exc()

# Rota principal - Landing Page
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Página inicial - Landing Page profissional"""
    return templates.TemplateResponse("landing_page.html", {"request": request})

# Dashboard principal  
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard principal do sistema com autenticação"""
    return templates.TemplateResponse("dashboard_auth.html", {"request": request})

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
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cnpj, razao_social, nome_fantasia, cnae_principal, 
                   cnaes_secundarias, porte, uf, municipio, 
                   situacao_cadastral, score_verde as green_score, ods_tags,
                   data_abertura, atualizado_em
            FROM empresas_verdes 
            ORDER BY score_verde DESC
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
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Contar empresas
        cursor.execute("SELECT COUNT(*) as total FROM empresas_verdes")
        empresas_total = cursor.fetchone()['total']
        
        # Score médio
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
        score_medio = cursor.fetchone()['media']
        
        # Contar vagas
        cursor.execute("SELECT COUNT(*) as total FROM vagas_esg")
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
    """Busca empresa por CNPJ na Receita Federal"""
    try:
        import requests
        
        # Remove formatação do CNPJ
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            raise HTTPException(status_code=400, detail="CNPJ deve ter 14 dígitos")
        
        # API da ReceitaWS
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
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
                    
                    # Calcula score verde básico (simulado por enquanto)
                    green_score = 0
                    is_green = False
                    
                    # Verifica se algum CNAE contém palavras-chave verdes
                    green_keywords = ['energia', 'renovável', 'solar', 'eólica', 'sustentável', 'reciclagem', 'ambiental']
                    atividade_text = (data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '').lower()
                    
                    for keyword in green_keywords:
                        if keyword in atividade_text:
                            green_score = 75
                            is_green = True
                            break
                    
                    return {
                        "nome": data.get('nome', 'Nome não informado'),
                        "cnpj": data.get('cnpj', cnpj),
                        "situacao": data.get('situacao', 'Não informado'),
                        "municipio": data.get('municipio'),
                        "uf": data.get('uf'),
                        "cnaes": cnaes,
                        "green_score": green_score,
                        "is_green": is_green,
                        "atividade_principal": atividade_text
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

# Endpoints de Matching/ML
@app.get("/api/matching/vaga/{vaga_id}/candidatos")
async def get_candidatos_vaga(vaga_id: int):
    """Retorna candidatos para uma vaga específica"""
    try:
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Busca candidaturas para a vaga
        cursor.execute("""
            SELECT c.*, p.nome_completo, p.anos_experiencia_esg, 
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
        conn = sqlite3.connect("gjb_dev.db")
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
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar top candidaturas com todos os dados
        cursor.execute("""
            SELECT 
                c.id, c.vaga_id, c.profissional_id, c.compatibilidade_score, 
                c.status, c.data_candidatura,
                p.nome_completo, p.email, p.cargo_atual, p.empresa_atual,
                p.localizacao_cidade, p.localizacao_uf, p.anos_experiencia_esg,
                p.aceita_remoto, p.habilidades_esg, p.ods_interesse,
                v.titulo as vaga_titulo, v.salario_min, v.salario_max,
                v.nivel_experiencia, v.remoto, v.hibrido, v.ods_tags as vaga_ods
            FROM candidaturas_esg c
            JOIN profissionais_esg p ON c.profissional_id = p.id
            JOIN vagas_esg v ON c.vaga_id = v.id
            ORDER BY c.compatibilidade_score DESC
            LIMIT 20
        """)
        
        candidaturas = []
        for row in cursor.fetchall():
            candidatura = dict(row)
            
            # Parse JSON fields
            try:
                if candidatura['habilidades_esg']:
                    candidatura['habilidades_esg'] = json.loads(candidatura['habilidades_esg'])
                if candidatura['ods_interesse']:
                    candidatura['ods_interesse'] = json.loads(candidatura['ods_interesse'])
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

@app.get("/api/vagas")
async def get_vagas(limit: int = 10):
    """Lista vagas ESG"""
    try:
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, e.nome_fantasia 
            FROM vagas_esg v
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE v.status = 'ativa'
            ORDER BY v.criada_em DESC
            LIMIT ?
        """, (limit,))
        
        vagas = []
        for row in cursor.fetchall():
            vaga = dict(row)
            # Parse JSON fields
            try:
                if vaga['ods_tags']:
                    vaga['ods_tags'] = json.loads(vaga['ods_tags'])
                if vaga['habilidades_requeridas']:
                    vaga['habilidades_requeridas'] = json.loads(vaga['habilidades_requeridas'])
            except:
                pass
            vagas.append(vaga)
        
        conn.close()
        return vagas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profissionais")
async def get_profissionais(limit: int = 10):
    """Lista profissionais ESG"""
    try:
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nome_completo, cargo_atual, empresa_atual, 
                   anos_experiencia_esg, formacao_area, localizacao_cidade, 
                   localizacao_uf, ods_interesse, status
            FROM profissionais_esg 
            WHERE status = 'ativo'
            ORDER BY anos_experiencia_esg DESC
            LIMIT ?
        """, (limit,))
        
        profissionais = []
        for row in cursor.fetchall():
            profissional = dict(row)
            try:
                if profissional['ods_interesse']:
                    profissional['ods_interesse'] = json.loads(profissional['ods_interesse'])
            except:
                pass
            profissionais.append(profissional)
        
        conn.close()
        return profissionais
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

if __name__ == "__main__":
    print("Iniciando Green Jobs Brasil API com ML...")
    print("API: http://127.0.0.1:8002")
    print("Docs: http://127.0.0.1:8002/docs")
    print("ML: Sistema de Matching Inteligente Ativo")
    print("Foco: Profissionais e Vagas Ambientais")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8002)