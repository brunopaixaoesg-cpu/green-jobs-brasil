#!/usr/bin/env python3
"""
Gerador de Vagas Ambientais Realísticas - Green Jobs Brasil
===========================================================
Cria vagas específicas da área ambiental com dados realísticos
baseados no mercado que você conhece.
"""

from scripts.db_wrapper import get_connection
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configurações
DATABASE_PATH = Path("gjb_dev.db")

# CNPJs de empresas que realmente contratam profissionais ambientais
EMPRESAS_AMBIENTAIS = {
    "33000167000101": "Vale S.A.",
    "33592510000154": "Petrobras",
    "43776517000103": "Sabesp",
    "40432544000147": "Copel",
    "17155730000164": "Cemig",
    "00001180000126": "Eletrobras",
    "16404287000155": "Suzano S.A.",
    "89637490000155": "Klabin S.A.",
    "02916265000160": "JBS S.A.",
    "01838723000127": "BRF S.A.",
    "17329485000159": "Ambev",
    "71673990000145": "Natura Cosméticos",
    "61082417000173": "BASF S.A.",
    "45990181000135": "3M do Brasil",
    "02467371000173": "EDP Brasil"
}

# Títulos de vagas realísticas da área ambiental
TITULOS_VAGAS_AMBIENTAIS = [
    "Analista Ambiental Júnior",
    "Analista Ambiental Pleno", 
    "Analista Ambiental Sênior",
    "Coordenador de Meio Ambiente",
    "Especialista em Licenciamento Ambiental",
    "Consultor Ambiental",
    "Engenheiro Ambiental",
    "Técnico em Meio Ambiente",
    "Analista de Recursos Hídricos",
    "Especialista em Gestão de Resíduos",
    "Analista de Monitoramento Ambiental",
    "Coordenador de Sustentabilidade",
    "Especialista em Mudanças Climáticas", 
    "Auditor Ambiental",
    "Gestor de EHS (Environment, Health & Safety)",
    "Analista de Impacto Ambiental",
    "Consultor ISO 14001",
    "Especialista em Biodiversidade",
    "Coordenador de Licenciamento",
    "Analista de Compliance Ambiental"
]

# Descrições detalhadas por tipo de vaga
DESCRICOES_AMBIENTAIS = {
    "analista": """Responsável por realizar análises ambientais, elaborar relatórios técnicos, acompanhar processos de licenciamento e monitorar o cumprimento da legislação ambiental. 

Principais atividades:
• Elaboração de estudos e relatórios ambientais
• Acompanhamento de licenças e condicionantes ambientais
• Monitoramento de indicadores de desempenho ambiental
• Apoio em auditorias e inspeções ambientais
• Interface com órgãos ambientais e consultores externos
• Análise de não-conformidades e proposição de ações corretivas""",

    "especialista": """Atuar como referência técnica na área ambiental, liderando projetos complexos e fornecendo expertise especializada para questões ambientais estratégicas da empresa.

Principais atividades:
• Desenvolvimento de estratégias e políticas ambientais
• Liderança de projetos de melhoria ambiental
• Gestão de stakeholders e relacionamento com órgãos reguladores
• Mentoria técnica para equipes júnior
• Análise de riscos ambientais e proposição de medidas mitigatórias
• Representação da empresa em comitês e fóruns setoriais""",

    "coordenador": """Liderar equipe multidisciplinar na gestão ambiental da empresa, garantindo o cumprimento da legislação e a melhoria contínua do desempenho ambiental.

Principais atividades:
• Coordenação de equipe de analistas ambientais
• Planejamento e execução de programas ambientais
• Gestão orçamentária da área ambiental
• Relacionamento com fornecedores e consultores especializados
• Elaboração de relatórios gerenciais e indicadores
• Condução de treinamentos e capacitação da equipe"""
}

# Requisitos técnicos por nível
REQUISITOS_AMBIENTAIS = {
    "junior": [
        "Formação superior em Engenharia Ambiental, Biologia, Geografia ou áreas afins",
        "Conhecimento da legislação ambiental brasileira",
        "Experiência com elaboração de relatórios técnicos",
        "Conhecimentos em SIG (Sistemas de Informação Geográfica) - desejável",
        "Inglês intermediário",
        "Disponibilidade para viagens"
    ],
    "pleno": [
        "Formação superior em Engenharia Ambiental, Biologia, Geografia ou áreas afins",
        "Especialização ou MBA na área ambiental - desejável",
        "Experiência mínima de 3 anos na área ambiental",
        "Conhecimento avançado da legislação ambiental",
        "Experiência com licenciamento ambiental",
        "Domínio de ferramentas de SIG e AutoCAD",
        "Inglês avançado",
        "Registro no conselho profissional (CREA, CRBio, etc.)"
    ],
    "senior": [
        "Formação superior em Engenharia Ambiental, Biologia, Geografia ou áreas afins",
        "Pós-graduação na área ambiental",
        "Experiência mínima de 7 anos na área ambiental",
        "Experiência em liderança de equipes",
        "Conhecimento aprofundado em EIA/RIMA",
        "Experiência com auditorias ambientais",
        "Certificações ISO 14001 - desejável",
        "Inglês fluente",
        "Registro ativo no conselho profissional"
    ]
}

