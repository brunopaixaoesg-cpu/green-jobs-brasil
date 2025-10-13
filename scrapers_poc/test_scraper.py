"""
Script de teste para o POC de Scraper de Vagas ESG

Executa scraping no Vagas.com e salva resultados
"""
import sys
from vagas_com_scraper import VagasComScraper
import config

def main():
    """Executa teste do scraper"""
    
    print("="*70)
    print("🤖 POC - SCRAPER DE VAGAS ESG")
    print("="*70)
    print(f"\n📍 Fonte: Vagas.com")
    print(f"🔑 Keywords: {len(config.ESG_KEYWORDS)}")
    print(f"🎯 Meta: {config.MAX_VAGAS_PER_RUN} vagas\n")
    
    # Confirmar execução
    resposta = input("Deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("❌ Operação cancelada")
        return
    
    print("\n" + "="*70)
    
    # Inicializar scraper
    scraper = VagasComScraper()
    
    # Executar scraping
    try:
        vagas = scraper.extrair_todas_vagas(max_vagas=config.MAX_VAGAS_PER_RUN)
        
        # Mostrar resumo
        scraper.imprimir_resumo()
        
        # Salvar resultados
        if vagas:
            arquivo = scraper.salvar_resultados()
            print(f"\n✅ Scraping concluído com sucesso!")
            print(f"📁 Arquivo salvo: {arquivo}")
            print(f"📊 Total de vagas: {len(vagas)}\n")
            
            # Perguntar se quer ver detalhes de algumas vagas
            ver_detalhes = input("\nDeseja buscar detalhes completos das 5 primeiras vagas? (s/n): ").strip().lower()
            if ver_detalhes == 's':
                links = [v.get('link_candidatura') for v in vagas[:5] if v.get('link_candidatura')]
                if links:
                    vagas_detalhadas = scraper.buscar_vagas_detalhadas(links)
                    
                    print("\n" + "="*70)
                    print("📋 DETALHES DAS VAGAS")
                    print("="*70 + "\n")
                    
                    for i, vaga in enumerate(vagas_detalhadas, 1):
                        print(f"\n{i}. {vaga.get('titulo', 'Sem título')}")
                        print(f"   {'─'*60}")
                        print(f"   🏢 Empresa: {vaga.get('empresa', 'N/A')}")
                        print(f"   📍 Local: {vaga.get('localizacao', 'N/A')}")
                        print(f"   💼 Tipo: {vaga.get('tipo', 'N/A')}")
                        print(f"   🏠 Remoto: {'Sim' if vaga.get('remoto') else 'Não'}")
                        if vaga.get('salario'):
                            print(f"   💰 Salário: {vaga['salario']}")
                        print(f"   🔗 Link: {vaga.get('link_candidatura', 'N/A')}")
                        
                        if vaga.get('descricao'):
                            desc = vaga['descricao'][:200] + "..." if len(vaga.get('descricao', '')) > 200 else vaga.get('descricao', '')
                            print(f"\n   📝 Descrição:\n   {desc}\n")
        else:
            print("\n⚠️ Nenhuma vaga encontrada. Possíveis razões:")
            print("   - Site mudou estrutura HTML")
            print("   - Keywords não retornaram resultados")
            print("   - Bloqueio anti-scraping")
            print("   - Problema de conexão\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸️ Scraping interrompido pelo usuário")
        print(f"📊 Vagas coletadas até agora: {len(scraper.vagas)}")
        
        if scraper.vagas:
            salvar = input("\nDeseja salvar os resultados parciais? (s/n): ").strip().lower()
            if salvar == 's':
                arquivo = scraper.salvar_resultados()
                print(f"💾 Resultados parciais salvos em: {arquivo}\n")
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "="*70)
        print("🏁 Teste finalizado")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
