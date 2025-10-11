"""
Green Jobs Brasil - Versão Definitiva e Robusta
Sistema final que funciona sempre, baseado em testes anteriores bem-sucedidos
"""
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import uvicorn
from datetime import datetime
import os
import sys
import requests
import time
from pathlib import Path

# Configuração robusta de caminhos
BASE_DIR = Path(__file__).parent.parent  # Pasta raiz do projeto
API_DIR = Path(__file__).parent          # Pasta api
DATABASE_PATH = BASE_DIR / "gjb_dev.db"
TEMPLATES_DIR = API_DIR / "templates"

# Verificações de segurança
if not DATABASE_PATH.exists():
    raise FileNotFoundError(f"Banco de dados não encontrado: {DATABASE_PATH}")

if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Green Jobs Brasil - Sistema Definitivo",
    description="Sistema robusto para identificação de empresas verdes",
    version="3.0.0"
)

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory=str(API_DIR / "static")), name="static")

# Templates com caminho absoluto
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def get_db_connection():
    """Conexão segura com banco de dados"""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"ERRO de conexão com banco: {e}")
        raise HTTPException(status_code=500, detail="Erro de conexão com banco")

class GreenJobsProcessor:
    """Classe robusta para processamento de empresas verdes"""
    
    def __init__(self):
        self.green_cnaes = self._load_green_cnaes()
        print(f"✅ {len(self.green_cnaes)} CNAEs verdes carregados")
    
    def _load_green_cnaes(self):
        """Carrega CNAEs verdes com tratamento de erro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT cnae, titulo, prioridade FROM cnae_green")
            rows = cursor.fetchall()
            conn.close()
            
            green_cnaes = {}
            for row in rows:
                green_cnaes[row['cnae']] = {
                    'descricao': row['titulo'],
                    'classificacao': row['prioridade']
                }
            return green_cnaes
        except Exception as e:
            print(f"ERRO ao carregar CNAEs: {e}")
            return {}
    
    def _normalize_cnae(self, cnae):
        """Normalização robusta de CNAE"""
        if not cnae or cnae == '00.00-0-00':
            return ''
        
        # Remove caracteres não numéricos
        digits_only = ''.join(filter(str.isdigit, str(cnae)))
        
        # Padronização
        if len(digits_only) >= 7:
            return digits_only[:7]
        elif len(digits_only) >= 4:
            return digits_only[:4].ljust(7, '0')
        
        return digits_only
    
    def calculate_green_score(self, cnaes):
        """Cálculo robusto de score verde"""
        if not cnaes or not self.green_cnaes:
            return 0
        
        total_score = 0
        green_count = 0
        
        for cnae in cnaes:
            cnae_norm = self._normalize_cnae(cnae)
            
            for green_cnae, info in self.green_cnaes.items():
                green_norm = self._normalize_cnae(green_cnae)
                
                if cnae_norm == green_norm and cnae_norm:
                    green_count += 1
                    
                    if info['classificacao'] == 'Core':
                        total_score += 100
                    elif info['classificacao'] == 'Adjacent':
                        total_score += 70
                    else:  # Secondary
                        total_score += 40
                    break
        
        if green_count == 0:
            return 0
        
        # Score final com bonus
        base_score = total_score / green_count
        green_ratio = green_count / len(cnaes)
        bonus = green_ratio * 20
        
        return min(100, int(base_score + bonus))
    
    def search_company_receita(self, cnpj):
        """Busca robusta na Receita Federal"""
        try:
            cnpj_clean = ''.join(filter(str.isdigit, cnpj))
            if len(cnpj_clean) != 14:
                return None
                
            url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    # Coleta CNAEs
                    cnaes = []
                    if data.get('atividade_principal'):
                        code = data['atividade_principal'][0].get('code')
                        if code:
                            cnaes.append(code)
                    
                    if data.get('atividades_secundarias'):
                        for ativ in data['atividades_secundarias']:
                            code = ativ.get('code')
                            if code:
                                cnaes.append(code)
                    
                    return {
                        'cnpj': data.get('cnpj'),
                        'nome': data.get('nome'),
                        'fantasia': data.get('fantasia'),
                        'situacao': data.get('situacao'),
                        'cnaes': cnaes,
                        'municipio': data.get('municipio'),
                        'uf': data.get('uf')
                    }
            
            return None
            
        except Exception as e:
            print(f"ERRO na busca CNPJ {cnpj}: {e}")
            return None
    
    def save_green_company(self, company_data):
        """Salva empresa com tratamento robusto"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert/Update empresa
            cursor.execute("""
                INSERT OR REPLACE INTO empresas_verdes 
                (cnpj, razao_social, nome_fantasia, score_verde, situacao_cadastral, municipio, uf, cnae_principal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company_data['cnpj'],
                company_data['nome'],
                company_data.get('fantasia'),
                company_data['green_score'],
                company_data['situacao'],
                company_data.get('municipio'),
                company_data.get('uf'),
                company_data['cnaes'][0] if company_data['cnaes'] else None
            ))
            
            # Salva relacionamentos CNAEs verdes
            green_cnaes = company_data.get('green_cnaes', [])
            for cnae in green_cnaes:
                cursor.execute("""
                    INSERT OR REPLACE INTO empresa_cnae (cnpj, codigo_cnae)
                    VALUES (?, ?)
                """, (company_data['cnpj'], cnae))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"ERRO ao salvar: {e}")
            return False

# Instância global do processador
processor = GreenJobsProcessor()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal - versão moderna"""
    try:
        # Verifica se template moderno existe
        template_path = TEMPLATES_DIR / "dashboard_moderno.html"
        if template_path.exists():
            return templates.TemplateResponse("dashboard_moderno.html", {"request": request})
        
        # Fallback para template básico se não encontrar o moderno
        template_path = TEMPLATES_DIR / "dashboard.html"
        if template_path.exists():
            return templates.TemplateResponse("dashboard.html", {"request": request})
            # Retorna HTML básico se template não existir
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Green Jobs Brasil</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0fdf4; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .header { text-align: center; color: #059669; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #059669; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .success { background: #d1fae5; color: #065f46; }
        .error { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🌱 Green Jobs Brasil - Sistema Definitivo</h1>
        <p>Digite o CNPJ de qualquer empresa brasileira para verificar se é verde:</p>
        
        <div class="form-group">
            <input type="text" id="cnpj" placeholder="00.000.000/0000-00" maxlength="18">
        </div>
        <button onclick="verificarEmpresa()">Verificar Empresa</button>
        
        <div id="resultado"></div>
        
        <hr style="margin: 40px 0;">
        <h3>API Endpoints Disponíveis:</h3>
        <ul>
            <li><a href="/api/stats">Estatísticas</a></li>
            <li><a href="/api/empresas">Lista de Empresas</a></li>
            <li><a href="/api/cnaes">CNAEs Verdes</a></li>
            <li><a href="/docs">Documentação da API</a></li>
        </ul>
    </div>
    
    <script>
        function verificarEmpresa() {
            const cnpj = document.getElementById('cnpj').value.replace(/\\D/g, '');
            const resultado = document.getElementById('resultado');
            
            if (cnpj.length !== 14) {
                resultado.innerHTML = '<div class="result error">CNPJ deve ter 14 dígitos</div>';
                return;
            }
            
            resultado.innerHTML = '<div class="result">🔍 Buscando empresa...</div>';
            
            fetch(`/search-company/${cnpj}`)
                .then(response => response.json())
                .then(data => {
                    if (data.is_green) {
                        resultado.innerHTML = `
                            <div class="result success">
                                <strong>✅ Empresa Verde Encontrada!</strong><br>
                                <strong>Nome:</strong> ${data.nome}<br>
                                <strong>Score:</strong> ${data.green_score}/100<br>
                                <strong>Situação:</strong> ${data.situacao}
                            </div>
                        `;
                    } else {
                        resultado.innerHTML = `
                            <div class="result">
                                <strong>ℹ️ Empresa Encontrada (Não Verde)</strong><br>
                                <strong>Nome:</strong> ${data.nome}<br>
                                <strong>Score:</strong> ${data.green_score}/100<br>
                                <strong>Situação:</strong> ${data.situacao}
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    resultado.innerHTML = '<div class="result error">Erro: ' + error.message + '</div>';
                });
        }
        
        // Formatação de CNPJ
        document.getElementById('cnpj').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\\D/g, '');
            value = value.replace(/(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2})/, '$1.$2.$3/$4-$5');
            e.target.value = value;
        });
    </script>
</body>
</html>
            """)
        
        return templates.TemplateResponse("dashboard.html", {"request": request})
        
    except Exception as e:
        print(f"ERRO no dashboard: {e}")
        return HTMLResponse(f"<h1>Erro: {e}</h1>")

@app.get("/api/stats")
async def get_stats():
    """Estatísticas robustas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM empresas_verdes")
        total_empresas = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as total FROM cnae_green")
        total_cnaes = cursor.fetchone()["total"]
        
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
        score_medio = cursor.fetchone()["media"] or 0
        
        cursor.execute("SELECT COUNT(*) as total FROM empresa_cnae")
        total_relacoes = cursor.fetchone()["total"]
        
        conn.close()
        
        return {
            "total_empresas": total_empresas,
            "total_cnaes_verdes": total_cnaes,
            "score_medio": round(float(score_medio), 2),
            "total_relacoes": total_relacoes,
            "timestamp": datetime.now().isoformat(),
            "status": "OK"
        }
        
    except Exception as e:
        print(f"ERRO em stats: {e}")
        return {"error": str(e), "status": "ERROR"}

@app.get("/api/empresas")
async def get_empresas():
    """Lista robusta de empresas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cnpj, razao_social, nome_fantasia, score_verde, 
                   situacao_cadastral, municipio, uf, cnae_principal
            FROM empresas_verdes 
            ORDER BY score_verde DESC
        """)
        
        empresas = []
        for row in cursor.fetchall():
            empresas.append({
                "cnpj": row["cnpj"],
                "nome": row["razao_social"],
                "nome_fantasia": row["nome_fantasia"],
                "pontuacao_verde": row["score_verde"],
                "situacao": row["situacao_cadastral"],
                "municipio": row["municipio"],
                "uf": row["uf"],
                "cnae_principal": row["cnae_principal"]
            })
        
        conn.close()
        return {"empresas": empresas, "total": len(empresas), "status": "OK"}
        
    except Exception as e:
        print(f"ERRO em empresas: {e}")
        return {"error": str(e), "status": "ERROR"}

@app.get("/empresas", response_class=HTMLResponse)
async def empresas_page(request: Request):
    """Página visual de empresas"""
    try:
        template_path = TEMPLATES_DIR / "empresas_modernas.html"
        if template_path.exists():
            return templates.TemplateResponse("empresas_modernas.html", {"request": request})
        else:
            return HTMLResponse("<h1>Template de empresas não encontrado</h1>")
    except Exception as e:
        return HTMLResponse(f"<h1>Erro: {e}</h1>")

@app.get("/api/cnaes")
async def get_cnaes():
    """Lista robusta de CNAEs"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT cnae, titulo, prioridade FROM cnae_green ORDER BY cnae")
        
        cnaes = []
        for row in cursor.fetchall():
            pontuacao = {"Core": 100, "Adjacent": 70, "Secondary": 40}.get(row["prioridade"], 40)
            cnaes.append({
                "codigo": row["cnae"],
                "descricao": row["titulo"],
                "tipo": row["prioridade"],
                "pontuacao": pontuacao
            })
        
        conn.close()
        return {"cnaes": cnaes, "total": len(cnaes), "status": "OK"}
        
    except Exception as e:
        print(f"ERRO em CNAEs: {e}")
        return {"error": str(e), "status": "ERROR"}

@app.get("/cnaes", response_class=HTMLResponse)
async def cnaes_page(request: Request):
    """Página visual de CNAEs"""
    try:
        template_path = TEMPLATES_DIR / "cnaes_modernos.html"
        if template_path.exists():
            return templates.TemplateResponse("cnaes_modernos.html", {"request": request})
        else:
            return HTMLResponse("<h1>Template de CNAEs não encontrado</h1>")
    except Exception as e:
        return HTMLResponse(f"<h1>Erro: {e}</h1>")

@app.get("/search-company/{cnpj}")
async def search_company(cnpj: str):
    """Busca robusta de empresa"""
    try:
        result = processor.search_company_receita(cnpj)
        
        if not result:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        # Calcula score
        score = processor.calculate_green_score(result['cnaes'])
        
        return {
            "nome": result['nome'],
            "cnpj": result['cnpj'],
            "situacao": result['situacao'],
            "municipio": result.get('municipio'),
            "uf": result.get('uf'),
            "cnaes": result['cnaes'],
            "green_score": score,
            "is_green": score > 0,
            "status": "OK"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERRO na busca: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-company")
async def add_company(cnpj: str = Form(...)):
    """Adiciona empresa de forma robusta"""
    try:
        # Busca empresa
        result = processor.search_company_receita(cnpj)
        
        if not result:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        if result['situacao'] != 'ATIVA':
            raise HTTPException(status_code=400, detail=f"Empresa inativa: {result['situacao']}")
        
        # Calcula score
        score = processor.calculate_green_score(result['cnaes'])
        
        if score > 0:
            # Identifica CNAEs verdes
            green_cnaes = []
            for cnae in result['cnaes']:
                if processor.calculate_green_score([cnae]) > 0:
                    green_cnaes.append(cnae)
            
            # Prepara para salvar
            result['green_score'] = score
            result['green_cnaes'] = green_cnaes
            
            # Salva
            if processor.save_green_company(result):
                return {
                    "success": True,
                    "message": "Empresa verde adicionada com sucesso!",
                    "company": {
                        "nome": result['nome'],
                        "cnpj": result['cnpj'],
                        "score": score,
                        "cnaes_verdes": green_cnaes
                    },
                    "status": "OK"
                }
            else:
                raise HTTPException(status_code=500, detail="Erro ao salvar empresa")
        else:
            return {
                "success": False,
                "message": "Empresa não é verde",
                "company": {
                    "nome": result['nome'],
                    "cnpj": result['cnpj'],
                    "score": 0,
                    "cnaes": result['cnaes']
                },
                "status": "OK"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERRO ao adicionar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌱 GREEN JOBS BRASIL - VERSÃO DEFINITIVA")
    print("=" * 60)
    print(f"📂 Diretório base: {BASE_DIR}")
    print(f"💾 Banco de dados: {DATABASE_PATH}")
    print(f"📄 Templates: {TEMPLATES_DIR}")
    print(f"✅ CNAEs verdes carregados: {len(processor.green_cnaes)}")
    print("=" * 60)
    print("🚀 Iniciando servidor...")
    print("📍 Dashboard: http://127.0.0.1:8000")
    print("📖 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")