# Habilidades específicas por área
HABILIDADES_ESPECIFICAS = {
    "licenciamento": ["EIA/RIMA", "Licenciamento Ambiental", "Legislação Ambiental", "Gestão de Stakeholders"],
    "recursos_hidricos": ["Recursos Hídricos", "Qualidade da Água", "Outorga", "Monitoramento Hidrológico"],
    "residuos": ["Gestão de Resíduos", "PNRS", "Logística Reversa", "Economia Circular"],
    "climaticas": ["Mudanças Climáticas", "Inventário GEE", "Pegada de Carbono", "Mercado de Carbono"],
    "biodiversidade": ["Biodiversidade", "Fauna", "Flora", "Unidades de Conservação"],
    "auditoria": ["Auditoria Ambiental", "ISO 14001", "Compliance", "Gestão de Riscos"]
}

# Benefícios típicos do setor
BENEFICIOS_AMBIENTAIS = [
    "Vale-refeição", "Vale-transporte", "Plano de saúde", "Plano odontológico",
    "Seguro de vida", "Previdência privada", "Participação nos lucros",
    "Auxílio educação", "Gimnásio/Academia", "Horário flexível",
    "Home office", "Treinamentos técnicos", "Certificações pagas pela empresa",
    "Carro da empresa (para viagens)", "Ajuda de custo para viagens"
]

# Using scripts.db_wrapper.get_connection() for DB access

def gerar_vaga_ambiental():
    """Gera uma vaga realística da área ambiental"""
    
    # Selecionar empresa
    cnpj, empresa = random.choice(list(EMPRESAS_AMBIENTAIS.items()))
    
    # Selecionar título
    titulo = random.choice(TITULOS_VAGAS_AMBIENTAIS)
    
    # Determinar nível baseado no título
    if "Júnior" in titulo or "Jr" in titulo or "Técnico" in titulo:
        nivel = "junior"
    elif "Coordenador" in titulo or "Especialista" in titulo or "Sênior" in titulo:
        nivel = "senior" if random.random() > 0.5 else "pleno"
    elif "Gerente" in titulo or "Diretor" in titulo:
        nivel = "especialista"
    else:
        nivel = random.choice(["junior", "pleno", "senior"])
    
    # Descrição baseada no tipo
    if "Analista" in titulo:
        descricao = DESCRICOES_AMBIENTAIS["analista"]
    elif "Especialista" in titulo or "Coordenador" in titulo:
        descricao = DESCRICOES_AMBIENTAIS["especialista"]
    elif "Coordenador" in titulo or "Gerente" in titulo:
        descricao = DESCRICOES_AMBIENTAIS["coordenador"]
    else:
        descricao = DESCRICOES_AMBIENTAIS["analista"]
    
    # Requisitos baseados no nível
    requisitos = "\n".join([f"• {req}" for req in REQUISITOS_AMBIENTAIS[nivel]])
    
    # Habilidades específicas
    area_foco = random.choice(list(HABILIDADES_ESPECIFICAS.keys()))
    habilidades = HABILIDADES_ESPECIFICAS[area_foco]
    habilidades_str = ", ".join(habilidades[:3])  # Pegar 3 habilidades principais
    
    # Salário realístico baseado no nível e região
    if nivel == "junior":
        salario_min = random.randint(3500, 5500)
        salario_max = salario_min + random.randint(1000, 2000)
    elif nivel == "pleno":
        salario_min = random.randint(6000, 9000)
        salario_max = salario_min + random.randint(2000, 3000)
    elif nivel == "senior":
        salario_min = random.randint(10000, 16000)
        salario_max = salario_min + random.randint(3000, 5000)
    else:  # especialista
        salario_min = random.randint(18000, 30000)
        salario_max = salario_min + random.randint(5000, 10000)
    
    # Localização (focar em estados com mais oportunidades)
    localizacoes = [
        ("SP", "São Paulo"), ("SP", "Campinas"), ("SP", "Santos"),
        ("RJ", "Rio de Janeiro"), ("RJ", "Niterói"),
        ("MG", "Belo Horizonte"), ("MG", "Contagem"),
        ("RS", "Porto Alegre"), ("PR", "Curitiba"),
        ("SC", "Florianópolis"), ("BA", "Salvador"),
        ("PE", "Recife"), ("CE", "Fortaleza")
    ]
    uf, cidade = random.choice(localizacoes)
    
    # Modalidade de trabalho
    modalidades = [
        (True, False),   # Remoto
        (False, True),   # Híbrido  
        (False, False)   # Presencial
    ]
    remoto, hibrido = random.choice(modalidades)
    
    # Tipo de contratação
    tipo_contrato = random.choice(["CLT", "PJ", "temporario"])
    
    # Benefícios
    num_beneficios = random.randint(5, 10)
    beneficios = random.sample(BENEFICIOS_AMBIENTAIS, num_beneficios)
    beneficios_str = "\n".join([f"• {ben}" for ben in beneficios])
    
    # ODS relacionados (área ambiental)
    ods_ambientais = [
        "ODS 6 - Água Limpa e Saneamento",
        "ODS 13 - Mudanças Climáticas", 
        "ODS 14 - Oceanos e Vida Marinha",
        "ODS 15 - Biodiversidade Terrestre"
    ]
    ods_selecionados = random.sample(ods_ambientais, random.randint(2, 4))
    ods_str = ", ".join(ods_selecionados)
    
    return {
        "cnpj": cnpj,
        "titulo": titulo,
        "descricao": descricao,
        "ods_tags": ods_str,
        "habilidades_requeridas": habilidades_str,
        "nivel_experiencia": nivel,
        "tipo_contratacao": tipo_contrato,
        "localizacao_uf": uf,
        "localizacao_cidade": cidade,
        "salario_min": float(salario_min),
        "salario_max": float(salario_max),
        "remoto": remoto,
        "hibrido": hibrido,
        "status": "ativa",
        "vagas_disponiveis": random.randint(1, 3),
        "beneficios": beneficios_str,
        "requisitos_adicionais": requisitos,
        "diferenciais": f"Trabalhar em {empresa}, empresa referência no setor. Oportunidade de atuar em projetos de grande impacto ambiental."
    }

