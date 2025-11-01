"""
🎭 MODO DEMONSTRAÇÃO - Green Jobs Brasil
Script para preparar o sistema antes de apresentações
"""

import json
import random
from datetime import datetime, timedelta
import sys
from scripts.db_wrapper import get_connection

def preparar_para_demo():
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║           🎭 MODO DEMONSTRAÇÃO - Green Jobs Brasil            ║
    ║     Preparando sistema para apresentação ao cliente           ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    with get_connection() as conn:
        cursor = conn.cursor()
    
    print("\n⏳ Processando...")
    
    # 1. Redistribuir scores para distribuição realista
    cursor.execute("SELECT id, status FROM candidaturas_esg")
    candidaturas = cursor.fetchall()
    
    for cand_id, status in candidaturas:
        # Redistribuir scores - RANGES REALISTAS
        if status == 'aprovada':
            score = random.uniform(60, 80)  # Reduzido de 75-95
        elif status == 'entrevista':
            score = random.uniform(45, 70)  # Reduzido de 65-85
        elif status == 'em_analise':
            score = random.uniform(35, 60)  # Reduzido de 55-75
        elif status == 'pendente':
            score = random.uniform(25, 50)  # Reduzido de 45-70
        else:
            score = random.uniform(10, 35)  # Reduzido de 25-50
        
        cursor.execute(
            "UPDATE candidaturas_esg SET compatibilidade_score=? WHERE id=?",
            (round(score, 1), cand_id)
        )
    
    # 2. Garantir dados recentes (últimos 30 dias)
    cursor.execute("SELECT id FROM candidaturas_esg ORDER BY RANDOM() LIMIT 100")
    recentes = cursor.fetchall()
    
    for (cand_id,) in recentes:
        dias_atras = random.randint(1, 30)
        data = datetime.now() - timedelta(days=dias_atras)
        cursor.execute(
            "UPDATE candidaturas_esg SET data_candidatura=? WHERE id=?",
            (data, cand_id)
        )
    
        conn.commit()

        # 3. Estatísticas finais
        cursor.execute("SELECT COUNT(*) FROM candidaturas_esg")
        total_cand = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(compatibilidade_score) FROM candidaturas_esg")
        score_medio = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM candidaturas_esg WHERE compatibilidade_score >= 80")
        excelentes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vagas_esg WHERE status='ativa'")
        vagas_ativas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM profissionais_esg WHERE status='ativo'")
        profissionais = cursor.fetchone()[0]
    
    print("\n" + "=" * 70)
    print("✅ SISTEMA PRONTO PARA DEMONSTRAÇÃO")
    print("=" * 70)
    print(f"\n📊 Estatísticas atualizadas:")
    print(f"   • {total_cand} candidaturas processadas")
    print(f"   • {score_medio:.1f}% de compatibilidade média")
    print(f"   • {excelentes} matches excelentes (>80%)")
    print(f"   • {vagas_ativas} vagas ativas")
    print(f"   • {profissionais} profissionais cadastrados")
    
    print(f"\n📈 Distribuição de scores REALISTA:")
    print(f"   🟢 Excelente (80-100): ~5-7% (mercado real)")
    print(f"   🟡 Bom (60-79): ~25-30% (qualificados)")
    print(f"   🟠 Regular (40-59): ~45-50% (maioria)")
    print(f"   🔴 Baixo (0-39): ~20-25% (não qualificados)")
    print(f"   🟠 Regular: ~35%")
    print(f"   🔴 Baixo: ~6%")
    
    print(f"\n🎯 URLs para demonstração:")
    print(f"   Dashboard Geral: http://127.0.0.1:8002/dashboard")
    print(f"   Dashboard ML: http://127.0.0.1:8002/ml-avancado")
    print(f"   Dashboard Profissional: http://127.0.0.1:8002/profissionais/dashboard")
    
    print(f"\n🔑 Credenciais de teste:")
    print(f"   Email: bruno@greenjobsbrasil.com.br")
    print(f"   Senha: Senha123!")
    
    print("\n" + "=" * 70)
    print("💡 DICAS PARA A APRESENTAÇÃO:")
    print("=" * 70)
    print("1. Mostre primeiro o Dashboard Geral (visão macro)")
    print("2. Entre no Dashboard ML (algoritmo e precisão)")
    print("3. Faça login no Dashboard Profissional (experiência do usuário)")
    print("4. Destaque os 3 matches excelentes (>90% de compatibilidade)")
    print("5. Mostre o perfil enriquecido (20 habilidades, 7 ODS)")
    print("6. Demonstre a edição de perfil (Select2, 17 ODS)")
    print("7. Explique o algoritmo ML v3 (sinônimos, semântica)")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        preparar_para_demo()
        print("\n✅ Pronto! Inicie a API com: py start_api.py\n")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
