"""
Green Jobs Brasil - API Completa e Funcional
Versão otimizada com busca de empresas reais integrada
"""
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import sqlite3
import uvicorn
from datetime import datetime
import os
import sys
import requests
import time

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI(
    title="Green Jobs Brasil API",
    description="API para consulta e adição de empresas verdes no Brasil",
    version="2.0.0"
)

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")  # Comentado - não usado

# Caminho para o banco de dados
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gjb_dev.db")

def get_db_connection():
    """Cria conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Classe para processamento de dados reais
class RealDataProcessor:
    def __init__(self):
        self.green_cnaes = self._load_green_cnaes()
    
    def _load_green_cnaes(self):
        """Carrega CNAEs verdes do banco"""
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
    
    def _normalize_cnae(self, cnae):
        """Normaliza CNAE para comparação"""
        if not cnae or cnae == '00.00-0-00':
            return ''
        
        # Remove todos os caracteres não numéricos
        digits_only = ''.join(filter(str.isdigit, str(cnae)))
        
        # Garante que tenha pelo menos 7 dígitos
        if len(digits_only) >= 7:
            return digits_only[:7]
        elif len(digits_only) >= 4:
            return digits_only[:4].ljust(7, '0')
        
        return digits_only
    
    def calculate_green_score(self, cnaes):
        """Calcula score verde baseado nos CNAEs"""
        if not cnaes:
            return 0
        
        total_score = 0
        green_cnaes_count = 0
        
        for cnae in cnaes:
            cnae_normalized = self._normalize_cnae(cnae)
            
            for green_cnae, info in self.green_cnaes.items():
                green_cnae_normalized = self._normalize_cnae(green_cnae)
                
                if cnae_normalized == green_cnae_normalized:
                    green_cnaes_count += 1
                    
                    if info['classificacao'] == 'Core':
                        total_score += 100
                    elif info['classificacao'] == 'Adjacent':
                        total_score += 70
                    elif info['classificacao'] == 'Secondary':
                        total_score += 40
                    break
        
        if green_cnaes_count == 0:
            return 0
        
        # Média ponderada
        base_score = total_score / green_cnaes_count
        
        # Bonus por proporção de CNAEs verdes
        green_ratio = green_cnaes_count / len(cnaes)
        bonus = green_ratio * 20
        
        final_score = min(100, int(base_score + bonus))
        return final_score
    
    def search_cnpj_receita_ws(self, cnpj):
        """Busca empresa na Receita Federal"""
        try:
            cnpj_clean = ''.join(filter(str.isdigit, cnpj))
            url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    return {
                        'cnpj': data.get('cnpj'),
                        'nome': data.get('nome'),
                        'fantasia': data.get('fantasia'),
                        'situacao': data.get('situacao'),
                        'atividade_principal': data.get('atividade_principal', [{}])[0].get('code') if data.get('atividade_principal') else None,
                        'atividades_secundarias': [ativ.get('code') for ativ in data.get('atividades_secundarias', [])],
                        'municipio': data.get('municipio'),
                        'uf': data.get('uf'),
                        'cep': data.get('cep'),
                        'telefone': data.get('telefone'),
                        'email': data.get('email')
                    }
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar CNPJ {cnpj}: {str(e)}")
            return None
    
    def save_green_company(self, company_data):
        """Salva empresa verde no banco"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
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
                company_data.get('atividade_principal')
            ))
            
            # Salva relacionamentos com CNAEs verdes
            for cnae in company_data.get('green_cnaes', []):
                cursor.execute("""
                    INSERT OR REPLACE INTO empresa_cnae (cnpj, codigo_cnae)
                    VALUES (?, ?)
                """, (company_data['cnpj'], cnae))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao salvar empresa: {str(e)}")
            return False

# Instância do processador
processor = RealDataProcessor()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal do dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/stats")
async def get_stats():
    """Estatísticas do sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de empresas
        cursor.execute("SELECT COUNT(*) as total FROM empresas_verdes")
        total_empresas = cursor.fetchone()["total"]
        
        # Total de CNAEs
        cursor.execute("SELECT COUNT(*) as total FROM cnae_green")
        total_cnaes = cursor.fetchone()["total"]
        
        # Score médio
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
        score_medio = cursor.fetchone()["media"] or 0
        
        # Total de relações
        cursor.execute("SELECT COUNT(*) as total FROM empresa_cnae")
        total_relacoes = cursor.fetchone()["total"]
        
        conn.close()
        
        return {
            "total_empresas": total_empresas,
            "total_cnaes_verdes": total_cnaes,
            "score_medio": float(score_medio),
            "total_relacoes": total_relacoes,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/empresas")
async def get_empresas():
    """Lista todas as empresas verdes"""
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
        return empresas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cnaes")
async def get_cnaes():
    """Lista todos os CNAEs verdes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT cnae, titulo, prioridade FROM cnae_green ORDER BY cnae")
        
        cnaes = []
        for row in cursor.fetchall():
            pontuacao = 100 if row["prioridade"] == "Core" else 70 if row["prioridade"] == "Adjacent" else 40
            cnaes.append({
                "codigo": row["cnae"],
                "descricao": row["titulo"],
                "tipo": row["prioridade"],
                "pontuacao": pontuacao
            })
        
        conn.close()
        return cnaes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search-company/{cnpj}")
async def search_company(cnpj: str):
    """Busca empresa por CNPJ na Receita Federal"""
    try:
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

@app.post("/add-company")
async def add_company(cnpj: str = Form(...)):
    """Adiciona empresa verde ao sistema"""
    try:
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
            # Identifica CNAEs verdes
            green_cnaes = []
            for cnae in all_cnaes:
                if processor.calculate_green_score([cnae]) > 0:
                    green_cnaes.append(cnae)
            
            # Prepara dados para salvar
            result['green_score'] = score
            result['green_cnaes'] = green_cnaes
            
            # Salva no banco
            if processor.save_green_company(result):
                return {
                    "success": True,
                    "message": "Empresa verde adicionada com sucesso!",
                    "company": {
                        "nome": result['nome'],
                        "cnpj": result['cnpj'],
                        "score": score,
                        "cnaes_verdes": green_cnaes
                    }
                }
            else:
                raise HTTPException(status_code=500, detail="Erro ao salvar empresa")
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
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌱 GREEN JOBS BRASIL - Iniciando API Completa")
    print("=" * 50)
    print("📍 Dashboard: http://127.0.0.1:8000")
    print("📖 Docs: http://127.0.0.1:8000/docs")
    print("🔍 Funcionalidades:")
    print("   • Busca empresas na Receita Federal")
    print("   • Classifica automaticamente como verde")
    print("   • Dashboard moderno e responsivo") 
    print("   • API REST completa")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)