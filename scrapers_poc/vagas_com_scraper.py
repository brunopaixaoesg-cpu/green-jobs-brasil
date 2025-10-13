"""
Scraper para Vagas.com
Busca vagas ESG/Sustentabilidade
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import re
from base_scraper import BaseScraper
import config

class VagasComScraper(BaseScraper):
    """
    Scraper específico para Vagas.com
    """
    
    BASE_URL = "https://www.vagas.com.br"
    SEARCH_URL = f"{BASE_URL}/vagas-de-{{keyword}}"
    
    def get_fonte_nome(self) -> str:
        return "vagas.com"
    
    def buscar_vagas(self, keyword: str, limite: int = 10) -> List[Dict]:
        """
        Busca vagas por palavra-chave no Vagas.com
        
        Args:
            keyword: Palavra-chave de busca
            limite: Número máximo de vagas
            
        Returns:
            Lista de vagas encontradas
        """
        vagas = []
        
        try:
            # Formatar keyword para URL (remover espaços, acentos)
            keyword_url = self._formatar_keyword_url(keyword)
            url = self.SEARCH_URL.format(keyword=keyword_url)
            
            # Fazer requisição
            response = requests.get(
                url,
                headers=config.HEADERS,
                timeout=config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"      ⚠️ Status {response.status_code} para '{keyword}'")
                return []
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontrar elementos de vaga
            vaga_elements = soup.find_all('li', class_='vaga')
            
            if not vaga_elements:
                # Tentar outro seletor (HTML pode variar)
                vaga_elements = soup.find_all('article', class_='job-card')
            
            # Processar cada vaga
            for elem in vaga_elements[:limite]:
                try:
                    vaga_data = self._extrair_dados_vaga(elem)
                    if vaga_data:
                        vagas.append(vaga_data)
                except Exception as e:
                    print(f"        ⚠️ Erro ao processar vaga: {str(e)}")
                    continue
            
            # Rate limiting
            time.sleep(config.REQUEST_DELAY)
            
        except requests.exceptions.Timeout:
            print(f"      ⏰ Timeout na busca por '{keyword}'")
        except requests.exceptions.RequestException as e:
            print(f"      ❌ Erro de conexão: {str(e)}")
        except Exception as e:
            print(f"      ❌ Erro inesperado: {str(e)}")
        
        return vagas
    
    def _formatar_keyword_url(self, keyword: str) -> str:
        """Formata keyword para URL do Vagas.com"""
        # Remover acentos
        keyword = keyword.lower()
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'â': 'a', 'ê': 'e', 'ô': 'o',
            'ã': 'a', 'õ': 'o',
            'ç': 'c'
        }
        for old, new in replacements.items():
            keyword = keyword.replace(old, new)
        
        # Substituir espaços por hífens
        keyword = re.sub(r'\s+', '-', keyword)
        
        # Remover caracteres especiais
        keyword = re.sub(r'[^a-z0-9\-]', '', keyword)
        
        return keyword
    
    def _extrair_dados_vaga(self, elem) -> Dict:
        """
        Extrai dados de uma vaga do HTML
        
        Args:
            elem: Elemento BeautifulSoup da vaga
            
        Returns:
            Dicionário com dados da vaga
        """
        vaga = {}
        
        # Título
        titulo_elem = elem.find('h2', class_='job-title') or elem.find('a', class_='link-detalhes-vaga')
        if titulo_elem:
            vaga['titulo'] = titulo_elem.get_text(strip=True)
        else:
            return None  # Vaga inválida sem título
        
        # Link
        link_elem = elem.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            if href.startswith('/'):
                href = self.BASE_URL + href
            vaga['link_candidatura'] = href
        
        # Empresa
        empresa_elem = elem.find('span', class_='emprVaga') or elem.find('div', class_='company-name')
        if empresa_elem:
            vaga['empresa'] = empresa_elem.get_text(strip=True)
        
        # Localização
        loc_elem = elem.find('span', class_='localizacaoVaga') or elem.find('div', class_='job-location')
        if loc_elem:
            vaga['localizacao'] = loc_elem.get_text(strip=True)
        
        # Tipo de contratação
        tipo_elem = elem.find('span', class_='nivelVaga')
        if tipo_elem:
            vaga['tipo'] = tipo_elem.get_text(strip=True)
        else:
            vaga['tipo'] = 'Não especificado'
        
        # Salário (se disponível)
        salario_elem = elem.find('span', class_='salarioVaga')
        if salario_elem:
            vaga['salario'] = salario_elem.get_text(strip=True)
        
        # Descrição resumida
        desc_elem = elem.find('p', class_='job-description') or elem.find('div', class_='descricao')
        if desc_elem:
            vaga['descricao'] = desc_elem.get_text(strip=True)[:500]  # Máx 500 chars
        
        # Detectar se é remoto
        texto_completo = elem.get_text().lower()
        vaga['remoto'] = any(termo in texto_completo for termo in ['remoto', 'home office', 'anywhere'])
        
        # Requisitos (tentar extrair)
        req_elem = elem.find('div', class_='requisitos')
        if req_elem:
            vaga['requisitos'] = req_elem.get_text(strip=True)[:500]
        
        return vaga
    
    def buscar_vagas_detalhadas(self, links: List[str]) -> List[Dict]:
        """
        Busca detalhes completos de vagas (página individual)
        
        Args:
            links: Lista de URLs de vagas
            
        Returns:
            Lista de vagas com dados completos
        """
        vagas_detalhadas = []
        
        print(f"\n🔎 Buscando detalhes de {len(links)} vagas...")
        
        for i, link in enumerate(links, 1):
            try:
                print(f"   {i}/{len(links)}...", end=' ')
                
                response = requests.get(
                    link,
                    headers=config.HEADERS,
                    timeout=config.REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    vaga = self._extrair_vaga_completa(soup, link)
                    vagas_detalhadas.append(vaga)
                    print("✅")
                else:
                    print(f"❌ (Status {response.status_code})")
                
                time.sleep(config.REQUEST_DELAY)
                
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                continue
        
        return vagas_detalhadas
    
    def _extrair_vaga_completa(self, soup: BeautifulSoup, link: str) -> Dict:
        """Extrai todos os dados de uma página de vaga"""
        vaga = {'link_candidatura': link}
        
        # Título
        titulo = soup.find('h1', class_='job-shortdescription__title')
        if titulo:
            vaga['titulo'] = titulo.get_text(strip=True)
        
        # Empresa
        empresa = soup.find('div', class_='job-shortdescription__company')
        if empresa:
            vaga['empresa'] = empresa.get_text(strip=True)
        
        # Localização
        local = soup.find('span', class_='job-location__city')
        if local:
            vaga['localizacao'] = local.get_text(strip=True)
        
        # Descrição completa
        desc = soup.find('div', class_='job-description__text')
        if desc:
            vaga['descricao'] = desc.get_text(strip=True)
        
        # Requisitos
        req = soup.find('div', class_='job-requirements')
        if req:
            vaga['requisitos'] = req.get_text(strip=True)
        
        # Benefícios
        benef = soup.find('div', class_='job-benefits')
        if benef:
            vaga['beneficios'] = benef.get_text(strip=True)
        
        # Salário
        sal = soup.find('span', class_='job-hierarchylist__item--salary')
        if sal:
            vaga['salario'] = sal.get_text(strip=True)
        
        # Tipo
        tipo = soup.find('span', class_='job-hierarchylist__item--type')
        if tipo:
            vaga['tipo'] = tipo.get_text(strip=True)
        
        # Remoto
        texto_completo = soup.get_text().lower()
        vaga['remoto'] = any(termo in texto_completo for termo in ['remoto', 'home office', 'anywhere'])
        
        return vaga
