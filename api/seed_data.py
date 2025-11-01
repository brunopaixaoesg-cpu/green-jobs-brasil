"""
Script para popular banco de dados com dados de exemplo
Green Jobs Brasil - Dados iniciais para demonstração
SQLite Local
"""
import os
from datetime import datetime

# Use centralized DB helper
from api.db import get_db
from api.logger import logger

def seed_database():
    """Popula banco com dados de exemplo - SEMPRE roda no Render"""
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Limpar dados anteriores (para Render)
    try:
        cursor.execute("DELETE FROM storytelling")
        cursor.execute("DELETE FROM vagas")
        cursor.execute("DELETE FROM empresas_esg")
        cursor.execute("DELETE FROM profissionais_esg")
        conn.commit()
        logger.info("Limpando dados antigos...")
    except Exception as e:
        logger.warning("Aviso ao limpar dados: %s", e)
        conn.rollback()
    
    logger.info("Populando banco com dados de exemplo...")
    
    # Inserir profissionais e capturar IDs reais
    profissionais = [
        ("Maria Silva", "maria.silva@email.com", "Energia Solar", 5, "São Paulo", "SP"),
        ("João Santos", "joao.santos@email.com", "Economia Circular", 3, "Rio de Janeiro", "RJ"),
        ("Ana Costa", "ana.costa@email.com", "Gestão de Resíduos", 7, "Curitiba", "PR"),
        ("Carlos Oliveira", "carlos.oliveira@email.com", "Mobilidade Sustentável", 4, "Porto Alegre", "RS")
    ]
    
    profissional_ids = []
    for nome, email, area, experiencia, cidade, uf in profissionais:
        cursor.execute(
            "INSERT INTO profissionais_esg (nome_completo, email, anos_experiencia_esg, localizacao_cidade, localizacao_uf) VALUES (?, ?, ?, ?, ?)",
            (nome, email, experiencia, cidade, uf)
        )
        prof_id = cursor.lastrowid
        profissional_ids.append(prof_id)
    
    # Inserir storytelling usando IDs reais
    storytelling_data = [
        (
            profissional_ids[0],
            "Comecei minha jornada verde instalando painéis solares em comunidades carentes...",
            "Sempre sonhei em trabalhar com energia limpa e fazer a diferença",
            "Já impactei mais de 500 famílias com acesso a energia solar"
        ),
        (
            profissional_ids[1],
            "Trabalho transformando resíduos em novos produtos há 5 anos...",
            "Vi o potencial da economia circular durante meus estudos",
            "Reduzi 30 toneladas de resíduos em aterros"
        ),
        (
            profissional_ids[2],
            "Especialista em gestão de resíduos sólidos urbanos...",
            "Quero criar cidades mais limpas e sustentáveis",
            "Implementei sistemas de coleta seletiva em 10 municípios"
        ),
        (
            profissional_ids[3],
            "Desenvolvo projetos de mobilidade urbana sustentável...",
            "Acredito que transporte público de qualidade muda vidas",
            "Projetei ciclovias que reduziram 40% das emissões"
        )
    ]
    
    for story in storytelling_data:
        cursor.execute(
            "INSERT INTO storytelling (profissional_id, jornada_verde, motivacao, impacto) VALUES (?, ?, ?, ?)",
            story
        )
    
    # Inserir empresas ESG
    empresas = [
        ("12345678000190", "EcoSolar Ltda", "EcoSolar", 85.5),
        ("98765432000110", "Verde Circular SA", "Verde Circular", 78.2),
        ("11223344000155", "Mobilidade Verde", "Mob Verde", 82.7)
    ]
    
    for emp in empresas:
        cursor.execute(
            "INSERT INTO empresas_esg (cnpj, razao_social, nome_fantasia, score_verde) VALUES (?, ?, ?, ?)",
            emp
        )
    
    # Inserir vagas (usar TRUE/FALSE para PostgreSQL boolean)
    vagas = [
        ("Analista Energia Solar Júnior", "Vaga para atuar com projetos de energia solar residencial", "12345678000190", "junior", "CLT", "São Paulo", "SP", False, "ativa", 3000, 4500),
        ("Especialista em Economia Circular", "Desenvolver estratégias de economia circular", "98765432000110", "senior", "PJ", "Rio de Janeiro", "RJ", True, "ativa", 8000, 12000),
        ("Coordenador de Sustentabilidade", "Coordenar projetos ESG e sustentabilidade", "11223344000155", "pleno", "CLT", "Curitiba", "PR", False, "ativa", 5500, 7500),
    ]
    
    for vaga in vagas:
        cursor.execute(
            "INSERT INTO vagas (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            vaga
        )
    
    conn.commit()
    logger.info("Dados inseridos com sucesso!")
    logger.info("   - %s profissionais", len(profissionais))
    logger.info("   - %s perfis storytelling", len(storytelling_data))
    logger.info("   - %s empresas ESG", len(empresas))
    logger.info("   - %s vagas", len(vagas))
    
    conn.close()

if __name__ == "__main__":
    seed_database()
