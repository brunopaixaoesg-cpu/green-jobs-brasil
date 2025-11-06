"""
Script para popular banco com dados demo realistas para Dashboard de KPIs
Cria profissionais, empresas, vagas e candidaturas com histórico
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker('pt_BR')

# Conectar ao banco
DB_PATH = 'api/gjb_dev.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ODS disponíveis
ODS_LIST = [
    "ODS 7 - Energia Limpa",
    "ODS 8 - Trabalho Decente",
    "ODS 9 - Indústria e Inovação",
    "ODS 11 - Cidades Sustentáveis",
    "ODS 12 - Consumo Responsável",
    "ODS 13 - Ação Climática",
    "ODS 15 - Vida Terrestre"
]

# CNAEs verdes exemplo
CNAES_VERDES = [
    "35.11-5-01",  # Energia solar
    "35.11-5-02",  # Energia eólica
    "38.11-4-00",  # Reciclagem
    "71.12-0-00",  # Consultoria ambiental
    "01.61-0-01"   # Agricultura sustentável
]

UFS = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "DF"]
CIDADES_SP = ["São Paulo", "Campinas", "Santos", "São José dos Campos", "Ribeirão Preto"]
CIDADES_RJ = ["Rio de Janeiro", "Niterói", "Petrópolis", "Nova Friburgo"]

def limpar_dados_antigos():
    """Remove dados demo anteriores"""
    print("🧹 Limpando dados demo antigos...")
    cursor.execute("DELETE FROM candidaturas WHERE id > 0")
    cursor.execute("DELETE FROM vagas WHERE id > 0")
    cursor.execute("DELETE FROM profissionais_esg WHERE id > 5")  # Mantém os 5 primeiros
    # Verificar se tabela empresas_esg existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='empresas_esg'")
    if cursor.fetchone():
        cursor.execute("DELETE FROM empresas_esg WHERE id > 0")
    conn.commit()
    print("✅ Dados antigos removidos")

def criar_profissionais(quantidade=25):
    """Cria profissionais com perfis variados"""
    print(f"\n👥 Criando {quantidade} profissionais...")
    
    areas = [
        "Energia Renovável", "Gestão Ambiental", "Sustentabilidade",
        "Economia Circular", "ESG", "Agricultura Sustentável",
        "Consultoria Ambiental", "Engenharia Ambiental", "Reciclagem"
    ]
    
    niveis = ["Júnior", "Pleno", "Sênior", "Especialista", "Coordenador"]
    cargos = ["Analista", "Coordenador", "Especialista", "Consultor", "Gerente"]
    
    profissionais_ids = []
    
    for i in range(quantidade):
        nome = fake.name()
        email = fake.email()
        telefone = fake.phone_number()
        uf = random.choice(UFS)
        cidade = random.choice(CIDADES_SP if uf == "SP" else CIDADES_RJ if uf == "RJ" else [fake.city()])
        
        # Experiência (1-15 anos)
        anos_experiencia = random.randint(1, 15)
        anos_esg = random.randint(1, min(anos_experiencia, 10))
        
        # Selecionar 2-4 ODS
        ods_selecionados = random.sample(ODS_LIST, k=random.randint(2, 4))
        ods_str = ", ".join(ods_selecionados)
        
        # Área de atuação
        area = random.choice(areas)
        nivel = random.choice(niveis)
        cargo = random.choice(cargos)
        
        # Datas (criados nos últimos 60 dias)
        dias_atras = random.randint(1, 60)
        data_cadastro = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Status ativo (80% ativos)
        status = "ativo" if random.random() < 0.8 else "inativo"
        
        # Salário
        pretensao_min = random.randint(3000, 10000)
        pretensao_max = pretensao_min + random.randint(2000, 5000)
        
        cursor.execute("""
            INSERT INTO profissionais_esg (
                nome, email, telefone, 
                localizacao_uf, localizacao_cidade,
                area_atuacao, anos_experiencia_total, anos_experiencia_esg,
                ods_interesse, nivel_desejado, cargo_atual,
                pretensao_salarial_min, pretensao_salarial_max,
                created_at, status, aceita_remoto,
                resumo_profissional
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, email, telefone, uf, cidade, area, anos_experiencia, anos_esg,
              ods_str, nivel, cargo, pretensao_min, pretensao_max,
              data_cadastro, status, True,
              f"Profissional de {area} com {anos_experiencia} anos de experiência."))
        
        profissionais_ids.append(cursor.lastrowid)
    
    conn.commit()
    print(f"✅ {quantidade} profissionais criados")
    return profissionais_ids

