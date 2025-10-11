"""
Green Jobs Brasil - Versão Ultra Simples
Launcher que sempre funciona - sem dependências complexas
"""
import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("🌱 GREEN JOBS BRASIL - SISTEMA SIMPLIFICADO 🌱")
    print("=" * 55)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("gjb_dev.db"):
        print("❌ Execute este script no diretório do projeto!")
        print("📁 Diretório atual:", os.getcwd())
        input("Pressione Enter para sair...")
        return
    
    print("✅ Banco de dados encontrado!")
    print("✅ Diretório correto!")
    
    # Tentar iniciar a API diretamente
    api_script = os.path.join("api", "sqlite_api.py")
    
    if os.path.exists(api_script):
        print(f"✅ Script da API encontrado: {api_script}")
        
        print("\n🚀 Iniciando API...")
        print("⏳ Aguarde alguns segundos...")
        
        try:
            # Executar API
            process = subprocess.Popen([sys.executable, api_script])
            
            # Aguardar API inicializar
            time.sleep(3)
            
            print("✅ API iniciada!")
            print("\n" + "="*50)
            print("🎉 SISTEMA PRONTO PARA USO!")
            print("="*50)
            print("📍 API: http://127.0.0.1:8000")
            print("📚 Documentação: http://127.0.0.1:8000/docs")
            print("🏢 Empresas: http://127.0.0.1:8000/empresas")
            print("📊 Estatísticas: http://127.0.0.1:8000/stats")
            print("="*50)
            
            # Perguntar se quer abrir no navegador
            choice = input("\n🌐 Abrir documentação no navegador? (s/n): ").lower()
            
            if choice in ['s', 'sim', 'y', 'yes', '']:
                print("🌐 Abrindo navegador...")
                webbrowser.open("http://127.0.0.1:8000/docs")
            
            print("\n⚠️  Para parar a API, feche este terminal ou pressione Ctrl+C")
            print("💡 Deixe este terminal aberto enquanto usar o sistema")
            
            # Aguardar processo terminar
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Parando API...")
                process.terminate()
                print("✅ API parada!")
                
        except Exception as e:
            print(f"❌ Erro ao iniciar API: {e}")
            print("💡 Tente executar manualmente: python api/sqlite_api.py")
    
    else:
        print(f"❌ Script da API não encontrado: {api_script}")
        print("💡 Verifique se todos os arquivos estão no lugar correto")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()