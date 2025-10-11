"""
Green Jobs Brasil - Launcher Simples
Versão sem interface gráfica que funciona sempre
"""
import subprocess
import webbrowser
import time
import os
import sys
from datetime import datetime

class SimpleGreenJobsLauncher:
    def __init__(self):
        self.api_process = None
        
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        """Mostra cabeçalho"""
        self.clear_screen()
        print("=" * 60)
        print("🌱 GREEN JOBS BRASIL - LAUNCHER SIMPLES 🌱")
        print("=" * 60)
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        print()
        
    def print_menu(self):
        """Mostra menu de opções"""
        print("📋 OPÇÕES DISPONÍVEIS:")
        print("1️⃣  - Iniciar API")
        print("2️⃣  - Abrir Documentação")
        print("3️⃣  - Ver Empresas")
        print("4️⃣  - Ver Estatísticas")
        print("5️⃣  - Parar API")
        print("0️⃣  - Sair")
        print()
        
    def start_api(self):
        """Inicia a API"""
        try:
            print("🚀 Iniciando API...")
            
            # Caminho para o script da API
            api_script = os.path.join(os.path.dirname(__file__), 'api', 'sqlite_api.py')
            if not os.path.exists(api_script):
                print(f"❌ Arquivo não encontrado: {api_script}")
                return False
                
            # Iniciar processo da API
            self.api_process = subprocess.Popen(
                [sys.executable, api_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Aguardar um pouco para API iniciar
            time.sleep(3)
            
            # Verificar se ainda está rodando
            if self.api_process.poll() is None:
                print("✅ API iniciada com sucesso!")
                print("📍 URL: http://127.0.0.1:8000")
                print("📚 Docs: http://127.0.0.1:8000/docs")
                return True
            else:
                print("❌ API falhou ao iniciar")
                stdout, stderr = self.api_process.communicate()
                if stderr:
                    print(f"Erro: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar API: {str(e)}")
            return False
            
    def stop_api(self):
        """Para a API"""
        try:
            if self.api_process and self.api_process.poll() is None:
                print("🛑 Parando API...")
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
                print("✅ API parada com sucesso!")
                return True
            else:
                print("⚠️ API não está rodando")
                return False
        except Exception as e:
            print(f"❌ Erro ao parar API: {str(e)}")
            return False
            
    def is_api_running(self):
        """Verifica se API está rodando"""
        return self.api_process and self.api_process.poll() is None
        
    def open_url(self, url, description):
        """Abre URL no navegador"""
        if self.is_api_running():
            print(f"🌐 Abrindo: {description}")
            print(f"📍 URL: {url}")
            webbrowser.open(url)
            time.sleep(2)
        else:
            print("⚠️ Inicie a API primeiro!")
            
    def run(self):
        """Loop principal"""
        while True:
            self.print_header()
            
            # Status da API
            if self.is_api_running():
                print("🟢 STATUS: API RODANDO")
            else:
                print("🔴 STATUS: API PARADA")
            print()
            
            self.print_menu()
            
            try:
                choice = input("👉 Escolha uma opção: ").strip()
                
                if choice == "1":
                    if not self.is_api_running():
                        self.start_api()
                    else:
                        print("⚠️ API já está rodando!")
                        
                elif choice == "2":
                    self.open_url("http://127.0.0.1:8000/docs", "Documentação Interativa")
                    
                elif choice == "3":
                    self.open_url("http://127.0.0.1:8000/empresas", "Lista de Empresas")
                    
                elif choice == "4":
                    self.open_url("http://127.0.0.1:8000/stats", "Estatísticas do Sistema")
                    
                elif choice == "5":
                    self.stop_api()
                    
                elif choice == "0":
                    if self.is_api_running():
                        print("🛑 Parando API antes de sair...")
                        self.stop_api()
                    print("👋 Até logo!")
                    break
                    
                else:
                    print("❌ Opção inválida!")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrompido pelo usuário")
                if self.is_api_running():
                    self.stop_api()
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                
            if choice != "0":
                input("\nPressione Enter para continuar...")

def main():
    launcher = SimpleGreenJobsLauncher()
    launcher.run()

if __name__ == "__main__":
    main()