def criar_empresas(quantidade=18):
    """Cria empresas com perfis variados"""
    print(f"\n🏢 Criando {quantidade} empresas...")
    
    setores = [
        "Energia Renovável", "Reciclagem", "Consultoria",
        "Indústria Verde", "Agricultura Sustentável", "Tecnologia Limpa"
    ]
    
    empresas_ids = []
    
    for i in range(quantidade):
        # CNPJ fake
        cnpj = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
        
        razao_social = f"{fake.company()} {random.choice(['Ltda', 'S.A.', 'EIRELI'])}"
        nome_fantasia = razao_social.split()[0]
        
        # Score verde (40-100)
        score_verde = random.randint(40, 100)
        
        # ODS (1-3)
        ods_selecionados = random.sample(ODS_LIST, k=random.randint(1, 3))
        ods_str = ", ".join(ods_selecionados)
        
        # Data cadastro (últimos 90 dias)
        dias_atras = random.randint(1, 90)
        data_cadastro = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Situação cadastral (95% ativas)
        status = "ativa" if random.random() < 0.95 else "inativa"
        
        # Email único
        email = f"contato{i}@{nome_fantasia.lower().replace(' ', '').replace('-', '')}esg.com.br"
        
        cursor.execute("""
            INSERT INTO empresas_esg (
                cnpj, razao_social, nome_fantasia, email,
                score_verde, ods_tags, status, data_cadastro, created_at,
                descricao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cnpj, razao_social, nome_fantasia, email,
              score_verde, ods_str, status, data_cadastro, data_cadastro,
              f"Empresa especializada em {random.choice(setores)}"))
        
        empresas_ids.append(cursor.lastrowid)
    
    conn.commit()
    print(f"✅ {quantidade} empresas criadas")
    return empresas_ids

def criar_vagas(empresas_ids, quantidade=35):
    """Cria vagas com status variados"""
    print(f"\n💼 Criando {quantidade} vagas...")
    
    titulos = [
        "Analista de Sustentabilidade",
        "Coordenador ESG",
        "Especialista em Energia Solar",
        "Gerente de Meio Ambiente",
        "Consultor Ambiental",
        "Engenheiro de Energia Renovável",
        "Analista de Economia Circular",
        "Técnico em Reciclagem",
        "Especialista em Carbono Zero",
        "Coordenador de Projetos Sustentáveis"
    ]
    
    tipos_contratacao = ["CLT", "PJ", "Híbrido"]
    niveis = ["Júnior", "Pleno", "Sênior", "Especialista"]
    
    vagas_ids = []
    
    # Buscar CNPJs das empresas criadas
    cursor.execute("SELECT id, cnpj FROM empresas_esg WHERE id IN ({})".format(
        ','.join('?' * len(empresas_ids))), empresas_ids)
    empresas_cnpjs = dict(cursor.fetchall())
    
    for i in range(quantidade):
        empresa_id = random.choice(empresas_ids)
        cnpj = empresas_cnpjs.get(empresa_id, "00.000.000/0001-00")
        
        titulo = random.choice(titulos)
        descricao = f"Vaga para {titulo} com experiência em projetos sustentáveis e ESG."
        
        # Salário (3k-15k)
        salario_min = random.randint(3000, 8000)
        salario_max = salario_min + random.randint(2000, 7000)
        
        tipo_contratacao = random.choice(tipos_contratacao)
        nivel = random.choice(niveis)
        
        # Localização
        uf = random.choice(UFS)
        cidade = random.choice(CIDADES_SP if uf == "SP" else [fake.city()])
        
        # Remoto
        remoto = random.random() < 0.4  # 40% remotas
        
        # Data publicação (últimos 45 dias)
        dias_atras = random.randint(1, 45)
        data_publicacao = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Status (60% abertas, 40% fechadas)
        status = "aberta" if random.random() < 0.6 else "fechada"
        
        cursor.execute("""
            INSERT INTO vagas (
                cnpj, titulo, descricao, salario_min, salario_max,
                tipo_contratacao, nivel_experiencia,
                localizacao_uf, localizacao_cidade, remoto,
                created_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cnpj, titulo, descricao, salario_min, salario_max,
              tipo_contratacao, nivel, uf, cidade, remoto,
              data_publicacao, status))
        
        vagas_ids.append(cursor.lastrowid)
    
    conn.commit()
    print(f"✅ {quantidade} vagas criadas")
    return vagas_ids

