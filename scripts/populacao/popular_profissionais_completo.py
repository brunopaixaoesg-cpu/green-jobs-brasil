import sys
import os
sys.path.append('api')

from sqlite_api_clean import get_db
import sqlite3
import random

def popular_profissionais_ambientais():
    """Popula o banco com 120+ profissionais das áreas ambientais"""
    print("🌱 Populando banco com profissionais ambientais...")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Dados base para gerar profissionais
    areas_atuacao = [
        "Biologia Ambiental", "Engenharia Florestal", "Engenharia Ambiental", 
        "Consultoria Ambiental", "Análise ESG", "Geoprocessamento",
        "Inventário Florestal", "Gestão Ambiental", "Sustentabilidade",
        "Ecologia", "Recursos Hídricos", "Mudanças Climáticas",
        "Licenciamento Ambiental", "Auditoria Ambiental", "SIG",
        "Sensoriamento Remoto", "Biomonitoramento", "Recuperação de Áreas",
        "Gestão de Resíduos", "Energia Renovável"
    ]
    
    cidades_sp = [
        "São Paulo", "Campinas", "Santos", "São José dos Campos", 
        "Ribeirão Preto", "Sorocaba", "São José do Rio Preto",
        "Piracicaba", "Bauru", "Jundiaí"
    ]
    
    cidades_outras = [
        "Rio de Janeiro", "Belo Horizonte", "Brasília", "Curitiba",
        "Porto Alegre", "Florianópolis", "Goiânia", "Salvador",
        "Recife", "Fortaleza", "Manaus", "Belém"
    ]
    
    ufs = ["SP", "RJ", "MG", "DF", "PR", "RS", "SC", "GO", "BA", "PE", "CE", "AM", "PA"]
    
    # Nomes fictícios mas realistas
    nomes_biologos = [
        "Ana Clara Silva", "Bruno Santos Oliveira", "Carla Mendes Costa",
        "Diego Ferreira Lima", "Elena Rodrigues", "Fernando Alves",
        "Gabriela Pereira", "Henrique Barbosa", "Isabela Martins",
        "João Paulo Nascimento", "Karina Souza", "Leonardo Torres",
        "Marina Campos", "Nicolas Ribeiro", "Olivia Castro"
    ]
    
    nomes_eng_florestais = [
        "André Floresta", "Beatriz Madeira", "Carlos Pinheiro",
        "Daniela Eucalipto", "Eduardo Bambu", "Fernanda Cedro",
        "Gustavo Ipê", "Helena Mogno", "Igor Jacarandá",
        "Julia Araucária", "Kevin Pau-brasil", "Laura Jequitibá"
    ]
    
    nomes_eng_ambientais = [
        "Alex Verde", "Bruna Sustentável", "Caio Renovável",
        "Débora Limpa", "Enzo Eficiente", "Flávia Ecológica",
        "Gabriel Consciente", "Heloísa Natural", "Ivan Sustento",
        "Júlia Ambiental", "Kaique Preserva", "Lívia Verde"
    ]
    
    nomes_consultores = [
        "Amanda Consultora", "Bernardo Assessor", "Camila Especialista",
        "Daniel Consultor", "Evelyn Auditora", "Fábio Perito",
        "Giovanna Avaliadora", "Humberto Analista", "Ingrid Técnica",
        "Juliano Especialista", "Kelly Consultora", "Luan Assessor"
    ]
    
    nomes_esg = [
        "Alice ESG", "Benjamin Sustentabilidade", "Carolina Impacto",
        "David Responsabilidade", "Emanuelle Governança", "Felipe Social",
        "Giovana Relatórios", "Hugo Compliance", "Isadora Métricas",
        "Jean Indicadores", "Katia Transparência", "Lucas Stakeholder"
    ]
    
    # Habilidades específicas por área
    habilidades_bio = [
        "Biomonitoramento", "Ecologia Aplicada", "Taxonomia", "Conservação",
        "Biodiversidade", "Biotecnologia", "Microbiologia Ambiental",
        "Ecotoxicologia", "Restauração Ecológica", "Fauna Silvestre"
    ]
    
    habilidades_eng_florestal = [
        "Inventário Florestal", "Manejo Florestal", "Silvicultura",
        "Dendrometria", "Melhoramento Genético", "Sistemas Agroflorestais",
        "Certificação Florestal", "Cadeia de Custódia", "LIDAR Florestal",
        "Modelagem Florestal"
    ]
    
    habilidades_geo = [
        "QGIS", "ArcGIS", "Google Earth Engine", "Python para GIS",
        "R Espacial", "ERDAS Imagine", "SNAP", "ENVI", "PostGIS",
        "FME", "Global Mapper", "GPS/GNSS", "Drone Mapping",
        "Machine Learning Espacial", "Análise Espacial"
    ]
    
    habilidades_esg = [
        "Relatórios GRI", "SASB", "TCFD", "CDP", "ISE B3",
        "Análise de Materialidade", "Due Diligence ESG", "Risk Assessment",
        "Stakeholder Engagement", "KPIs Sustentabilidade", "Carbon Footprint",
        "Life Cycle Assessment", "ESG Data Analytics", "Compliance Ambiental"
    ]
    
    try:
        profissionais_criados = 0
        
        # Criar biólogos (30)
        for i in range(30):
            nome = random.choice(nomes_biologos) + f" {i+1}"
            cidade = random.choice(cidades_sp + cidades_outras)
            uf = random.choice(ufs)
            exp = random.randint(1, 15)
            
            cursor.execute("""
                INSERT INTO profissionais_esg 
                (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                f"{nome.lower().replace(' ', '.')}@email.com",
                random.choice(areas_atuacao[:4]),  # Áreas mais biológicas
                exp,
                cidade,
                uf
            ))
            profissionais_criados += 1
        
        # Criar engenheiros florestais (25)
        for i in range(25):
            nome = random.choice(nomes_eng_florestais) + f" {i+1}"
            cidade = random.choice(cidades_sp + cidades_outras)
            uf = random.choice(ufs)
            exp = random.randint(2, 20)
            
            cursor.execute("""
                INSERT INTO profissionais_esg 
                (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                f"{nome.lower().replace(' ', '.')}@email.com",
                "Engenharia Florestal",
                exp,
                cidade,
                uf
            ))
            profissionais_criados += 1
        
        # Criar engenheiros ambientais (25)
        for i in range(25):
            nome = random.choice(nomes_eng_ambientais) + f" {i+1}"
            cidade = random.choice(cidades_sp + cidades_outras)
            uf = random.choice(ufs)
            exp = random.randint(1, 18)
            
            cursor.execute("""
                INSERT INTO profissionais_esg 
                (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                f"{nome.lower().replace(' ', '.')}@email.com",
                "Engenharia Ambiental",
                exp,
                cidade,
                uf
            ))
            profissionais_criados += 1
        
        # Criar consultores ambientais (20)
        for i in range(20):
            nome = random.choice(nomes_consultores) + f" {i+1}"
            cidade = random.choice(cidades_sp + cidades_outras)
            uf = random.choice(ufs)
            exp = random.randint(3, 25)
            
            cursor.execute("""
                INSERT INTO profissionais_esg 
                (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                f"{nome.lower().replace(' ', '.')}@email.com",
                "Consultoria Ambiental",
                exp,
                cidade,
                uf
            ))
            profissionais_criados += 1
        
        # Criar analistas ESG (20)
        for i in range(20):
            nome = random.choice(nomes_esg) + f" {i+1}"
            cidade = random.choice(cidades_sp + cidades_outras)
            uf = random.choice(ufs)
            exp = random.randint(1, 12)
            
            cursor.execute("""
                INSERT INTO profissionais_esg 
                (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                f"{nome.lower().replace(' ', '.')}@email.com",
                "Análise ESG",
                exp,
                cidade,
                uf
            ))
            profissionais_criados += 1
        
        conn.commit()
        print(f"✅ {profissionais_criados} profissionais ambientais criados!")
        
        # Verificar resultado
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        total = cursor.fetchone()[0]
        print(f"📊 Total de profissionais no banco: {total}")
        
        # Mostrar estatísticas por área
        cursor.execute("""
            SELECT area_atuacao, COUNT(*) as total 
            FROM profissionais_esg 
            GROUP BY area_atuacao 
            ORDER BY total DESC
        """)
        stats = cursor.fetchall()
        print("\n📈 Profissionais por área:")
        for area, count in stats:
            print(f"   {area}: {count}")
        
    except Exception as e:
        print(f"❌ Erro ao popular profissionais: {e}")
        conn.rollback()
    finally:
        conn.close()

def popular_empresas_e_vagas():
    """Popula empresas e vagas de exemplo"""
    print("\n🏢 Populando empresas e vagas...")
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Empresa 1 - Green Tech
        cursor.execute("""
            INSERT INTO empresas_esg 
            (cnpj, razao_social, nome_fantasia, email, senha_hash, telefone, website, 
             descricao, score_verde, ods_tags, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '60.331.021/0001-11',
            'GREEN TECH SOLUTIONS LTDA',
            'Green Tech Solutions',
            'contato@greentech.com.br',
            'hash123',
            '(11) 98765-4321',
            'https://greentech.com.br',
            'Empresa focada em soluções sustentáveis e tecnologia verde',
            95.0,
            'ODS 7,ODS 9,ODS 11',
            'ativa'
        ))
        
        # Empresa 2 - EcoConsult
        cursor.execute("""
            INSERT INTO empresas_esg 
            (cnpj, razao_social, nome_fantasia, email, senha_hash, telefone, website, 
             descricao, score_verde, ods_tags, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '12.345.678/0001-90',
            'ECOCONSULT AMBIENTAL LTDA',
            'EcoConsult',
            'rh@ecoconsult.com.br',
            'hash456',
            '(11) 91234-5678',
            'https://ecoconsult.com.br',
            'Consultoria especializada em licenciamento e estudos ambientais',
            88.0,
            'ODS 6,ODS 14,ODS 15',
            'ativa'
        ))
        
        # Vagas para Green Tech
        vagas_greentech = [
            ('Analista de Sustentabilidade Jr', 'Análise de dados ESG e elaboração de relatórios de sustentabilidade', 'junior', 'clt', 'São Paulo', 'SP', 0, 4000, 6000),
            ('Coordenador de ESG', 'Coordenação de projetos ESG e relatórios de sustentabilidade', 'pleno', 'clt', 'São Paulo', 'SP', 1, 7000, 10000),
            ('Especialista em GIS', 'Desenvolvimento de projetos de geoprocessamento e análise espacial', 'senior', 'clt', 'Campinas', 'SP', 0, 8000, 12000)
        ]
        
        for titulo, desc, nivel, tipo, cidade, uf, remoto, sal_min, sal_max in vagas_greentech:
            cursor.execute("""
                INSERT INTO vagas 
                (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, 
                 localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (titulo, desc, '60.331.021/0001-11', nivel, tipo, cidade, uf, remoto, 'ativa', sal_min, sal_max))
        
        # Vagas para EcoConsult
        vagas_ecoconsult = [
            ('Biólogo Ambiental', 'Elaboração de estudos de fauna e flora para licenciamento ambiental', 'pleno', 'clt', 'Rio de Janeiro', 'RJ', 0, 6000, 8500),
            ('Engenheiro Florestal', 'Inventários florestais e planos de manejo sustentável', 'senior', 'clt', 'Belo Horizonte', 'MG', 0, 9000, 13000),
            ('Consultor Ambiental', 'Consultoria em licenciamento e compliance ambiental', 'senior', 'pj', 'São Paulo', 'SP', 1, 12000, 18000)
        ]
        
        for titulo, desc, nivel, tipo, cidade, uf, remoto, sal_min, sal_max in vagas_ecoconsult:
            cursor.execute("""
                INSERT INTO vagas 
                (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, 
                 localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (titulo, desc, '12.345.678/0001-90', nivel, tipo, cidade, uf, remoto, 'ativa', sal_min, sal_max))
        
        conn.commit()
        print("✅ Empresas e vagas criadas!")
        
        # Verificar vagas criadas
        cursor.execute("SELECT COUNT(*) FROM vagas")
        total_vagas = cursor.fetchone()[0]
        print(f"📊 Total de vagas: {total_vagas}")
        
    except Exception as e:
        print(f"❌ Erro ao criar empresas/vagas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🌱 POPULANDO BANCO GREEN JOBS BRASIL")
    print("=" * 50)
    
    popular_profissionais_ambientais()
    popular_empresas_e_vagas()
    
    print("\n🎉 Banco populado com sucesso!")
    print("📋 Resumo:")
    print("   • 120 profissionais ambientais")
    print("   • 2 empresas exemplo")
    print("   • 6 vagas ESG/ambientais")
    print("   • Foco: Bio, Eng. Florestal, Eng. Ambiental, ESG, GIS")