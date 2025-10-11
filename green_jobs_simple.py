"""
Green Jobs Brasil - Launcher Executavel (Sem Emojis)
Versao compativel com console Windows
"""
import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def get_base_path():
    """Detectar o diretorio base correto"""
    if getattr(sys, 'frozen', False):
        # Executavel PyInstaller - usar diretorio do .exe
        return Path(sys.executable).parent
    else:
        # Script Python - usar diretorio do arquivo
        return Path(__file__).parent

def find_python():
    """Encontrar executavel Python"""
    python_options = [
        sys.executable,
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
    """Funcao principal otimizada para executavel"""
    print("=" * 65)
    print("GREEN JOBS BRASIL - LAUNCHER EXECUTAVEL")
    print("=" * 65)
    
    # Detectar diretorio base
    base_path = get_base_path()
    print(f"Base: {base_path}")
    
    # Verificar arquivos essenciais
    db_path = base_path / "gjb_dev.db"
    api_path = base_path / "api" / "sqlite_api.py"
    
    print("\nVerificando arquivos...")
    
    if not db_path.exists():
        print(f"ERRO: Banco de dados nao encontrado: {db_path}")
        print("DICA: Certifique-se de que o .exe esta na pasta do projeto!")
        input("Pressione Enter para sair...")
        return
    print("OK: Banco de dados encontrado!")
    
    if not api_path.exists():
        print(f"ERRO: Script da API nao encontrado: {api_path}")
        print("DICA: Certifique-se de que a pasta 'api' esta no mesmo local!")
        input("Pressione Enter para sair...")
        return
    print("OK: Script da API encontrado!")
    
    # Encontrar Python
    print("\nProcurando Python...")
    python_exe = find_python()
    
    if not python_exe:
        print("ERRO: Python nao encontrado!")
        print("DICA: Instale Python ou coloque no PATH do sistema")
        input("Pressione Enter para sair...")
        return
    print(f"OK: Python encontrado: {python_exe}")
    
    # Iniciar API
    print("\nIniciando API...")
    print("Aguarde alguns segundos...")
    
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
        print("Aguardando API inicializar...")
        time.sleep(5)
        
        # Verificar se processo ainda esta rodando
        if process.poll() is None:
            print("OK: API iniciada com sucesso!")
            
            # Mostrar informacoes
            print("\n" + "=" * 60)
            print("SISTEMA PRONTO PARA USO!")
            print("=" * 60)
            print("Dashboard Principal: http://127.0.0.1:8000")
            print("API: http://127.0.0.1:8000/api")
            print("Documentacao: http://127.0.0.1:8000/docs")
            print("Empresas: http://127.0.0.1:8000/api/empresas")
            print("Estatisticas: http://127.0.0.1:8000/api/stats")
            print("Health Check: http://127.0.0.1:8000/api/health")
            print("=" * 60)
            
            # Perguntar se quer abrir navegador
            try:
                choice = input("\nAbrir dashboard no navegador? (s/n): ").lower().strip()
                if choice in ['s', 'sim', 'y', 'yes', '']:
                    try:
                        print("Abrindo dashboard no navegador...")
                        webbrowser.open("http://127.0.0.1:8000", new=2)
                        time.sleep(1)  # Pequena pausa
                        print("OK: Navegador aberto!")
                    except Exception as e:
                        print(f"AVISO: Erro ao abrir navegador: {e}")
                        print("DICA: Acesse manualmente: http://127.0.0.1:8000")
                else:
                    print("OK: Navegador nao sera aberto.")
                    print("DICA: Acesse manualmente: http://127.0.0.1:8000")
            except:
                print("DICA: Acesse manualmente: http://127.0.0.1:8000")
            
            # Aguardar usuario
            print("\n" + "*" * 25)
            print("SISTEMA RODANDO!")
            print("NAO FECHE esta janela!")
            print("Para parar: Feche esta janela ou pressione Ctrl+C")
            print("*" * 25)
            
            try:
                # Aguardar processo terminar ou Ctrl+C
                process.wait()
            except KeyboardInterrupt:
                print("\nParando sistema...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print("OK: API parada com sucesso!")
                except:
                    process.kill()
                    print("FORCADO: API parada!")
        else:
            print("ERRO: API falhou ao iniciar")
            # Mostrar erro
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erro detalhado: {stderr.decode()}")
            input("Pressione Enter para sair...")
            
    except Exception as e:
        print(f"ERRO GERAL: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()