def criar_candidaturas(profissionais_ids, vagas_ids, quantidade=80):
    """Cria candidaturas com histórico"""
    print(f"\n🤝 Criando {quantidade} candidaturas...")
    
    status_opcoes = ["pendente", "em analise", "aceita", "recusada"]
    
    candidaturas_criadas = 0
    
    # Buscar emails dos profissionais
    cursor.execute("SELECT id, nome, email, telefone FROM profissionais_esg WHERE id IN ({})".format(
        ','.join('?' * len(profissionais_ids))), profissionais_ids)
    profissionais_data = {row[0]: (row[1], row[2], row[3]) for row in cursor.fetchall()}
    
    for i in range(quantidade):
        profissional_id = random.choice(profissionais_ids)
        vaga_id = random.choice(vagas_ids)
        
        # Verificar se candidatura já existe
        cursor.execute("""
            SELECT id FROM candidaturas 
            WHERE email = ? AND vaga_id = ?
        """, (profissionais_data[profissional_id][1], vaga_id))
        
        if cursor.fetchone():
            continue  # Pular se já existe
        
        nome, email, telefone = profissionais_data[profissional_id]
        
        # Status (mais pendentes e em análise)
        status = random.choices(
            status_opcoes,
            weights=[0.3, 0.3, 0.2, 0.2]  # 30% pendente, 30% em análise, 20% aceita, 20% recusada
        )[0]
        
        # Data candidatura (últimos 60 dias)
        dias_atras = random.randint(1, 60)
        data_candidatura = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO candidaturas (
                vaga_id, nome, email, telefone, status, data_candidatura,
                curriculo
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (vaga_id, nome, email, telefone, status, data_candidatura,
              f"Currículo de {nome}"))
        
        candidaturas_criadas += 1
    
    conn.commit()
    print(f"✅ {candidaturas_criadas} candidaturas criadas")

def exibir_resumo():
    """Exibe resumo dos dados criados"""
    print("\n" + "="*60)
    print("📊 RESUMO DOS DADOS CRIADOS")
    print("="*60)
    
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
    total_prof = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM profissionais_esg WHERE status = 'ativo'")
    ativos_prof = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM empresas_esg")
    total_emp = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM empresas_esg WHERE status = 'ativa'")
    ativas_emp = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vagas")
    total_vagas = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM vagas WHERE status = 'aberta'")
    abertas_vagas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM candidaturas")
    total_cand = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE status = 'aceita'")
    aceitas_cand = cursor.fetchone()[0]
    
    print(f"\n👥 Profissionais: {total_prof} ({ativos_prof} ativos)")
    print(f"🏢 Empresas: {total_emp} ({ativas_emp} ativas)")
    print(f"💼 Vagas: {total_vagas} ({abertas_vagas} abertas)")
    print(f"🤝 Candidaturas: {total_cand} ({aceitas_cand} aceitas)")
    
    if total_cand > 0 and total_vagas > 0:
        taxa_match = (aceitas_cand / total_cand) * 100
        print(f"\n📈 Taxa de Match: {taxa_match:.1f}%")
    
    print("\n✅ Dashboard pronto para visualização!")
    print("🔗 Acesse: http://127.0.0.1:8002/kpis")
    print("="*60)

if __name__ == "__main__":
    try:
        print("🚀 Iniciando população do banco de dados...\n")
        
        # Instalar faker se necessário
        try:
            from faker import Faker
        except ImportError:
            print("📦 Instalando biblioteca Faker...")
            os.system("pip install faker")
            from faker import Faker
        
        limpar_dados_antigos()
        
        profissionais_ids = criar_profissionais(25)
        empresas_ids = criar_empresas(18)
        vagas_ids = criar_vagas(empresas_ids, 35)
        criar_candidaturas(profissionais_ids, vagas_ids, 80)
        
        exibir_resumo()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
