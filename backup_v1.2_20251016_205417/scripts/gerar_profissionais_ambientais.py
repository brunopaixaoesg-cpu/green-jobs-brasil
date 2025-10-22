#!/usr/bin/env python3
"""
Gerador de Profissionais Ambientais Realísticos - Green Jobs Brasil
====================================================================
Cria perfis específicos para área ambiental com dados mais realísticos
para demonstração focada no setor que você conhece.
"""

import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configurações
DATABASE_PATH = Path("gjb_dev.db")

# Dados específicos da área ambiental
NOMES_AMBIENTAIS = [
    "Ana Beatriz Santos", "Carlos Eduardo Lima", "Mariana Costa Silva", 
    "João Paulo Ferreira", "Fernanda Rodrigues", "Rafael Almeida",
    "Patrícia Oliveira", "Thiago Barros", "Juliana Mendes", "Diego Carvalho",
    "Camila Nascimento", "Bruno Machado", "Letícia Ribeiro", "André Felipe",
    "Vanessa Moreira", "Lucas Gabriel", "Isabela Torres", "Matheus Souza",
    "Priscila Andrade", "Fernando Dias", "Amanda Silva", "Gustavo Pereira",
    "Renata Campos", "Victor Hugo", "Carolina Freitas", "Daniel Rocha"
]

# Cargos específicos da área ambiental
CARGOS_AMBIENTAIS = [
    "Analista Ambiental", "Consultor em Meio Ambiente", "Especialista em Licenciamento",
    "Coordenador de Gestão Ambiental", "Técnico em Meio Ambiente", "Engenheiro Ambiental",
    "Biólogo Consultor", "Analista de Recursos Hídricos", "Especialista em Resíduos",
    "Consultor em Sustentabilidade", "Analista de Impacto Ambiental", "Gestor Ambiental",
    "Especialista em Mudanças Climáticas", "Auditor Ambiental", "Coordenador de EHS",
    "Analista de Monitoramento Ambiental", "Consultor ISO 14001", "Especialista em Biodiversidade"
]

# Empresas que realmente contratam profissionais ambientais
EMPRESAS_AMBIENTAIS = [
    "Vale", "Petrobras", "Sabesp", "Copel", "Cemig", "Eletrobras",
    "Suzano", "Klabin", "Fibria", "JBS", "BRF", "Cargill",
    "Ambev", "Natura", "Unilever", "BASF", "Dow Chemical", "3M",
    "Consulting Ambiental", "TAESA", "EDP Brasil", "Engie Brasil",
    "Arcadis", "Golder Associates", "AECOM", "Tractebel Engineering"
]

# Habilidades específicas da área ambiental
HABILIDADES_AMBIENTAIS = [
    "Licenciamento Ambiental", "EIA/RIMA", "Gestão de Resíduos", "ISO 14001",
    "Monitoramento Ambiental", "Recursos Hídricos", "Mudanças Climáticas", "Biodiversidade",
    "Auditoria Ambiental", "Legislação Ambiental", "Geoprocessamento", "SIG",
    "Inventário GEE", "Pegada de Carbono", "ACV - Análise do Ciclo de Vida",
    "Recuperação de Áreas Degradadas", "Tratamento de Efluentes", "Gestão de Stakeholders",
    "Educação Ambiental", "Due Diligence Ambiental", "Compliance Ambiental"
]

# Certificações ambientais reconhecidas
CERTIFICACOES_AMBIENTAIS = [
    "CRA - Conselho Regional de Administração", "CREA - Engenharia Ambiental",
    "CRBio - Conselho Regional de Biologia", "ISO 14001 Lead Auditor",
    "Certified Environmental Manager (CEM)", "LEED Green Associate",
    "Carbon Footprint Analyst", "EMS Internal Auditor", "OHSAS 18001",
    "Specialist in Environmental Impact Assessment", "GHG Protocol",
    "NEBOSH Environmental Certificate", "Certified Sustainability Professional"
]

# Formações típicas da área
FORMACOES_AMBIENTAIS = [
    "Engenharia Ambiental", "Biologia", "Geografia", "Engenharia Florestal",
    "Gestão Ambiental", "Engenharia Sanitária", "Ecologia", "Geologia",
    "Engenharia Química", "Ciências Ambientais", "Engenharia Civil",
    "Administração com foco em Sustentabilidade"
]

# Especializações/Pós-graduação
ESPECIALIZACOES = [
    "MBA em Gestão Ambiental", "Especialização em Licenciamento Ambiental",
    "Mestrado em Engenharia Ambiental", "Pós em Auditoria Ambiental",
    "MBA em Sustentabilidade", "Especialização em Recursos Hídricos",
    "Pós em Mudanças Climáticas", "MBA em Meio Ambiente e Desenvolvimento Sustentável"
]

