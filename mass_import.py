"""
Importador de dados em massa da Receita Federal
Sistema Green Jobs Brasil - Processamento de milhares de empresas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from etl.real_data_processor import RealDataProcessor
import requests
import zipfile
from pathlib import Path
import pandas as pd

class MassDataImporter:
    def __init__(self):
        self.processor = RealDataProcessor()
        self.data_dir = Path("data/receita_federal")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def download_receita_data(self):
        """Baixa dados da Receita Federal (simulado - URLs reais variam)"""
        print("📥 Preparando download dos dados da Receita Federal...")
        print("ℹ️  IMPORTANTE: Os dados da Receita Federal são muito grandes (>10GB)")
        print("ℹ️  Para este exemplo, vamos simular com dados menores")
        
        # URLs reais da Receita Federal (exemplo)
        # http://200.152.38.155/CNPJ/dados_abertos_cnpj/
        
        confirm = input("Deseja continuar com simulação de dados? (s/n): ").lower().strip()
        if confirm != 's':
            return False
        
        return True
    
    def generate_sample_companies(self, count: int = 1000) -> list:
        """Gera empresas exemplo para demonstração"""
        print(f"🏭 Gerando {count} empresas exemplo...")
        
        # CNPJs de empresas reais conhecidas (algumas podem ser verdes)
        real_cnpjs = [
            "34.028.316/0001-96",  # Ambev
            "33.592.510/0001-54",  # Magazine Luiza  
            "04.814.563/0001-74",  # WEG
            "02.558.157/0001-62",  # JBS
            "33.000.167/0001-01",  # Petrobras
            "60.746.948/0001-12",  # Vale
            "17.184.037/0001-74",  # Suzano
            "02.012.862/0001-91",  # Klabin
            "61.186.888/0001-74",  # Cemig
            "02.998.611/0001-04",  # Copel
            "04.332.034/0001-56",  # Engie Brasil
            "09.168.704/0001-42",  # EDP Brasil
            "07.526.557/0001-00",  # Enel Brasil
            "04.593.842/0001-04",  # Braskem
            "17.190.134/0001-80",  # Fibria (fusão Suzano)
        ]
        
        return real_cnpjs[:min(count, len(real_cnpjs))]
    
    def process_priority_sectors(self):
        """Processa setores prioritários para empresas verdes"""
        print("🎯 Processando setores prioritários...")
        
        # CNAEs verdes prioritários
        priority_cnaes = [
            "35.11-5",  # Geração energia renovável
            "38.11-4",  # Coleta de resíduos
            "38.21-1",  # Tratamento de resíduos
            "71.12-1",  # Engenharia ambiental
            "84.13-4",  # Administração ambiental
        ]
        
        print(f"📊 CNAEs prioritários: {', '.join(priority_cnaes)}")
        
        # Aqui você conectaria com base real da Receita Federal
        # Por enquanto, usamos CNPJs exemplo
        sample_companies = self.generate_sample_companies(50)
        
        print(f"🔄 Processando {len(sample_companies)} empresas exemplo...")
        green_companies = self.processor.process_cnpj_list(sample_companies)
        
        if green_companies:
            print(f"✅ {len(green_companies)} empresas verdes encontradas!")
            self.processor.save_green_companies(green_companies)
            return len(green_companies)
        
        return 0
    
    def import_regional_data(self, uf: str = None):
        """Importa dados de uma região específica"""
        if uf:
            print(f"🗺️  Importando dados da região: {uf}")
        else:
            print("🗺️  Importando dados nacionais...")
        
        # Em implementação real, filtraria por UF na base da Receita
        sample_companies = self.generate_sample_companies(100)
        
        green_companies = self.processor.process_cnpj_list(sample_companies)
        
        if green_companies:
            print(f"✅ {len(green_companies)} empresas verdes encontradas na região!")
            self.processor.save_green_companies(green_companies)
            return len(green_companies)
        
        return 0
    
    def show_statistics(self):
        """Mostra estatísticas dos dados importados"""
        import sqlite3
        
        conn = sqlite3.connect(self.processor.db_path)
        cursor = conn.cursor()
        
        # Total de empresas
        cursor.execute("SELECT COUNT(*) FROM empresas_verdes")
        total_empresas = cursor.fetchone()[0]
        
        # Por estado
        cursor.execute("SELECT uf, COUNT(*) as count FROM empresas_verdes GROUP BY uf ORDER BY count DESC")
        por_estado = cursor.fetchall()
        
        # Por score
        cursor.execute("SELECT green_score, COUNT(*) as count FROM empresas_verdes GROUP BY green_score ORDER BY green_score DESC")
        por_score = cursor.fetchall()
        
        # Top empresas
        cursor.execute("SELECT nome, green_score, uf FROM empresas_verdes ORDER BY green_score DESC LIMIT 10")
        top_empresas = cursor.fetchall()
        
        conn.close()
        
        print("\n📊 ESTATÍSTICAS DOS DADOS")
        print("=" * 50)
        print(f"Total de empresas verdes: {total_empresas}")
        
        if por_estado:
            print(f"\n🗺️  Por Estado:")
            for uf, count in por_estado[:10]:  # Top 10
                print(f"   {uf or 'N/A'}: {count} empresas")
        
        if por_score:
            print(f"\n⭐ Por Pontuação:")
            for score, count in por_score[:5]:  # Top 5 scores
                print(f"   Score {score}: {count} empresas")
        
        if top_empresas:
            print(f"\n🏆 Top 10 Empresas Mais Verdes:")
            for i, (nome, score, uf) in enumerate(top_empresas, 1):
                print(f"   {i}. {nome} - {score}/100 ({uf or 'N/A'})")

def main():
    """Menu principal do importador"""
    print("🌱 GREEN JOBS BRASIL - Importador de Dados em Massa")
    print("=" * 60)
    
    importer = MassDataImporter()
    
    while True:
        print("\nOpções de Importação:")
        print("1. Processar setores prioritários (~50 empresas)")
        print("2. Importar por região/estado")
        print("3. Baixar dados da Receita Federal (completo)")
        print("4. Ver estatísticas dos dados")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == '1':
            print("\n🎯 PROCESSANDO SETORES PRIORITÁRIOS")
            count = importer.process_priority_sectors()
            print(f"✅ Processamento concluído! {count} empresas verdes adicionadas.")
        
        elif choice == '2':
            uf = input("Digite a UF (ou Enter para todos): ").strip().upper()
            uf = uf if uf else None
            count = importer.import_regional_data(uf)
            print(f"✅ Processamento concluído! {count} empresas verdes adicionadas.")
        
        elif choice == '3':
            print("\n📥 DOWNLOAD DADOS RECEITA FEDERAL")
            if importer.download_receita_data():
                print("ℹ️  Em uma implementação real, aqui baixaríamos os dados completos")
                print("ℹ️  Por agora, use as opções 1 ou 2 para dados exemplo")
        
        elif choice == '4':
            importer.show_statistics()
        
        elif choice == '5':
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()