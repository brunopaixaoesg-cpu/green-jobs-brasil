"""
Script para popular banco de dados com dados de exemplo
Green Jobs Brasil - Dados iniciais para demonstração
"""
import sqlite3
import os
from datetime import datetime

# Caminho do banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "gjb_dev.db")

def seed_database():
    """Popula banco com dados de exemplo"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar se já tem dados
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"✅ Banco já tem {count} profissionais. Pulando seed.")
        conn.close()
        return
    
    print("📊 Populando banco com dados de exemplo...")
    
    # Inserir profissionais
    profissionais = [
        ("Maria Silva", "maria.silva@email.com", "Energia Solar"),
        ("João Santos", "joao.santos@email.com", "Economia Circular"),
        ("Ana Costa", "ana.costa@email.com", "Gestão de Resíduos"),
        ("Carlos Oliveira", "carlos.oliveira@email.com", "Mobilidade Sustentável")
    ]
    
    cursor.executemany(
        "INSERT INTO profissionais_esg (nome, email, area_atuacao) VALUES (?, ?, ?)",
        profissionais
    )
    
    # Inserir storytelling
    storytelling_data = [
        (
            1,
            "Comecei minha jornada verde instalando painéis solares em comunidades carentes...",
            "Sempre sonhei em trabalhar com energia limpa e fazer a diferença",
            "Já impactei mais de 500 famílias com acesso a energia solar"
        ),
        (
            2,
            "Trabalho transformando resíduos em novos produtos há 5 anos...",
            "Vi o potencial da economia circular durante meus estudos",
            "Reduzi 30 toneladas de resíduos em aterros"
        ),
        (
            3,
            "Especialista em gestão de resíduos sólidos urbanos...",
            "Quero criar cidades mais limpas e sustentáveis",
            "Implementei sistemas de coleta seletiva em 10 municípios"
        ),
        (
            4,
            "Desenvolvo projetos de mobilidade urbana sustentável...",
            "Acredito que transporte público de qualidade muda vidas",
            "Projetei ciclovias que reduziram 40% das emissões"
        )
    ]
    
    cursor.executemany(
        "INSERT INTO storytelling (profissional_id, jornada_verde, motivacao, impacto) VALUES (?, ?, ?, ?)",
        storytelling_data
    )
    
    conn.commit()
    print("✅ Dados inseridos com sucesso!")
    print(f"   - {len(profissionais)} profissionais")
    print(f"   - {len(storytelling_data)} perfis storytelling")
    
    conn.close()

if __name__ == "__main__":
    seed_database()