def conectar_db():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect(DATABASE_PATH)

def gerar_perfil_ambiental():
    """Gera um perfil profissional realístico da área ambiental"""
    nome = random.choice(NOMES_AMBIENTAIS)
    
    # Anos de experiência mais realísticos
    anos_total = random.randint(2, 25)
    anos_ambiental = min(anos_total, random.randint(1, anos_total))
    
    # Nível baseado na experiência
    if anos_total <= 3:
        nivel = "junior"
    elif anos_total <= 8:
        nivel = "pleno"
    elif anos_total <= 15:
        nivel = "senior"
    else:
        nivel = "especialista"
    
    # Cargo atual
    cargo = random.choice(CARGOS_AMBIENTAIS)
    empresa = random.choice(EMPRESAS_AMBIENTAIS)
    
    # Formação
    formacao_base = random.choice(FORMACOES_AMBIENTAIS)
    especializacao = random.choice(ESPECIALIZACOES) if random.random() > 0.3 else None
    
    # Habilidades (3-7 por profissional)
    num_habilidades = random.randint(3, 7)
    habilidades = random.sample(HABILIDADES_AMBIENTAIS, num_habilidades)
    
    # Certificações (0-3 por profissional)
    num_cert = random.randint(0, 3)
    certificacoes = random.sample(CERTIFICACOES_AMBIENTAIS, num_cert) if num_cert > 0 else []
    
    # Salário realístico baseado no nível
    if nivel == "junior":
        salario_min = random.randint(3000, 5000)
        salario_max = salario_min + random.randint(1000, 2000)
    elif nivel == "pleno":
        salario_min = random.randint(5000, 8000)
        salario_max = salario_min + random.randint(2000, 3000)
    elif nivel == "senior":
        salario_min = random.randint(8000, 15000)
        salario_max = salario_min + random.randint(3000, 5000)
    else:  # especialista
        salario_min = random.randint(15000, 25000)
        salario_max = salario_min + random.randint(5000, 15000)
    
    # Estados com mais oportunidades ambientais
    estados_ambientais = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "GO"]
    uf = random.choice(estados_ambientais)
    
    # Cidades por estado
    cidades = {
        "SP": ["São Paulo", "Campinas", "Santos", "São José dos Campos"],
        "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis", "Campos dos Goytacazes"],
        "MG": ["Belo Horizonte", "Contagem", "Juiz de Fora", "Uberlândia"],
        "RS": ["Porto Alegre", "Caxias do Sul", "Canoas", "Pelotas"],
        "PR": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa"],
        "SC": ["Florianópolis", "Joinville", "Blumenau", "Chapecó"],
        "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari"],
        "PE": ["Recife", "Jaboatão dos Guararapes", "Olinda", "Caruaru"],
        "CE": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Maracanaú"],
        "GO": ["Goiânia", "Aparecida de Goiânia", "Anápolis", "Rio Verde"]
    }
    cidade = random.choice(cidades[uf])
    
    # Email corporativo realístico
    email_base = nome.lower().replace(" ", ".").replace("ã", "a").replace("ç", "c")
    email = f"{email_base}@email.com"
    
    # Aceita remoto (área ambiental tem trabalho de campo, então nem todos aceitam 100% remoto)
    aceita_remoto = random.choice([True, False, True])  # 66% aceita remoto
    
    return {
        "email": email,
        "nome_completo": nome,
        "telefone": f"({random.randint(11, 85)}){random.randint(90000, 99999)}-{random.randint(1000, 9999)}",
        "linkedin_url": f"https://linkedin.com/in/{email_base}",
        "localizacao_uf": uf,
        "localizacao_cidade": cidade,
        "aceita_remoto": aceita_remoto,
        "disponivel_mudanca": random.choice([True, False]),
        "anos_experiencia_total": anos_total,
        "anos_experiencia_esg": anos_ambiental,
        "cargo_atual": cargo,
        "empresa_atual": empresa,
        "formacao_nivel": "superior",
        "formacao_area": formacao_base,
        "instituicao": f"Universidade {random.choice(['Federal', 'Estadual', 'Particular'])}",
        "ods_interesse": "ODS 6 - Água Limpa, ODS 13 - Mudanças Climáticas, ODS 14 - Oceanos, ODS 15 - Biodiversidade",
        "ods_experiencia": random.choice([
            "ODS 6 - Água Limpa, ODS 14 - Oceanos",
            "ODS 13 - Mudanças Climáticas, ODS 15 - Biodiversidade", 
            "ODS 6 - Água Limpa, ODS 13 - Mudanças Climáticas",
            "ODS 14 - Oceanos, ODS 15 - Biodiversidade"
        ]),
        "habilidades_esg": ", ".join(habilidades),
        "certificacoes": ", ".join(certificacoes),
        "areas_interesse": random.choice([
            "Licenciamento Ambiental, Consultoria",
            "Gestão de Resíduos, Sustentabilidade Corporativa",
            "Recursos Hídricos, Monitoramento",
            "Mudanças Climáticas, Carbono",
            "Biodiversidade, Conservação"
        ]),
        "nivel_desejado": nivel,
        "tipo_contratacao_desejado": random.choice(["CLT", "PJ", "CLT"]),  # CLT mais comum
        "pretensao_salarial_min": float(salario_min),
        "pretensao_salarial_max": float(salario_max),
        "resumo_profissional": f"Profissional da área ambiental com {anos_total} anos de experiência, especializado em {habilidades[0]} e {habilidades[1] if len(habilidades) > 1 else 'gestão ambiental'}. {especializacao if especializacao else 'Graduado em ' + formacao_base}.",
        "motivacao_esg": random.choice([
            "Paixão por preservação ambiental e desenvolvimento sustentável",
            "Busco contribuir para um futuro mais sustentável através da minha experiência técnica",
            "Acredito que a área ambiental é fundamental para o desenvolvimento do país",
            "Quero fazer a diferença na conservação dos recursos naturais brasileiros"
        ])
    }

