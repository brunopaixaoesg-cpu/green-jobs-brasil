"""
Busca individual de empresa por CNPJ
Sistema Green Jobs Brasil - Verificação se empresa é verde
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from etl.real_data_processor import RealDataProcessor
import sqlite3

def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ para exibição"""
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj_clean) == 14:
        return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"
    return cnpj

def search_company(cnpj: str):
    """Busca uma empresa específica por CNPJ"""
    print(f"\n🔍 Buscando empresa com CNPJ: {format_cnpj(cnpj)}")
    print("=" * 60)
    
    processor = RealDataProcessor()
    
    # Primeiro verifica se já está no banco
    conn = sqlite3.connect(processor.db_path)
    cursor = conn.cursor()
    
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    cursor.execute("SELECT * FROM empresas_verdes WHERE cnpj LIKE ?", (f"%{cnpj_clean}%",))
    existing = cursor.fetchone()
    
    if existing:
        print("✅ Empresa encontrada no banco local:")
        print(f"   Nome: {existing[1]}")  # razao_social
        print(f"   CNPJ: {existing[0]}")
        print(f"   Score Verde: {existing[10]}/100")  # score_verde
        print(f"   Situação: {existing[8]}")  # situacao_cadastral
        print(f"   Cidade: {existing[7]}, {existing[6]}")  # municipio, uf
        
        # Busca CNAEs relacionados
        cursor.execute("""
            SELECT codigo_cnae FROM empresa_cnae 
            WHERE cnpj LIKE ?
        """, (f"%{cnpj_clean}%",))
        cnaes = [row[0] for row in cursor.fetchall()]
        
        if cnaes:
            print(f"   CNAEs Verdes: {', '.join(cnaes)}")
        
        conn.close()
        return
    
    conn.close()
    
    # Se não está no banco, busca na Receita Federal
    print("🌐 Buscando na Receita Federal...")
    company_data = processor.search_cnpj_receita_ws(cnpj)
    
    if not company_data:
        print("❌ Empresa não encontrada ou erro na consulta")
        return
    
    if company_data['situacao'] != 'ATIVA':
        print(f"⚠️  Empresa encontrada mas não está ATIVA (Status: {company_data['situacao']})")
        return
    
    # Coleta CNAEs
    all_cnaes = []
    if company_data['atividade_principal']:
        all_cnaes.append(company_data['atividade_principal'])
    if company_data['atividades_secundarias']:
        all_cnaes.extend(company_data['atividades_secundarias'])
    
    # Calcula score verde
    green_score = processor.calculate_green_score(all_cnaes)
    
    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"   Nome: {company_data['nome']}")
    print(f"   Fantasia: {company_data.get('fantasia', 'N/A')}")
    print(f"   CNPJ: {company_data['cnpj']}")
    print(f"   Score Verde: {green_score}/100")
    
    if green_score > 0:
        print(f"   🌱 EMPRESA VERDE! 🌱")
        
        # Identifica CNAEs verdes
        green_cnaes = []
        for cnae in all_cnaes:
            for green_cnae in processor.green_cnaes.keys():
                if cnae.replace('.','').replace('-','') == green_cnae.replace('.','').replace('-',''):
                    green_cnaes.append(f"{cnae} - {processor.green_cnaes[green_cnae]['descricao']}")
                    break
        
        if green_cnaes:
            print(f"   CNAEs Verdes identificados:")
            for cnae_info in green_cnaes:
                print(f"     • {cnae_info}")
        
        # Pergunta se quer salvar
        save = input(f"\n💾 Deseja salvar esta empresa no banco? (s/n): ").lower().strip()
        if save == 's':
            company_data['green_score'] = green_score
            company_data['green_cnaes'] = [cnae.split(' - ')[0] for cnae in green_cnaes]
            processor.save_green_companies([company_data])
            print("✅ Empresa salva com sucesso!")
    
    else:
        print(f"   ❌ Empresa NÃO é verde")
        print(f"   Motivo: Nenhum CNAE verde identificado")
        print(f"   CNAEs da empresa: {', '.join(all_cnaes) if all_cnaes else 'Nenhum encontrado'}")
    
    print(f"   Localização: {company_data.get('municipio', 'N/A')}, {company_data.get('uf', 'N/A')}")
    print(f"   Situação: {company_data['situacao']}")

def batch_search():
    """Busca em lote de CNPJs"""
    print("\n📋 BUSCA EM LOTE")
    print("Digite os CNPJs (um por linha), ou 'fim' para terminar:")
    
    cnpjs = []
    while True:
        cnpj = input("CNPJ: ").strip()
        if cnpj.lower() == 'fim':
            break
        if cnpj:
            cnpjs.append(cnpj)
    
    if not cnpjs:
        print("Nenhum CNPJ fornecido.")
        return
    
    print(f"\n🔄 Processando {len(cnpjs)} empresas...")
    processor = RealDataProcessor()
    companies = processor.process_cnpj_list(cnpjs)
    
    if companies:
        print(f"\n✅ {len(companies)} empresas verdes encontradas!")
        processor.save_green_companies(companies)
    else:
        print("❌ Nenhuma empresa verde encontrada.")

def main():
    """Menu principal"""
    print("🌱 GREEN JOBS BRASIL - Verificador de Empresas Verdes")
    print("=" * 60)
    
    while True:
        print("\nOpções:")
        print("1. Buscar empresa por CNPJ")
        print("2. Busca em lote (múltiplos CNPJs)")
        print("3. Sair")
        
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == '1':
            cnpj = input("\nDigite o CNPJ: ").strip()
            if cnpj:
                search_company(cnpj)
        
        elif choice == '2':
            batch_search()
        
        elif choice == '3':
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()