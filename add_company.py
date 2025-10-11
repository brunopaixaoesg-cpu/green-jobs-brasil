"""
Busca e adiciona empresa verde via CNPJ - Versão Simplificada
Uso: python add_company.py [CNPJ]
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from etl.real_data_processor import RealDataProcessor

def add_company_by_cnpj(cnpj: str):
    """Adiciona uma empresa via CNPJ se for verde"""
    print(f"🔍 Buscando empresa: {cnpj}")
    print("-" * 50)
    
    processor = RealDataProcessor()
    result = processor.search_cnpj_receita_ws(cnpj)
    
    if not result:
        print("❌ Empresa não encontrada na Receita Federal")
        return False
    
    if result['situacao'] != 'ATIVA':
        print(f"⚠️  Empresa não está ativa (Status: {result['situacao']})")
        return False
    
    print(f"✅ Empresa encontrada: {result['nome']}")
    
    # Coleta CNAEs
    all_cnaes = []
    if result['atividade_principal']:
        all_cnaes.append(result['atividade_principal'])
    if result['atividades_secundarias']:
        all_cnaes.extend(result['atividades_secundarias'])
    
    print(f"📋 CNAEs: {', '.join(all_cnaes)}")
    
    # Calcula score
    score = processor.calculate_green_score(all_cnaes)
    print(f"🌱 Score Verde: {score}/100")
    
    if score > 0:
        print("✅ EMPRESA VERDE! Salvando no banco...")
        
        # Identifica CNAEs verdes
        green_cnaes = []
        for cnae in all_cnaes:
            if processor.calculate_green_score([cnae]) > 0:
                green_cnaes.append(cnae)
        
        result['green_score'] = score
        result['green_cnaes'] = green_cnaes
        processor.save_green_companies([result])
        
        print(f"✅ Empresa salva com sucesso!")
        print(f"   Nome: {result['nome']}")
        print(f"   CNPJ: {result['cnpj']}")
        print(f"   Score: {score}/100")
        print(f"   CNAEs Verdes: {', '.join(green_cnaes)}")
        
        return True
    else:
        print("❌ Empresa não é verde (nenhum CNAE verde identificado)")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # CNPJ passado como argumento
        cnpj = sys.argv[1]
        add_company_by_cnpj(cnpj)
    else:
        # Modo interativo
        print("🌱 ADICIONAR EMPRESA VERDE")
        print("=" * 40)
        
        while True:
            cnpj = input("\nDigite o CNPJ (ou 'sair' para terminar): ").strip()
            
            if cnpj.lower() in ['sair', 'exit', 'quit', '']:
                break
            
            if cnpj:
                add_company_by_cnpj(cnpj)
                print("\n" + "="*40)
        
        print("👋 Até logo!")

if __name__ == "__main__":
    main()