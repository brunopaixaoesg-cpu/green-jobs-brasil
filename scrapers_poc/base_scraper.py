"""
Classe base abstrata para scrapers de vagas ESG
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import json
import os
import config

class BaseScraper(ABC):
    """
    Classe base para todos os scrapers de vagas
    """
    
    def __init__(self, keywords: List[str] = None):
        """
        Inicializa o scraper
        
        Args:
            keywords: Lista de palavras-chave ESG para buscar
        """
        self.keywords = keywords or config.ESG_KEYWORDS
        self.vagas = []
        self.fonte = self.get_fonte_nome()
    
    @abstractmethod
    def get_fonte_nome(self) -> str:
        """Retorna o nome da fonte (ex: 'vagas.com')"""
        pass
    
    @abstractmethod
    def buscar_vagas(self, keyword: str, limite: int = 10) -> List[Dict]:
        """
        Busca vagas por palavra-chave
        
        Args:
            keyword: Palavra-chave de busca
            limite: Número máximo de vagas
            
        Returns:
            Lista de dicionários com dados das vagas
        """
        pass
    
    def extrair_todas_vagas(self, max_vagas: int = None) -> List[Dict]:
        """
        Executa busca para todas as keywords configuradas
        
        Args:
            max_vagas: Número máximo total de vagas
            
        Returns:
            Lista de vagas encontradas
        """
        max_vagas = max_vagas or config.MAX_VAGAS_PER_RUN
        todas_vagas = []
        vagas_por_keyword = max_vagas // len(self.keywords)
        
        print(f"\n🔍 Iniciando scraping em {self.fonte}")
        print(f"📋 Keywords: {len(self.keywords)}")
        print(f"🎯 Meta: {max_vagas} vagas\n")
        
        for keyword in self.keywords:
            print(f"  🔎 Buscando: '{keyword}'...")
            try:
                vagas = self.buscar_vagas(keyword, limite=vagas_por_keyword)
                
                # Adicionar metadata
                for vaga in vagas:
                    vaga['keywords_encontradas'] = [keyword]
                    vaga['data_scraping'] = datetime.now().isoformat()
                    vaga['fonte'] = self.fonte
                
                todas_vagas.extend(vagas)
                print(f"    ✅ Encontradas: {len(vagas)} vagas")
                
                if len(todas_vagas) >= max_vagas:
                    print(f"\n✅ Meta atingida! {len(todas_vagas)} vagas coletadas")
                    break
                    
            except Exception as e:
                print(f"    ❌ Erro: {str(e)}")
                continue
        
        # Remover duplicatas por link
        vagas_unicas = self._remover_duplicatas(todas_vagas)
        
        print(f"\n📊 Resultado final:")
        print(f"   Total bruto: {len(todas_vagas)}")
        print(f"   Duplicatas removidas: {len(todas_vagas) - len(vagas_unicas)}")
        print(f"   Total único: {len(vagas_unicas)}\n")
        
        self.vagas = vagas_unicas
        return vagas_unicas
    
    def _remover_duplicatas(self, vagas: List[Dict]) -> List[Dict]:
        """Remove vagas duplicadas baseado no link"""
        seen = set()
        unicas = []
        
        for vaga in vagas:
            link = vaga.get('link_candidatura', '')
            if link and link not in seen:
                seen.add(link)
                unicas.append(vaga)
        
        return unicas
    
    def salvar_resultados(self, filename: Optional[str] = None) -> str:
        """
        Salva resultados em JSON
        
        Args:
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"vagas_{self.fonte}_{timestamp}.json"
        
        filepath = os.path.join(config.RESULTS_DIR, filename)
        
        data = {
            'fonte': self.fonte,
            'data_scraping': datetime.now().isoformat(),
            'total_vagas': len(self.vagas),
            'keywords': self.keywords,
            'vagas': self.vagas
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Resultados salvos em: {filepath}")
        return filepath
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas das vagas coletadas"""
        if not self.vagas:
            return {}
        
        stats = {
            'total': len(self.vagas),
            'com_salario': sum(1 for v in self.vagas if v.get('salario')),
            'remotas': sum(1 for v in self.vagas if v.get('remoto')),
            'por_estado': {},
            'por_tipo': {}
        }
        
        for vaga in self.vagas:
            # Contar por estado
            loc = vaga.get('localizacao', '')
            if ' - ' in loc:
                estado = loc.split(' - ')[-1]
                stats['por_estado'][estado] = stats['por_estado'].get(estado, 0) + 1
            
            # Contar por tipo
            tipo = vaga.get('tipo', 'Não especificado')
            stats['por_tipo'][tipo] = stats['por_tipo'].get(tipo, 0) + 1
        
        return stats
    
    def imprimir_resumo(self):
        """Imprime resumo formatado das vagas"""
        if not self.vagas:
            print("❌ Nenhuma vaga coletada")
            return
        
        stats = self.get_estatisticas()
        
        print("\n" + "="*60)
        print(f"📊 RESUMO DO SCRAPING - {self.fonte.upper()}")
        print("="*60)
        print(f"✅ Total de vagas: {stats['total']}")
        print(f"💰 Com informação salarial: {stats['com_salario']}")
        print(f"🏠 Vagas remotas: {stats['remotas']}")
        
        print("\n📍 Por Estado:")
        for estado, count in sorted(stats['por_estado'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {estado}: {count}")
        
        print("\n📋 Por Tipo:")
        for tipo, count in sorted(stats['por_tipo'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {tipo}: {count}")
        
        print("\n💼 Primeiras 3 vagas:")
        for i, vaga in enumerate(self.vagas[:3], 1):
            print(f"\n   {i}. {vaga.get('titulo', 'Sem título')}")
            print(f"      Empresa: {vaga.get('empresa', 'N/A')}")
            print(f"      Local: {vaga.get('localizacao', 'N/A')}")
            print(f"      Link: {vaga.get('link_candidatura', 'N/A')[:60]}...")
        
        print("\n" + "="*60 + "\n")
