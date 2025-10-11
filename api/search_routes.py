"""
Interface web melhorada para adicionar empresas
Adiciona rota para buscar e adicionar empresas via CNPJ
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from etl.real_data_processor import RealDataProcessor

# Adiciona rota à API existente
def add_search_routes(app: FastAPI):
    """Adiciona rotas de busca à API existente"""
    
    templates = Jinja2Templates(directory="templates")
    
    @app.post("/add-company")
    async def add_company(request: Request, cnpj: str = Form(...)):
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
    
    @app.get("/search-company/{cnpj}")
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

# Script para adicionar as rotas à API atual
if __name__ == "__main__":
    print("🔧 Para adicionar funcionalidade de busca ao dashboard:")
    print("1. Adicione as rotas ao sqlite_api.py")
    print("2. Atualize o template HTML com formulário de busca")
    print("3. Reinicie a API")