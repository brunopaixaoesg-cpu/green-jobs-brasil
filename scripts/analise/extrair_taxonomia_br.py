#!/usr/bin/env python3
"""
Script para extração estruturada de dados da Taxonomia Sustentável Brasileira

Este script ajuda a processar os cadernos setoriais e extrair:
- Atividades elegíveis
- Critérios técnicos
- Mapeamentos para CNAE
- Dados quantitativos

Uso:
    python extrair_taxonomia_br.py --setor "Energia" --caderno "caminho/para/caderno.pdf"
    python extrair_taxonomia_br.py --analise-interativa
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class TaxonomiaBRExtractor:
    """Extrator de dados da Taxonomia BR"""
    
    def __init__(self, output_dir: str = "data/taxonomia_br"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdiretórios
        self.dirs = {
            'extratos': self.output_dir / 'extratos',
            'mapeamentos': self.output_dir / 'mapeamentos',
            'criterios': self.output_dir / 'criterios',
            'analises': self.output_dir / 'analises'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(exist_ok=True)
    
    def analise_interativa(self, setor: str):
        """
        Modo interativo para análise manual de um setor
        Faz perguntas e estrutura as respostas
        """
        print(f"\n{'='*60}")
        print(f"ANÁLISE INTERATIVA - SETOR: {setor.upper()}")
        print(f"{'='*60}\n")
        
        dados = {
            'setor': setor,
            'data_analise': datetime.now().isoformat(),
            'atividades': [],
            'cnaes_mapeados': [],
            'criterios_tecnicos': {},
            'insights': []
        }
        
        # 1. Informações básicas
        print("📋 INFORMAÇÕES BÁSICAS")
        print("-" * 60)
        dados['caderno_nome'] = input("Nome do caderno: ").strip()
        dados['caderno_versao'] = input("Versão do caderno: ").strip()
        dados['data_publicacao'] = input("Data de publicação (DD/MM/AAAA): ").strip()
        
        # 2. Objetivos ambientais
        print("\n🌍 OBJETIVOS AMBIENTAIS")
        print("-" * 60)
        print("Este setor atende quais objetivos? (s/n para cada)")
        objetivos = [
            "Mitigação das mudanças climáticas",
            "Adaptação às mudanças climáticas",
            "Recursos hídricos",
            "Economia circular",
            "Prevenção e controle da poluição",
            "Biodiversidade e ecossistemas"
        ]
        dados['objetivos_ambientais'] = []
        for obj in objetivos:
            resp = input(f"  {obj}? (s/n): ").strip().lower()
            if resp == 's':
                dados['objetivos_ambientais'].append(obj)
        
        # 3. Atividades elegíveis
        print("\n🏭 ATIVIDADES ELEGÍVEIS")
        print("-" * 60)
        num_atividades = int(input("Quantas atividades elegíveis foram identificadas? "))
        
        for i in range(num_atividades):
            print(f"\n--- Atividade {i+1}/{num_atividades} ---")
            atividade = {
                'nome': input("  Nome da atividade: ").strip(),
                'codigo': input("  Código (se houver, ou deixe vazio): ").strip(),
                'categoria': self._escolher_opcao(
                    "  Categoria",
                    ['Verde', 'Transição', 'Não-elegível']
                ),
                'descricao': input("  Descrição resumida: ").strip(),
                'objetivo_principal': dados['objetivos_ambientais'][0] if dados['objetivos_ambientais'] else ''
            }
            dados['atividades'].append(atividade)
            
            # Mapeamento CNAE para esta atividade
            print(f"\n  CNAEs relacionados a '{atividade['nome']}':")
            while True:
                cnae = input("    CNAE (ou Enter para próxima atividade): ").strip()
                if not cnae:
                    break
                
                cnae_map = {
                    'cnae': cnae,
                    'atividade': atividade['nome'],
                    'tipo_alinhamento': self._escolher_opcao(
                        "    Tipo de alinhamento",
                        ['Core', 'Adjacent', 'Transição']
                    ),
                    'descricao_cnae': input("    Descrição do CNAE: ").strip()
                }
                dados['cnaes_mapeados'].append(cnae_map)
        
        # 4. Critérios técnicos
        print("\n📊 CRITÉRIOS TÉCNICOS")
        print("-" * 60)
        tipo_criterio = self._escolher_opcao(
            "Tipo predominante de critérios",
            ['Quantitativos', 'Qualitativos', 'Mistos']
        )
        dados['criterios_tecnicos']['tipo'] = tipo_criterio
        
        tem_thresholds = input("Há thresholds numéricos específicos? (s/n): ").strip().lower() == 's'
        dados['criterios_tecnicos']['tem_thresholds'] = tem_thresholds
        
        if tem_thresholds:
            print("  Exemplos de thresholds (máximo 3):")
            thresholds = []
            for i in range(3):
                threshold = input(f"    Threshold {i+1} (ou Enter para pular): ").strip()
                if threshold:
                    thresholds.append(threshold)
            dados['criterios_tecnicos']['exemplos_thresholds'] = thresholds
        
        # 5. Análise quantitativa
        print("\n📈 ESTIMATIVAS QUANTITATIVAS")
        print("-" * 60)
        try:
            dados['empresas_potenciais'] = int(input("Empresas potencialmente elegíveis (estimativa): ") or "0")
            dados['empregos_potenciais'] = int(input("Empregos verdes potenciais (estimativa): ") or "0")
        except ValueError:
            dados['empresas_potenciais'] = 0
            dados['empregos_potenciais'] = 0
        
        # 6. Insights e observações
        print("\n💡 INSIGHTS E OBSERVAÇÕES")
        print("-" * 60)
        print("Digite seus insights (um por linha, linha vazia para finalizar):")
        while True:
            insight = input("  → ").strip()
            if not insight:
                break
            dados['insights'].append(insight)
        
        # 7. Salvar resultados
        self._salvar_analise(setor, dados)
        self._gerar_relatorio_markdown(setor, dados)
        
        print(f"\n✅ Análise concluída!")
        print(f"📁 Dados salvos em:")
        print(f"   - JSON: {self.dirs['analises'] / f'{setor.lower()}.json'}")
        print(f"   - MD: {self.dirs['analises'] / f'{setor.lower()}_relatorio.md'}")
        
        return dados
    
    def _escolher_opcao(self, pergunta: str, opcoes: List[str]) -> str:
        """Helper para escolha múltipla"""
        print(f"{pergunta}:")
        for i, opcao in enumerate(opcoes, 1):
            print(f"    {i}. {opcao}")
        while True:
            try:
                escolha = int(input("  Escolha (número): ").strip())
                if 1 <= escolha <= len(opcoes):
                    return opcoes[escolha - 1]
            except ValueError:
                pass
            print("  ⚠️  Escolha inválida. Tente novamente.")
    
    def _salvar_analise(self, setor: str, dados: Dict):
        """Salva análise em JSON e CSV"""
        # JSON completo
        json_path = self.dirs['analises'] / f"{setor.lower()}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        # CSV de atividades
        if dados['atividades']:
            csv_path = self.dirs['extratos'] / f"{setor.lower()}_atividades.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=dados['atividades'][0].keys())
                writer.writeheader()
                writer.writerows(dados['atividades'])
        
        # CSV de mapeamentos CNAE
        if dados['cnaes_mapeados']:
            csv_path = self.dirs['mapeamentos'] / f"{setor.lower()}_cnae_mapping.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=dados['cnaes_mapeados'][0].keys())
                writer.writeheader()
                writer.writerows(dados['cnaes_mapeados'])
    
    def _gerar_relatorio_markdown(self, setor: str, dados: Dict):
        """Gera relatório em Markdown"""
        md_path = self.dirs['analises'] / f"{setor.lower()}_relatorio.md"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Análise - Setor {setor}\n\n")
            f.write(f"**Data da análise**: {dados['data_analise']}\n")
            f.write(f"**Caderno**: {dados.get('caderno_nome', 'N/A')}\n")
            f.write(f"**Versão**: {dados.get('caderno_versao', 'N/A')}\n\n")
            
            # Objetivos
            f.write("## Objetivos Ambientais\n\n")
            for obj in dados.get('objetivos_ambientais', []):
                f.write(f"- {obj}\n")
            f.write("\n")
            
            # Atividades
            f.write(f"## Atividades Elegíveis ({len(dados.get('atividades', []))})\n\n")
            for ativ in dados.get('atividades', []):
                f.write(f"### {ativ['nome']}\n\n")
                f.write(f"- **Categoria**: {ativ['categoria']}\n")
                if ativ.get('codigo'):
                    f.write(f"- **Código**: {ativ['codigo']}\n")
                f.write(f"- **Descrição**: {ativ['descricao']}\n\n")
            
            # Mapeamentos CNAE
            f.write(f"## Mapeamentos CNAE ({len(dados.get('cnaes_mapeados', []))})\n\n")
            f.write("| CNAE | Atividade | Alinhamento | Descrição |\n")
            f.write("|------|-----------|-------------|------------|\n")
            for cnae in dados.get('cnaes_mapeados', []):
                f.write(f"| {cnae['cnae']} | {cnae['atividade']} | {cnae['tipo_alinhamento']} | {cnae['descricao_cnae']} |\n")
            f.write("\n")
            
            # Critérios
            criterios = dados.get('criterios_tecnicos', {})
            f.write("## Critérios Técnicos\n\n")
            f.write(f"- **Tipo**: {criterios.get('tipo', 'N/A')}\n")
            f.write(f"- **Thresholds numéricos**: {'Sim' if criterios.get('tem_thresholds') else 'Não'}\n\n")
            
            if criterios.get('exemplos_thresholds'):
                f.write("**Exemplos de thresholds**:\n")
                for t in criterios['exemplos_thresholds']:
                    f.write(f"- {t}\n")
                f.write("\n")
            
            # Estimativas
            f.write("## Estimativas Quantitativas\n\n")
            f.write(f"- **Empresas potenciais**: {dados.get('empresas_potenciais', 0):,}\n")
            f.write(f"- **Empregos potenciais**: {dados.get('empregos_potenciais', 0):,}\n\n")
            
            # Insights
            if dados.get('insights'):
                f.write("## Insights\n\n")
                for insight in dados['insights']:
                    f.write(f"- {insight}\n")
    
    def consolidar_setores(self) -> Dict:
        """Consolida análises de múltiplos setores"""
        analises_dir = self.dirs['analises']
        consolidado = {
            'total_setores': 0,
            'total_atividades': 0,
            'total_cnaes': 0,
            'empresas_total': 0,
            'empregos_total': 0,
            'setores': []
        }
        
        for json_file in analises_dir.glob('*.json'):
            if json_file.stem.endswith('_consolidado'):
                continue
                
            with open(json_file, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            consolidado['total_setores'] += 1
            consolidado['total_atividades'] += len(dados.get('atividades', []))
            consolidado['total_cnaes'] += len(dados.get('cnaes_mapeados', []))
            consolidado['empresas_total'] += dados.get('empresas_potenciais', 0)
            consolidado['empregos_total'] += dados.get('empregos_potenciais', 0)
            
            consolidado['setores'].append({
                'nome': dados['setor'],
                'atividades': len(dados.get('atividades', [])),
                'cnaes': len(dados.get('cnaes_mapeados', [])),
                'empresas': dados.get('empresas_potenciais', 0),
                'empregos': dados.get('empregos_potenciais', 0)
            })
        
        # Salvar consolidado
        json_path = analises_dir / 'analise_consolidada.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(consolidado, f, ensure_ascii=False, indent=2)
        
        # Relatório consolidado
        self._gerar_relatorio_consolidado(consolidado)
        
        return consolidado
    
    def _gerar_relatorio_consolidado(self, dados: Dict):
        """Gera relatório consolidado em Markdown"""
        md_path = self.dirs['analises'] / 'CONSOLIDADO.md'
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Taxonomia Sustentável Brasileira - Análise Consolidada\n\n")
            f.write(f"**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            f.write("## Resumo Geral\n\n")
            f.write(f"- **Setores analisados**: {dados['total_setores']}\n")
            f.write(f"- **Atividades elegíveis**: {dados['total_atividades']}\n")
            f.write(f"- **CNAEs mapeados**: {dados['total_cnaes']}\n")
            f.write(f"- **Empresas potenciais**: {dados['empresas_total']:,}\n")
            f.write(f"- **Empregos verdes potenciais**: {dados['empregos_total']:,}\n\n")
            
            f.write("## Detalhamento por Setor\n\n")
            f.write("| Setor | Atividades | CNAEs | Empresas | Empregos |\n")
            f.write("|-------|-----------|-------|----------|----------|\n")
            
            for setor in dados['setores']:
                f.write(f"| {setor['nome']} | {setor['atividades']} | {setor['cnaes']} | ")
                f.write(f"{setor['empresas']:,} | {setor['empregos']:,} |\n")
            
            f.write("\n## Próximos Passos\n\n")
            f.write("- [ ] Validar mapeamentos CNAE com especialistas\n")
            f.write("- [ ] Desenvolver algoritmo de scoring automático\n")
            f.write("- [ ] Criar POC para setor prioritário\n")
            f.write("- [ ] Iniciar desenvolvimento de API endpoints\n")


def main():
    parser = argparse.ArgumentParser(
        description='Extrator de dados da Taxonomia Sustentável Brasileira'
    )
    parser.add_argument(
        '--setor',
        help='Nome do setor para análise interativa'
    )
    parser.add_argument(
        '--consolidar',
        action='store_true',
        help='Consolidar análises de todos os setores'
    )
    
    args = parser.parse_args()
    
    extrator = TaxonomiaBRExtractor()
    
    if args.consolidar:
        print("🔄 Consolidando análises de todos os setores...")
        resultado = extrator.consolidar_setores()
        print(f"\n✅ Consolidação concluída!")
        print(f"📊 {resultado['total_setores']} setores, {resultado['total_atividades']} atividades")
        print(f"📁 Relatório em: data/taxonomia_br/analises/CONSOLIDADO.md")
    
    elif args.setor:
        extrator.analise_interativa(args.setor)
    
    else:
        # Modo menu
        print("\n" + "="*60)
        print("TAXONOMIA SUSTENTÁVEL BRASILEIRA - EXTRATOR DE DADOS")
        print("="*60 + "\n")
        print("Escolha uma opção:")
        print("  1. Análise interativa de um setor")
        print("  2. Consolidar análises existentes")
        print("  3. Sair")
        
        escolha = input("\nOpção: ").strip()
        
        if escolha == '1':
            setor = input("Nome do setor: ").strip()
            extrator.analise_interativa(setor)
        elif escolha == '2':
            resultado = extrator.consolidar_setores()
            print(f"\n✅ {resultado['total_setores']} setores consolidados!")
        else:
            print("👋 Até logo!")


if __name__ == '__main__':
    main()
