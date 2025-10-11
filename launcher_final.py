"""
Green Jobs Brasil - Launcher Final
Versão otimizada e completamente funcional
"""
import subprocess
import time
import webbrowser
import os
import sys

def main():
    print("🌱 GREEN JOBS BRASIL - Sistema de Empresas Verdes")
    print("=" * 60)
    print("Inicializando sistema...")
    
    # Caminho para a API final
    api_path = os.path.join(os.path.dirname(__file__), "api", "final_api.py")
    
    try:
        # Pergunta se quer abrir o navegador
        open_browser = input("\n🌐 Abrir dashboard no navegador? (s/n) [s]: ").lower().strip()
        if open_browser == '' or open_browser == 's':
            print("📡 Iniciando servidor...")
            
            # Inicia o servidor em background
            process = subprocess.Popen([
                sys.executable, api_path
            ], cwd=os.path.dirname(__file__))
            
            # Aguarda servidor inicializar
            print("⏳ Aguardando servidor inicializar...")
            time.sleep(3)
            
            # Abre navegador
            print("🌐 Abrindo dashboard...")
            webbrowser.open("http://127.0.0.1:8000")
            
            print("\n✅ Sistema iniciado com sucesso!")
            print("📍 Dashboard: http://127.0.0.1:8000")
            print("📖 API Docs: http://127.0.0.1:8000/docs")
            print("\n🔍 Funcionalidades:")
            print("   • Digite qualquer CNPJ brasileiro")
            print("   • Sistema verifica se é empresa verde")
            print("   • Adiciona automaticamente ao banco")
            print("   • Dashboard atualiza em tempo real")
            print("\n⚠️  Para parar: Feche esta janela ou pressione Ctrl+C")
            
            # Mantém processo rodando
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n👋 Encerrando sistema...")
                process.terminate()
        else:
            print("📡 Iniciando apenas o servidor...")
            subprocess.run([sys.executable, api_path], cwd=os.path.dirname(__file__))
            
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()