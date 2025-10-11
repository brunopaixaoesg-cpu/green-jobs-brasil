"""
Green Jobs Brasil - Launcher Executável
Script otimizado para ser compilado em .exe
"""
import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

class GreenJobsLauncher:
    def __init__(self):
        # Para executáveis PyInstaller, usar o diretório onde o .exe está
        if getattr(sys, 'frozen', False):
            # Executável PyInstaller
            self.base_path = Path(sys.executable).parent.absolute()
        else:
            # Script Python normal
            self.base_path = Path(__file__).parent.absolute()
            
        self.api_path = self.base_path / "api" / "sqlite_api.py"
        self.db_path = self.base_path / "gjb_dev.db"
        self.process = None
        
    def show_banner(self):
        print("=" * 60)
        print("🌱 GREEN JOBS BRASIL - LAUNCHER EXECUTÁVEL 🌱")
        print("=" * 60)
        print(f"📁 Base: {self.base_path}")
        
    def check_files(self):
        """Verificar se todos os arquivos necessários existem"""
        print("\n🔍 Verificando arquivos...")
        
        if not self.db_path.exists():
            print(f"❌ Banco de dados não encontrado: {self.db_path}")
            return False
        print("✅ Banco de dados encontrado!")
        
        if not self.api_path.exists():
            print(f"❌ Script da API não encontrado: {self.api_path}")
            return False
        print("✅ Script da API encontrado!")
        
        return True
    
    def start_api(self):
        """Iniciar a API em background"""
        try:
            print("\n🚀 Iniciando API...")
            
            # Usar o Python do sistema
            python_exe = sys.executable
            
            # Iniciar processo da API
            self.process = subprocess.Popen(
                [python_exe, str(self.api_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_path)
            )
            
            # Aguardar um pouco para API inicializar
            time.sleep(4)
            
            # Verificar se processo ainda está rodando
            if self.process.poll() is None:
                print("✅ API iniciada com sucesso!")
                return True
            else:
                print("❌ API falhou ao iniciar")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar API: {e}")
            return False
    
    def show_urls(self):
        """Mostrar URLs do sistema"""
        print("\n" + "=" * 55)
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("=" * 55)
        print("📍 API Principal: http://127.0.0.1:8000")
        print("📚 Documentação: http://127.0.0.1:8000/docs")
        print("🏢 Empresas: http://127.0.0.1:8000/empresas")
        print("📊 Estatísticas: http://127.0.0.1:8000/stats")
        print("❤️  Saúde da API: http://127.0.0.1:8000/health")
        print("=" * 55)
    
    def open_browser(self):
        """Abrir navegador"""
        try:
            print("\n🌐 Abrindo documentação no navegador...")
            webbrowser.open("http://127.0.0.1:8000/docs")
            time.sleep(2)
            print("✅ Navegador aberto!")
        except Exception as e:
            print(f"⚠️  Erro ao abrir navegador: {e}")
            print("💡 Acesse manualmente: http://127.0.0.1:8000/docs")
    
    def wait_for_exit(self):
        """Aguardar usuário fechar"""
        print("\n" + "🔥" * 20)
        print("💡 SISTEMA RODANDO!")
        print("⚠️  NÃO FECHE esta janela!")
        print("🛑 Para parar: Feche esta janela ou pressione Ctrl+C")
        print("🔥" * 20)
        
        try:
            # Aguardar processo terminar ou Ctrl+C
            self.process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Parando sistema...")
            self.stop_api()
    
    def stop_api(self):
        """Parar a API"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ API parada com sucesso!")
            except:
                self.process.kill()
                print("🔨 API forçada a parar!")
    
    def run(self):
        """Executar launcher completo"""
        self.show_banner()
        
        if not self.check_files():
            print("\n❌ Falha na verificação de arquivos!")
            input("Pressione Enter para sair...")
            return
        
        if not self.start_api():
            print("\n❌ Falha ao iniciar API!")
            input("Pressione Enter para sair...")
            return
        
        self.show_urls()
        
        # Abrir navegador automaticamente
        threading.Thread(target=self.open_browser, daemon=True).start()
        
        # Aguardar saída
        self.wait_for_exit()

def main():
    """Função principal"""
    launcher = GreenJobsLauncher()
    launcher.run()

if __name__ == "__main__":
    main()