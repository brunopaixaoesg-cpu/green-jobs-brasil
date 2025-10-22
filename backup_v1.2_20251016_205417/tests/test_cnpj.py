#!/usr/bin/env python3
"""
Teste da funcionalidade de busca por CNPJ
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'etl'))

def test_cnpj_search():
    try:
        from etl.real_data_processor import RealDataProcessor
        
        print("🔍 TESTANDO BUSCA POR CNPJ NA RECEITA FEDERAL")
        print("=" * 50)
        
        processor = RealDataProcessor()
        
        # Testar com CNPJ real
        test_cnpj = "12345678000195"
        print(f"📝 Testando CNPJ: {test_cnpj}")
        
        result = processor.search_cnpj_receita_ws(test_cnpj)
        
        if result:
            print("✅ Busca funcionando!")
            print(f"Nome: {result.get('nome', 'N/A')}")
            print(f"Situação: {result.get('situacao', 'N/A')}")
            print(f"Município: {result.get('municipio', 'N/A')}")
            print(f"CNAEs: {len(result.get('atividade_principal', []) + result.get('atividades_secundarias', []))}")
            
            # Testar cálculo de score
            all_cnaes = []
            if result.get('atividade_principal'):
                all_cnaes.append(result['atividade_principal'])
            if result.get('atividades_secundarias'):
                all_cnaes.extend(result['atividades_secundarias'])
            
            print(f"CNAEs para análise: {all_cnaes}")
            score = processor.calculate_green_score(all_cnaes)
            print(f"Score Verde: {score}")
            
        else:
            print("❌ Busca retornou vazio")
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    test_cnpj_search()