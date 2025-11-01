"""
Sistema de Simulação e Enriquecimento de Dados
Gera candidaturas, vagas e dados dinâmicos para demonstrações
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from scripts.db_wrapper import get_connection

class SimuladorGreenJobs:
    def __init__(self, db_path='gjb_dev.db'):
        # do not hold a persistent connection; use context manager per operation
        self.db_path = db_path

        # Configurações
        self.STATUS_CANDIDATURA = ['pendente', 'em_analise', 'entrevista', 'aprovada', 'rejeitada']
        self.PESOS_STATUS = [0.30, 0.25, 0.20, 0.15, 0.10]  # Distribuição realista
        
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def redistribuir_scores_candidaturas(self):
        """Redistribui scores das candidaturas para uma curva mais realista"""
        print("=" * 70)
        print("📊 REDISTRIBUINDO SCORES DE CANDIDATURAS")
        print("=" * 70)
        
        # Buscar todas as candidaturas
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.profissional_id, c.vaga_id, c.status
                FROM candidaturas_esg c
            """)
            candidaturas = cursor.fetchall()
        
        scores_antes = []
        scores_depois = []
        
        for cand in candidaturas:
            # Score antigo
            cursor.execute(
                "SELECT compatibilidade_score FROM candidaturas_esg WHERE id=?", 
                (cand['id'],)
            )
            score_antigo = cursor.fetchone()[0]
            scores_antes.append(score_antigo)
            
            # Gerar novo score baseado no status - RANGES REALISTAS
            status = cand['status']
            
            if status == 'aprovada':
                # Aprovadas: 60-80% (reduzido de 70-95)
                novo_score = random.uniform(60, 80)
            elif status == 'entrevista':
                # Entrevista: 45-70% (reduzido de 60-85)
                novo_score = random.uniform(45, 70)
            elif status == 'em_analise':
                # Em análise: 35-60% (reduzido de 50-75)
                novo_score = random.uniform(35, 60)
            elif status == 'pendente':
                # Pendente: 25-50% (reduzido de 40-70)
                novo_score = random.uniform(25, 50)
            else:  # rejeitada
                # Rejeitada: 10-35% (reduzido de 20-50)
                novo_score = random.uniform(10, 35)
            
            novo_score = round(novo_score, 1)
            scores_depois.append(novo_score)
            
            # Atualizar
            cursor.execute("""
                UPDATE candidaturas_esg 
                SET compatibilidade_score = ?
                WHERE id = ?
            """, (novo_score, cand['id']))

        conn.commit()
        
        print(f"\n✅ {len(candidaturas)} candidaturas atualizadas")
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   Score médio ANTES: {sum(scores_antes)/len(scores_antes):.1f}%")
        print(f"   Score médio DEPOIS: {sum(scores_depois)/len(scores_depois):.1f}%")
        print(f"   Score mínimo: {min(scores_depois):.1f}%")
        print(f"   Score máximo: {max(scores_depois):.1f}%")
        
        # Distribuição por faixa
        excelente = len([s for s in scores_depois if s >= 80])
        bom = len([s for s in scores_depois if 60 <= s < 80])
        regular = len([s for s in scores_depois if 40 <= s < 60])
        baixo = len([s for s in scores_depois if s < 40])
        
        print(f"\n📈 DISTRIBUIÇÃO:")
        print(f"   🟢 Excelente (80-100): {excelente} ({excelente/len(scores_depois)*100:.1f}%)")
        print(f"   🟡 Bom (60-79): {bom} ({bom/len(scores_depois)*100:.1f}%)")
        print(f"   🟠 Regular (40-59): {regular} ({regular/len(scores_depois)*100:.1f}%)")
        print(f"   🔴 Baixo (0-39): {baixo} ({baixo/len(scores_depois)*100:.1f}%)")
        
        return {
            'total': len(candidaturas),
            'score_medio': sum(scores_depois)/len(scores_depois),
            'excelente': excelente,
            'bom': bom,
            'regular': regular,
            'baixo': baixo
        }
    
    def gerar_candidaturas_simuladas(self, num_candidaturas=50):
        """Gera candidaturas simuladas para enriquecer os dados"""
        print("\n" + "=" * 70)
        print("🎲 GERANDO CANDIDATURAS SIMULADAS")
        print("=" * 70)
        
        # Buscar profissionais e vagas disponíveis
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM profissionais_esg WHERE status='ativo' LIMIT 50")
            profissionais = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT id FROM vagas_esg WHERE status='ativa' LIMIT 100")
            vagas = [row[0] for row in cursor.fetchall()]
        
        if not profissionais or not vagas:
            print("⚠️ Não há profissionais ou vagas suficientes")
            return
        
        candidaturas_criadas = 0
        
        for _ in range(num_candidaturas):
            prof_id = random.choice(profissionais)
            vaga_id = random.choice(vagas)
            
            # Verificar se já existe
            cursor.execute("""
                SELECT id FROM candidaturas_esg 
                WHERE profissional_id=? AND vaga_id=?
            """, (prof_id, vaga_id))

            if cursor.fetchone():
                continue  # Já existe
            
            # Gerar dados
            status = random.choices(self.STATUS_CANDIDATURA, weights=self.PESOS_STATUS)[0]
            
            # Score baseado no status
            if status == 'aprovada':
                score = random.uniform(75, 95)
            elif status == 'entrevista':
                score = random.uniform(65, 85)
            elif status == 'em_analise':
                score = random.uniform(55, 75)
            elif status == 'pendente':
                score = random.uniform(45, 70)
            else:
                score = random.uniform(25, 50)
            
            score = round(score, 1)
            
            # Data aleatória nos últimos 60 dias
            dias_atras = random.randint(1, 60)
            data_candidatura = datetime.now() - timedelta(days=dias_atras)
            
            # Inserir
            cursor.execute("""
                INSERT INTO candidaturas_esg 
                (profissional_id, vaga_id, compatibilidade_score, status, data_candidatura)
                VALUES (?, ?, ?, ?, ?)
            """, (prof_id, vaga_id, score, status, data_candidatura))

            candidaturas_criadas += 1

        conn.commit()
        
        print(f"\n✅ {candidaturas_criadas} novas candidaturas criadas")
        
        return candidaturas_criadas
    
    def gerar_vagas_simuladas(self, num_vagas=20):
        """Gera vagas simuladas com dados realistas"""
        print("\n" + "=" * 70)
        print("💼 GERANDO VAGAS SIMULADAS")
        print("=" * 70)
        
        # Templates de vagas
        titulos = [
            "Analista de Sustentabilidade",
            "Coordenador ESG",
            "Especialista em Carbono",
            "Gerente de Meio Ambiente",
            "Analista de Energia Renovável",
            "Consultor de Economia Circular",
            "Especialista em Biodiversidade",
            "Analista de Mudanças Climáticas",
            "Coordenador de Compliance ESG",
            "Especialista em Relatórios GRI"
        ]
        
        niveis = ['junior', 'pleno', 'senior', 'especialista']
        cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Brasília']
        ufs = ['SP', 'RJ', 'MG', 'PR', 'RS', 'DF']
        
        habilidades_pool = [
            "ISO 14001", "GRI Standards", "Inventário GEE", "LCA", 
            "Net Zero", "Energia Renovável", "Economia Circular",
            "Stakeholder Engagement", "SASB", "CDP", "TCFD",
            "Due Diligence ESG", "Análise de Materialidade"
        ]
        
        ods_pool = [7, 8, 9, 11, 12, 13, 14, 15]
        
        # Buscar empresas
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT cnpj FROM empresas_verdes LIMIT 10")
            empresas = [row[0] for row in cursor.fetchall()]
        
        vagas_criadas = 0
        
        for _ in range(num_vagas):
            titulo = random.choice(titulos)
            nivel = random.choice(niveis)
            idx_cidade = random.randint(0, len(cidades)-1)
            cidade = cidades[idx_cidade]
            uf = ufs[idx_cidade]
            
            # Salário baseado no nível
            if nivel == 'junior':
                sal_min = random.randint(3000, 5000)
                sal_max = sal_min + random.randint(1000, 2000)
            elif nivel == 'pleno':
                sal_min = random.randint(6000, 9000)
                sal_max = sal_min + random.randint(2000, 4000)
            elif nivel == 'senior':
                sal_min = random.randint(10000, 15000)
                sal_max = sal_min + random.randint(3000, 7000)
            else:
                sal_min = random.randint(15000, 25000)
                sal_max = sal_min + random.randint(5000, 15000)
            
            # Habilidades (3-6 por vaga)
            num_habs = random.randint(3, 6)
            habilidades = random.sample(habilidades_pool, num_habs)
            
            # ODS (2-4 por vaga)
            num_ods = random.randint(2, 4)
            ods = random.sample(ods_pool, num_ods)
            ods_formatados = [f"ODS {o}" for o in ods]
            
            remoto = random.choice([True, False])
            cnpj = random.choice(empresas) if empresas else None
            
            descricao = f"Vaga para {nivel} em {titulo}. Empresa busca profissional com experiência em ESG."
            
            # Inserir
            try:
                cursor.execute("""
                    INSERT INTO vagas_esg 
                    (cnpj, titulo, descricao, nivel_experiencia, 
                     salario_min, salario_max, localizacao_cidade, localizacao_uf,
                     remoto, ods_tags, habilidades_requeridas, status, criada_em)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cnpj, titulo, descricao, nivel,
                    sal_min, sal_max, cidade, uf,
                    remoto, json.dumps(ods_formatados), json.dumps(habilidades),
                    'ativa', datetime.now()
                ))
                vagas_criadas += 1
            except Exception as e:
                print(f"⚠️ Erro ao criar vaga: {e}")
                continue

        conn.commit()
        
        print(f"\n✅ {vagas_criadas} novas vagas criadas")
        
        return vagas_criadas
    
    def executar_simulacao_completa(self):
        """Executa simulação completa do sistema"""
        print("\n" + "=" * 70)
        print("🚀 INICIANDO SIMULAÇÃO COMPLETA DO SISTEMA")
        print("=" * 70)
        
        resultados = {}

        # 1. Redistribuir scores existentes
        resultados['scores'] = self.redistribuir_scores_candidaturas()

        # 2. Gerar novas vagas
        resultados['vagas'] = self.gerar_vagas_simuladas(20)

        # 3. Gerar novas candidaturas
        resultados['candidaturas'] = self.gerar_candidaturas_simuladas(50)

        # 4. Estatísticas finais
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM vagas_esg WHERE status='ativa'")
            total_vagas = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM candidaturas_esg")
            total_candidaturas = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(compatibilidade_score) FROM candidaturas_esg")
            score_medio = cursor.fetchone()[0]
        
        print("\n" + "=" * 70)
        print("📊 ESTATÍSTICAS FINAIS DO SISTEMA")
        print("=" * 70)
        print(f"\n💼 Vagas ativas: {total_vagas}")
        print(f"📝 Total de candidaturas: {total_candidaturas}")
        print(f"📈 Score médio: {score_medio:.1f}%")
        
        resultados['totais'] = {
            'vagas': total_vagas,
            'candidaturas': total_candidaturas,
            'score_medio': score_medio
        }
        
        print("\n" + "=" * 70)
        print("✅ SIMULAÇÃO COMPLETA CONCLUÍDA!")
        print("=" * 70)
        print("\n💡 Próximos passos:")
        print("   1. Reinicie a API para aplicar as mudanças")
        print("   2. Acesse o dashboard para ver os novos gráficos")
        print("   3. Este script pode ser executado antes de demos")
        
        return resultados


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║     🌱 GREEN JOBS BRASIL - SIMULADOR DE DADOS                 ║
    ║     Sistema de Enriquecimento para Demonstrações              ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    simulador = SimuladorGreenJobs()
    
    try:
        resultados = simulador.executar_simulacao_completa()
        
        # Salvar log
        with open('simulacao_log.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'resultados': resultados
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Log salvo em: simulacao_log.json")
        
    except Exception as e:
        print(f"\n❌ Erro na simulação: {e}")
        import traceback
        traceback.print_exc()