def inserir_profissional_ambiental(perfil):
    """Insere profissional ambiental no banco de dados"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO profissionais_esg (
            email, nome_completo, telefone, linkedin_url, localizacao_uf, localizacao_cidade,
            aceita_remoto, disponivel_mudanca, anos_experiencia_total, anos_experiencia_esg,
            cargo_atual, empresa_atual, formacao_nivel, formacao_area, instituicao,
            ods_interesse, ods_experiencia, habilidades_esg, certificacoes, areas_interesse,
            nivel_desejado, tipo_contratacao_desejado, pretensao_salarial_min, pretensao_salarial_max,
            resumo_profissional, motivacao_esg, status, perfil_completo, aceita_contato
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            perfil["email"], perfil["nome_completo"], perfil["telefone"], perfil["linkedin_url"],
            perfil["localizacao_uf"], perfil["localizacao_cidade"], perfil["aceita_remoto"],
            perfil["disponivel_mudanca"], perfil["anos_experiencia_total"], perfil["anos_experiencia_esg"],
            perfil["cargo_atual"], perfil["empresa_atual"], perfil["formacao_nivel"], perfil["formacao_area"],
            perfil["instituicao"], perfil["ods_interesse"], perfil["ods_experiencia"], perfil["habilidades_esg"],
            perfil["certificacoes"], perfil["areas_interesse"], perfil["nivel_desejado"],
            perfil["tipo_contratacao_desejado"], perfil["pretensao_salarial_min"], perfil["pretensao_salarial_max"],
            perfil["resumo_profissional"], perfil["motivacao_esg"], "ativo", True, True
        ))
        
        conn.commit()
        return True
        
    except sqlite3.IntegrityError:
        return False  # Email já existe
    finally:
        conn.close()

def main():
    print("🌱 Gerando Profissionais da Área Ambiental - Green Jobs Brasil")
    print("=" * 70)
    print("📍 Foco: Profissionais ambientais para demonstração específica")
    print()
    
    # Limpar profissionais existentes se quiser recomeçar
    resposta = input("🗑️  Limpar profissionais existentes? (s/N): ").lower()
    if resposta == 's':
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profissionais_esg")
        conn.commit()
        conn.close()
        print("✅ Profissionais anteriores removidos")
    
    # Gerar profissionais ambientais
    num_profissionais = int(input("🔢 Quantos profissionais ambientais gerar? (padrão 50): ") or 50)
    
    sucessos = 0
    duplicados = 0
    
    print(f"\n🚀 Gerando {num_profissionais} profissionais ambientais...")
    
    for i in range(num_profissionais):
        perfil = gerar_perfil_ambiental()
        
        if inserir_profissional_ambiental(perfil):
            sucessos += 1
            print(f"✅ {i+1:2d}/{num_profissionais} - {perfil['nome_completo']:<25} | {perfil['cargo_atual']}")
        else:
            duplicados += 1
            print(f"⚠️  {i+1:2d}/{num_profissionais} - Email duplicado, pulando...")
    
    print("\n" + "=" * 70)
    print("🎉 GERAÇÃO CONCLUÍDA!")
    print(f"✅ Sucessos: {sucessos}")
    print(f"⚠️  Duplicados: {duplicados}")
    print(f"📊 Taxa de sucesso: {sucessos/(sucessos+duplicados)*100:.1f}%")
    print()
    print("🔗 Para ver os resultados:")
    print("   http://127.0.0.1:8000/profissionais")
    print("   http://127.0.0.1:8000/api/profissionais/?limit=100")

if __name__ == "__main__":
    main()