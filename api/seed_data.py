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
    """Popula banco com dados de exemplo - SEMPRE roda no Render"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Limpar dados anteriores (para Render)
    try:
        cursor.execute("DELETE FROM storytelling")
        cursor.execute("DELETE FROM vagas")
        cursor.execute("DELETE FROM empresas_esg")
        cursor.execute("DELETE FROM profissionais_esg")
        print("🧹 Limpando dados antigos...")
    except:
        pass  # Tabelas podem não existir ainda
    
    print("📊 Populando banco com dados de exemplo...")
    
    # Inserir profissionais
    profissionais = [
        ("Maria Silva", "maria.silva@email.com", "Energia Solar", 5, "São Paulo", "SP"),
        ("João Santos", "joao.santos@email.com", "Economia Circular", 3, "Rio de Janeiro", "RJ"),
        ("Ana Costa", "ana.costa@email.com", "Gestão de Resíduos", 7, "Curitiba", "PR"),
        ("Carlos Oliveira", "carlos.oliveira@email.com", "Mobilidade Sustentável", 4, "Porto Alegre", "RS")
    ]
    
    cursor.executemany(
        "INSERT INTO profissionais_esg (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf) VALUES (?, ?, ?, ?, ?, ?)",
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
    
    # Inserir empresas ESG
    empresas = [
        ("12345678000190", "EcoSolar Ltda", "EcoSolar", 85.5),
        ("98765432000110", "Verde Circular SA", "Verde Circular", 78.2),
        ("11223344000155", "Mobilidade Verde", "Mob Verde", 82.7)
    ]
    
    cursor.executemany(
        "INSERT INTO empresas_esg (cnpj, razao_social, nome_fantasia, score_verde) VALUES (?, ?, ?, ?)",
        empresas
    )
    
    # Inserir vagas
    vagas = [
        ("Analista Energia Solar Júnior", "Vaga para atuar com projetos de energia solar residencial", "12345678000190", "junior", "CLT", "São Paulo", "SP", 0, "ativa", 3000, 4500),
        ("Especialista em Economia Circular", "Desenvolver estratégias de economia circular", "98765432000110", "senior", "PJ", "Rio de Janeiro", "RJ", 1, "ativa", 8000, 12000),
        ("Coordenador de Sustentabilidade", "Coordenar projetos ESG e sustentabilidade", "11223344000155", "pleno", "CLT", "Curitiba", "PR", 0, "ativa", 5500, 7500),
    ]
    
    cursor.executemany(
        "INSERT INTO vagas (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        vagas
    )
    
    conn.commit()
    print("✅ Dados inseridos com sucesso!")
    print(f"   - {len(profissionais)} profissionais")
    print(f"   - {len(storytelling_data)} perfis storytelling")
    print(f"   - {len(empresas)} empresas ESG")
    print(f"   - {len(vagas)} vagas")
    
    conn.close()

if __name__ == "__main__":
    seed_database()
