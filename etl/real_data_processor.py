"""
ETL para processar dados reais de empresas brasileiras
Sistema Green Jobs Brasil - Processamento de dados da Receita Federal
"""

import pandas as pd
import sqlite3
import requests
import time
from typing import Dict, List, Optional
import os
from pathlib import Path

class RealDataProcessor:
    def __init__(self, db_path: str = None):
        """Inicializa o processador de dados reais"""
        if db_path is None:
            # Caminho para o banco na raiz do projeto
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gjb_dev.db")
        else:
            self.db_path = db_path
        
        # CNAEs verdes já classificados no sistema
        self.green_cnaes = self._load_green_cnaes()
    
    def _load_green_cnaes(self) -> Dict[str, Dict]:
        """Carrega os CNAEs verdes já classificados"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT cnae, titulo, prioridade FROM cnae_green"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        green_cnaes = {}
        for _, row in df.iterrows():
            green_cnaes[row['cnae']] = {
                'descricao': row['titulo'],
                'classificacao': row['prioridade']
            }
        return green_cnaes
    
    def calculate_green_score(self, cnaes: List[str]) -> int:
        """Calcula a pontuação verde baseado nos CNAEs da empresa"""
        if not cnaes:
            return 0
        
        total_score = 0
        green_cnaes_count = 0
        matched_cnaes = []
        
        for cnae in cnaes:
            # Normaliza o CNAE removendo pontuação e padronizando formato
            cnae_normalized = self._normalize_cnae(cnae)
            
            # Busca por CNAE exato ou similar
            for green_cnae, info in self.green_cnaes.items():
                green_cnae_normalized = self._normalize_cnae(green_cnae)
                
                if cnae_normalized == green_cnae_normalized:
                    green_cnaes_count += 1
                    matched_cnaes.append(f"{cnae} -> {green_cnae}")
                    
                    # Pontuação baseada na classificação
                    if info['classificacao'] == 'Core':
                        total_score += 100
                    elif info['classificacao'] == 'Adjacent':
                        total_score += 70
                    elif info['classificacao'] == 'Secondary':
                        total_score += 40
                    break
        
        if green_cnaes_count == 0:
            return 0
        
        # Debug: mostra CNAEs encontrados
        print(f"   CNAEs verdes encontrados: {matched_cnaes}")
        
        # Média ponderada considerando total de CNAEs
        base_score = total_score / green_cnaes_count
        
        # Bonus se tem muitos CNAEs verdes
        green_ratio = green_cnaes_count / len(cnaes)
        bonus = green_ratio * 20  # Até 20 pontos de bonus
        
        final_score = min(100, int(base_score + bonus))
        return final_score
    
    def _normalize_cnae(self, cnae: str) -> str:
        """Normaliza CNAE para comparação (remove pontuação e padroniza)"""
        if not cnae or cnae == '00.00-0-00':
            return ''
        
        # Remove todos os caracteres não numéricos
        digits_only = ''.join(filter(str.isdigit, str(cnae)))
        
        # Garante que tenha pelo menos 7 dígitos
        if len(digits_only) >= 7:
            # Formato padrão: XXXXXXX (7 dígitos)
            return digits_only[:7]
        elif len(digits_only) >= 4:
            # Se tem pelo menos 4 dígitos, compara os primeiros 4
            return digits_only[:4].ljust(7, '0')
        
        return digits_only
    
    def search_cnpj_receita_ws(self, cnpj: str) -> Optional[Dict]:
        """Busca dados de uma empresa pelo CNPJ usando ReceitaWS"""
        try:
            # Remove formatação do CNPJ
            cnpj_clean = ''.join(filter(str.isdigit, cnpj))
            
            # API da ReceitaWS (gratuita com limite)
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
    
    def process_cnpj_list(self, cnpj_list: List[str]) -> List[Dict]:
        """Processa uma lista de CNPJs e retorna empresas verdes"""
        green_companies = []
        
        for i, cnpj in enumerate(cnpj_list):
            print(f"Processando {i+1}/{len(cnpj_list)}: {cnpj}")
            
            # Busca dados da empresa
            company_data = self.search_cnpj_receita_ws(cnpj)
            
            if company_data and company_data['situacao'] == 'ATIVA':
                # Coleta todos os CNAEs
                all_cnaes = []
                if company_data['atividade_principal']:
                    all_cnaes.append(company_data['atividade_principal'])
                if company_data['atividades_secundarias']:
                    all_cnaes.extend(company_data['atividades_secundarias'])
                
                # Calcula pontuação verde
                green_score = self.calculate_green_score(all_cnaes)
                
                # Se tem pontuação verde, adiciona à lista
                if green_score > 0:
                    company_data['green_score'] = green_score
                    company_data['green_cnaes'] = [cnae for cnae in all_cnaes if any(cnae.replace('.','').replace('-','') == gc.replace('.','').replace('-','') for gc in self.green_cnaes.keys())]
                    green_companies.append(company_data)
                    
                    print(f"✅ Empresa verde encontrada: {company_data['nome']} (Score: {green_score})")
                else:
                    print(f"❌ Empresa não verde: {company_data['nome']}")
            
            # Delay para não sobrecarregar a API
            time.sleep(1)  # 1 segundo entre requisições
        
        return green_companies
    
    def save_green_companies(self, companies: List[Dict]):
        """Salva empresas verdes no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for company in companies:
            try:
                # Insere empresa - usar esquema atual
                cursor.execute("""
                    INSERT OR REPLACE INTO empresas_verdes 
                    (cnpj, razao_social, nome_fantasia, score_verde, situacao_cadastral, municipio, uf, cnae_principal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    company['cnpj'],
                    company['nome'],
                    company.get('fantasia'),
                    company['green_score'],
                    company['situacao'],
                    company.get('municipio'),
                    company.get('uf'),
                    company.get('atividade_principal')
                ))
                
                # Insere relacionamentos com CNAEs verdes
                for cnae in company.get('green_cnaes', []):
                    cursor.execute("""
                        INSERT OR REPLACE INTO empresa_cnae (cnpj, codigo_cnae)
                        VALUES (?, ?)
                    """, (company['cnpj'], cnae))
                
                print(f"✅ Empresa salva: {company['nome']}")
                
            except Exception as e:
                print(f"❌ Erro ao salvar empresa {company['nome']}: {str(e)}")
        
        conn.commit()
        conn.close()
    
    def process_receita_federal_csv(self, csv_path: str, sample_size: int = 1000):
        """Processa arquivo CSV da Receita Federal (versão otimizada)"""
        print(f"Processando arquivo CSV da Receita Federal: {csv_path}")
        
        # Lê apenas uma amostra do arquivo (muito grande)
        chunk_size = 10000
        green_companies = []
        processed = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, encoding='latin-1', sep=';'):
            for _, row in chunk.iterrows():
                if processed >= sample_size:
                    break
                
                # Extrai CNAEs da linha
                cnae_principal = row.get('cnae_fiscal_principal')
                cnaes_secundarios = str(row.get('cnae_fiscal_secundaria', '')).split(',') if pd.notna(row.get('cnae_fiscal_secundaria')) else []
                
                all_cnaes = [cnae_principal] + cnaes_secundarios if cnae_principal else cnaes_secundarios
                all_cnaes = [cnae.strip() for cnae in all_cnaes if cnae and str(cnae).strip()]
                
                # Calcula pontuação verde
                green_score = self.calculate_green_score(all_cnaes)
                
                if green_score > 0:
                    green_company = {
                        'cnpj': row.get('cnpj'),
                        'nome': row.get('razao_social'),
                        'fantasia': row.get('nome_fantasia'),
                        'green_score': green_score,
                        'situacao': row.get('situacao_cadastral'),
                        'municipio': row.get('municipio'),
                        'uf': row.get('uf'),
                        'cep': row.get('cep'),
                        'green_cnaes': [cnae for cnae in all_cnaes if any(cnae.replace('.','').replace('-','') == gc.replace('.','').replace('-','') for gc in self.green_cnaes.keys())]
                    }
                    green_companies.append(green_company)
                    print(f"✅ Empresa verde encontrada: {green_company['nome']} (Score: {green_score})")
                
                processed += 1
            
            if processed >= sample_size:
                break
        
        print(f"Processamento concluído. {len(green_companies)} empresas verdes encontradas.")
        return green_companies

def main():
    """Exemplo de uso do processador"""
    processor = RealDataProcessor()
    
    # Exemplo 1: Buscar CNPJs específicos
    print("=== EXEMPLO 1: Busca por CNPJs específicos ===")
    cnpjs_exemplo = [
        "34.028.316/0001-96",  # Ambev
        "33.592.510/0001-54",  # Magazine Luiza
        "04.814.563/0001-74",  # WEG
        "02.558.157/0001-62",  # JBS
    ]
    
    companies = processor.process_cnpj_list(cnpjs_exemplo)
    if companies:
        processor.save_green_companies(companies)
    
    print(f"\n✅ Processamento concluído! {len(companies)} empresas verdes encontradas e salvas.")

if __name__ == "__main__":
    main()