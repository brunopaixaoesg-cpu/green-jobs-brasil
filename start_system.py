"""
SISTEMA GREEN JOBS BRASIL - VERSÃO ULTRA SIMPLES
Execução direta sem complicações
"""
import os
import sys
import subprocess
import time

def main():
    print("🌱 GREEN JOBS BRASIL - SISTEMA ULTRA SIMPLES")
    print("=" * 60)
    
    # Diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_file = os.path.join(current_dir, "api", "app_definitivo.py")
    
    print(f"📂 Pasta: {current_dir}")
    print(f"🎯 API: {api_file}")
    
    if not os.path.exists(api_file):
        print("❌ ERRO: Arquivo da API não encontrado!")
        input("Pressione Enter para sair...")
        return
    
    print("\n🚀 Iniciando sistema...")
    print("📍 URL: http://127.0.0.1:8000")
    print("🔴 Para parar: Pressione Ctrl+C")
    print("=" * 60)
    
    try:
        # Executa diretamente
        os.chdir(current_dir)
        subprocess.run([sys.executable, api_file], check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema parado pelo usuário")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Tente executar diretamente:")
        print(f"py \"{api_file}\"")
        
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()