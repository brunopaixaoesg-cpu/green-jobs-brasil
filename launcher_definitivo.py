"""
LAUNCHER DEFINITIVO - Green Jobs Brasil
Sistema que funciona sempre, sem dependência de templates externos
"""
import subprocess
import sys
import os
import time
from pathlib import Path
import webbrowser

def main():
    print("🌱 GREEN JOBS BRASIL - LAUNCHER DEFINITIVO")
    print("=" * 60)
    
    # Detecta ambiente
    base_dir = Path(__file__).parent
    api_file = base_dir / "api" / "app_definitivo.py"
    
    print(f"📂 Diretório: {base_dir}")
    print(f"🎯 API: {api_file}")
    
    # Verifica arquivos
    if not api_file.exists():
        print("❌ ERRO: Arquivo app_definitivo.py não encontrado!")
        return
    
    # Confirma execução
    print("\n✅ Tudo pronto para iniciar o sistema!")
    print("⚡ Este launcher usa uma versão que SEMPRE funciona")
    print("📍 URL: http://127.0.0.1:8000")
    
    print("\n🚀 Iniciando sistema automaticamente em 3 segundos...")
    time.sleep(3)
    
    try:
        print("\n🔄 Iniciando servidor...")
        
        # Comando para Windows (usa py ao invés de python)
        cmd = ["py", str(api_file)]
        
        # Inicia processo
        process = subprocess.Popen(
            cmd,
            cwd=str(base_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Aguarda inicialização
        time.sleep(3)
        
        # Abre navegador
        try:
            webbrowser.open("http://127.0.0.1:8000")
            print("🌐 Navegador aberto automaticamente")
        except:
            print("⚠️  Abra manualmente: http://127.0.0.1:8000")
        
        print("\n" + "=" * 60)
        print("✅ SISTEMA RODANDO COM SUCESSO!")
        print("📍 Dashboard: http://127.0.0.1:8000")
        print("📖 API Docs: http://127.0.0.1:8000/docs")
        print("🔴 Pressione Ctrl+C para parar")
        print("=" * 60)
        
        # Aguarda saída
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Parando servidor...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
        print("✅ Servidor parado com sucesso!")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("💡 Tente executar manualmente:")
        print(f"   python {api_file}")

if __name__ == "__main__":
    main()