def inserir_vaga_ambiental(vaga):
    """Insere vaga ambiental no banco de dados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO vagas_esg (
                cnpj, titulo, descricao, ods_tags, habilidades_requeridas,
                nivel_experiencia, tipo_contratacao, localizacao_uf, localizacao_cidade,
                salario_min, salario_max, remoto, hibrido, status, vagas_disponiveis,
                beneficios, requisitos_adicionais, diferenciais
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                vaga["cnpj"], vaga["titulo"], vaga["descricao"], vaga["ods_tags"],
                vaga["habilidades_requeridas"], vaga["nivel_experiencia"], vaga["tipo_contratacao"],
                vaga["localizacao_uf"], vaga["localizacao_cidade"], vaga["salario_min"],
                vaga["salario_max"], vaga["remoto"], vaga["hibrido"], vaga["status"],
                vaga["vagas_disponiveis"], vaga["beneficios"], vaga["requisitos_adicionais"],
                vaga["diferenciais"]
            ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir vaga: {e}")
            return False

def main():
    print("🌱 Gerando Vagas da Área Ambiental - Green Jobs Brasil")
    print("=" * 60)
    print("📍 Foco: Vagas ambientais em empresas reais do mercado")
    print()
    
    # Limpar vagas existentes se quiser recomeçar
    resposta = input("🗑️  Limpar vagas existentes? (s/N): ").lower()
    if resposta == 's':
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vagas_esg")
            conn.commit()
        print("✅ Vagas anteriores removidas")
    
    # Gerar vagas ambientais
    num_vagas = int(input("🔢 Quantas vagas ambientais gerar? (padrão 25): ") or 25)
    
    sucessos = 0
    erros = 0
    
    print(f"\n🚀 Gerando {num_vagas} vagas ambientais...")
    
    for i in range(num_vagas):
        vaga = gerar_vaga_ambiental()
        
        if inserir_vaga_ambiental(vaga):
            sucessos += 1
            empresa = EMPRESAS_AMBIENTAIS[vaga["cnpj"]]
            salario_display = f"R$ {vaga['salario_min']:,.0f} - R$ {vaga['salario_max']:,.0f}"
            print(f"✅ {i+1:2d}/{num_vagas} - {vaga['titulo']:<30}")
            print(f"      {empresa} | {vaga['localizacao_cidade']}-{vaga['localizacao_uf']} | {salario_display}")
        else:
            erros += 1
            print(f"❌ {i+1:2d}/{num_vagas} - Erro ao inserir vaga")
    
    print("\n" + "=" * 60)
    print("🎉 GERAÇÃO CONCLUÍDA!")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📊 Taxa de sucesso: {sucessos/(sucessos+erros)*100:.1f}%")
    print()
    print("🔗 Para ver os resultados:")
    print("   http://127.0.0.1:8000/vagas")
    print("   http://127.0.0.1:8000/api/vagas/")

if __name__ == "__main__":
    main()