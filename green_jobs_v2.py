"""
Green Jobs Brasil - Launcher Atualizado
Versão 2.0 com API melhorada
"""
import subprocess
import time
import webbrowser
import os
import sys

def main():
    print("Green Jobs Brasil - Sistema de Empresas Verdes")
    print("=" * 60)
    print("Versao 2.0 - Completamente Funcional")
    print("- Busca empresas na Receita Federal")
    print("- Classifica automaticamente como verde")
    print("- Dashboard moderno e responsivo")
    
    # Pergunta se quer abrir o navegador
    resposta = input("\nAbrir dashboard no navegador? (s/n) [s]: ").lower().strip()
    if resposta == '' or resposta == 's':
        print("Iniciando servidor...")
        
        # Determina o diretório base
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        
        # Caminho para a API final
        api_path = os.path.join(base_dir, "api", "final_api.py")
        
        try:
            # Inicia o servidor
            process = subprocess.Popen([
                sys.executable, api_path
            ], cwd=base_dir)
            
            # Aguarda servidor inicializar
            print("Aguardando servidor inicializar...")
            time.sleep(4)
            
            # Abre navegador
            print("Abrindo dashboard...")
            webbrowser.open("http://127.0.0.1:8000")
            
            print("\nSistema iniciado com sucesso!")
            print("Dashboard: http://127.0.0.1:8000")
            print("\nComo usar:")
            print("1. Digite qualquer CNPJ brasileiro no dashboard")
            print("2. Clique 'Verificar e Adicionar'")
            print("3. Sistema busca automaticamente na Receita Federal")
            print("4. Se for empresa verde, adiciona ao banco")
            print("5. Dashboard atualiza automaticamente")
            print("\nPara parar: Feche esta janela")
            
            # Mantém processo rodando
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\nEncerrando sistema...")
                process.terminate()
                
        except Exception as e:
            print(f"Erro ao iniciar: {e}")
            input("Pressione Enter para sair...")
    else:
        print("Sistema nao iniciado.")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()