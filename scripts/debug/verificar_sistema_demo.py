import os
import sys
import sqlite3
import requests
import time

def verificar_sistema_completo():
    """Verificação completa do sistema Green Jobs Brasil"""
    print("🔍 VERIFICAÇÃO SISTEMA GREEN JOBS BRASIL")
    print("=" * 50)
    
    erros = []
    sucessos = []
    
    # 1. Verificar Python
    print("\n1️⃣ Python...")
    try:
        python_version = sys.version
        print(f"   ✅ Python {python_version[:5]} detectado")
        sucessos.append("Python instalado")
    except Exception as e:
        print(f"   ❌ Erro Python: {e}")
        erros.append("Python não encontrado")
    
    # 2. Verificar estrutura de arquivos
    print("\n2️⃣ Estrutura de arquivos...")
    arquivos_essenciais = [
        "start_api.py",
        "api/sqlite_api_clean.py", 
        "api/templates/listar_vagas.html",
        "api/templates/dashboard_empresa.html",
        "api/templates/cadastro_empresa.html",
        "api/templates/criar_vaga.html"
    ]
    
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
            sucessos.append(f"Arquivo {arquivo}")
        else:
            print(f"   ❌ {arquivo} não encontrado")
            erros.append(f"Arquivo {arquivo} ausente")
    
    # 3. Verificar banco de dados
    print("\n3️⃣ Banco de dados...")
    try:
        if os.path.exists("api/gjb_dev.db"):
            from scripts.db_wrapper import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
            
            # Verificar tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabelas = [t[0] for t in cursor.fetchall()]
            print(f"   ✅ Banco existe com {len(tabelas)} tabelas")
            
            # Verificar dados
            cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
            profissionais = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM empresas_esg")
            empresas = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM vagas")
            vagas = cursor.fetchone()[0]
            
            print(f"   📊 {profissionais} profissionais, {empresas} empresas, {vagas} vagas")
            
            if profissionais > 0 and empresas > 0 and vagas > 0:
                sucessos.append("Banco populado")
            else:
                erros.append("Banco vazio - execute popular_profissionais_completo.py")
            
            # connection closed by context manager
        else:
            print("   ❌ Banco não existe")
            erros.append("Banco de dados ausente")
            
    except Exception as e:
        print(f"   ❌ Erro no banco: {e}")
        erros.append(f"Erro banco: {e}")
    
    # 4. Tentar iniciar API (se não estiver rodando)
    print("\n4️⃣ API Status...")
    try:
        response = requests.get("http://127.0.0.1:8002/api/vagas", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API rodando - {data.get('total', 0)} vagas disponíveis")
            sucessos.append("API funcionando")
        else:
            print(f"   ⚠️ API respondeu com status {response.status_code}")
            erros.append("API com problemas")
    except requests.exceptions.ConnectionError:
        print("   ⚠️ API não está rodando")
        print("      💡 Execute: python start_api.py")
        erros.append("API não iniciada")
    except Exception as e:
        print(f"   ❌ Erro na API: {e}")
        erros.append(f"Erro API: {e}")
    
    # 5. Verificar templates
    print("\n5️⃣ Templates...")
    templates_dir = "api/templates"
    if os.path.exists(templates_dir):
        templates = len([f for f in os.listdir(templates_dir) if f.endswith('.html')])
        print(f"   ✅ {templates} templates HTML encontrados")
        sucessos.append(f"{templates} templates")
    else:
        print("   ❌ Diretório templates não encontrado")
        erros.append("Templates ausentes")
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📋 RELATÓRIO FINAL")
    print("=" * 50)
    
    print(f"\n✅ SUCESSOS ({len(sucessos)}):")
    for sucesso in sucessos:
        print(f"   • {sucesso}")
    
    if erros:
        print(f"\n❌ PROBLEMAS ({len(erros)}):")
        for erro in erros:
            print(f"   • {erro}")
    
    # Status geral
    if len(erros) == 0:
        print("\n🎉 SISTEMA 100% OPERACIONAL!")
        print("   Execute: python start_api.py")
        print("   Acesse: http://127.0.0.1:8002/vagas")
        return True
    elif len(erros) <= 2:
        print("\n⚠️ SISTEMA QUASE PRONTO!")
        print("   Corrija os problemas acima")
        return False
    else:
        print("\n🚨 SISTEMA COM PROBLEMAS!")
        print("   Verifique instalação e arquivos")
        return False

if __name__ == "__main__":
    try:
        verificar_sistema_completo()
    except KeyboardInterrupt:
        print("\n\n⏹️ Verificação interrompida pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
    
    print("\nPressione Enter para sair...")
    input()