"""
Alternativa para testar responsividade mobile SEM configurar firewall
Usa túnel SSH reverso ou simplesmente abre no navegador para DevTools mobile
"""
import webbrowser
import time

def main():
    print("\n" + "="*70)
    print("🌿 GREEN JOBS BRASIL - TESTE MOBILE (SEM FIREWALL)")
    print("="*70)
    
    print("\n📱 OPÇÕES DE TESTE:")
    print("\n1️⃣  OPÇÃO 1: Chrome DevTools Mobile Emulation (RECOMENDADO)")
    print("   ✅ Não precisa configurar firewall")
    print("   ✅ Testa todos os dispositivos móveis")
    print("   ✅ Funciona agora mesmo!")
    
    print("\n2️⃣  OPÇÃO 2: Celular Real (Precisa liberar firewall)")
    print("   ⚠️  Precisa executar como Administrador")
    print("   ⚠️  Mais complexo")
    
    print("\n" + "="*70)
    
    opcao = input("\nEscolha uma opção (1 ou 2): ").strip()
    
    if opcao == "1":
        print("\n🚀 Abrindo Chrome com DevTools...")
        print("\n📋 INSTRUÇÕES:")
        print("   1. Chrome vai abrir")
        print("   2. Pressione F12 para abrir DevTools")
        print("   3. Clique no ícone de celular (ou Ctrl+Shift+M)")
        print("   4. Escolha o dispositivo: iPhone SE, Pixel 5, iPad, etc.")
        print("   5. Teste a responsividade!")
        
        urls = [
            "http://127.0.0.1:8002/api/profissionais/dashboard/1",
            "http://127.0.0.1:8002/api/profissionais/perfil/1",
            "http://127.0.0.1:8002/api/profissionais/editar/1"
        ]
        
        print("\n🌐 URLs que serão abertas:")
        for url in urls:
            print(f"   • {url}")
        
        input("\nPressione ENTER para abrir o navegador...")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Abrindo: {url}")
            webbrowser.open(url)
            time.sleep(1)
        
        print("\n✅ SUCESSO! Navegador aberto.")
        print("\n💡 DICA: Dispositivos para testar no DevTools:")
        print("   • iPhone SE (375x667) - Mobile pequeno")
        print("   • iPhone 12/13 (390x844) - Mobile médio")
        print("   • Pixel 5 (393x851) - Android")
        print("   • iPad Mini (768x1024) - Tablet")
        print("   • iPad Pro (1024x1366) - Tablet grande")
        
    elif opcao == "2":
        print("\n📱 Para testar no celular real:")
        print("\n1. Execute o arquivo 'liberar_firewall.bat' como Administrador:")
        print("   • Clique com botão direito no arquivo")
        print("   • Selecione 'Executar como administrador'")
        print("\n2. Depois execute: py start_mobile.py")
        print("\n3. No celular, acesse:")
        print("   http://192.168.100.6:8002/api/profissionais/dashboard/1")
    
    else:
        print("\n❌ Opção inválida. Execute novamente.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
