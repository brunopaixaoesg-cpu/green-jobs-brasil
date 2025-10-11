"""
Green Jobs Brasil - Launcher Executável Otimizado
Versão especial para arquivo .exe que sempre funciona
"""
import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def get_base_path():
    """Detectar o diretório base correto"""
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller - usar diretório do .exe
        return Path(sys.executable).parent
    else:
        # Script Python - usar diretório do arquivo
        return Path(__file__).parent

def find_python():
    """Encontrar executável Python"""
    # Tentar várias opções
    python_options = [
        sys.executable,  # Python atual
        "python",
        "python3",
        "C:/Users/Bruno/AppData/Local/Programs/Python/Python313/python.exe",
        "C:/Python313/python.exe",
        "C:/Python/python.exe"
    ]
    
    for python_path in python_options:
        try:
            result = subprocess.run([python_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return python_path
        except:
            continue
    
    return None

def main():
    """Função principal otimizada para executável"""
    print("=" * 65)
    print("🌱 GREEN JOBS BRASIL - LAUNCHER EXECUTÁVEL 🌱")
    print("=" * 65)
    
    # Detectar diretório base
    base_path = get_base_path()
    print(f"📁 Base: {base_path}")
    
    # Verificar arquivos essenciais
    db_path = base_path / "gjb_dev.db"
    api_path = base_path / "api" / "sqlite_api.py"
    
    print("\n🔍 Verificando arquivos...")
    
    if not db_path.exists():
        print(f"❌ Banco de dados não encontrado: {db_path}")
        print("💡 Certifique-se de que o .exe está na pasta do projeto!")
        input("Pressione Enter para sair...")
        return
    print("✅ Banco de dados encontrado!")
    
    if not api_path.exists():
        print(f"❌ Script da API não encontrado: {api_path}")
        print("💡 Certifique-se de que a pasta 'api' está no mesmo local!")
        input("Pressione Enter para sair...")
        return
    print("✅ Script da API encontrado!")
    
    # Encontrar Python
    print("\n🐍 Procurando Python...")
    python_exe = find_python()
    
    if not python_exe:
        print("❌ Python não encontrado!")
        print("💡 Instale Python ou coloque no PATH do sistema")
        input("Pressione Enter para sair...")
        return
    print(f"✅ Python encontrado: {python_exe}")
    
    # Iniciar API
    print("\n🚀 Iniciando API...")
    print("⏳ Aguarde alguns segundos...")
    
    try:
        # Configurar ambiente
        env = os.environ.copy()
        env['PYTHONPATH'] = str(base_path)
        
        # Iniciar processo da API
        process = subprocess.Popen(
            [python_exe, str(api_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(base_path),
            env=env
        )
        
        # Aguardar API inicializar
        print("⏳ Aguardando API inicializar...")
        time.sleep(5)
        
        # Verificar se processo ainda está rodando
        if process.poll() is None:
            print("✅ API iniciada com sucesso!")
            
            # Mostrar informações
            print("\n" + "=" * 60)
            print("🎉 SISTEMA PRONTO PARA USO!")
            print("=" * 60)
            print("📍 API Principal: http://127.0.0.1:8000")
            print("📚 Documentação: http://127.0.0.1:8000/docs")
            print("🏢 Empresas: http://127.0.0.1:8000/empresas")
            print("📊 Estatísticas: http://127.0.0.1:8000/stats")
            print("❤️  Saúde da API: http://127.0.0.1:8000/health")
            print("=" * 60)
            
            # Abrir navegador
            def open_browser():
                time.sleep(2)
                try:
                    print("\n🌐 Abrindo documentação no navegador...")
                    webbrowser.open("http://127.0.0.1:8000/docs")
                    print("✅ Navegador aberto!")
                except Exception as e:
                    print(f"⚠️  Erro ao abrir navegador: {e}")
                    print("💡 Acesse manualmente: http://127.0.0.1:8000/docs")
            
            # Abrir navegador em background
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Aguardar usuário
            print("\n" + "🔥" * 25)
            print("💡 SISTEMA RODANDO!")
            print("⚠️  NÃO FECHE esta janela!")
            print("🛑 Para parar: Feche esta janela ou pressione Ctrl+C")
            print("🔥" * 25)
            
            try:
                # Aguardar processo terminar ou Ctrl+C
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Parando sistema...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print("✅ API parada com sucesso!")
                except:
                    process.kill()
                    print("🔨 API forçada a parar!")
        else:
            print("❌ API falhou ao iniciar")
            # Mostrar erro
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erro: {stderr.decode()}")
            input("Pressione Enter para sair...")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()