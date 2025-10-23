"""
Script alternativo para popular dados via SQL direto
Conecta no PostgreSQL e insere dados de demonstração
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# URL do PostgreSQL do Render (você precisa fornecer)
DATABASE_URL = "postgresql://green_jobs_brasil_user:vUdJkMbqEqc7lw4FPOHDTNTQRhF5tLm5@dpg-csnkcubqf0us73c6bklg-a.oregon-postgres.render.com/green_jobs_brasil"

def populate_postgresql():
    """Popula PostgreSQL diretamente"""
    
    try:
        # Conectar ao PostgreSQL com SSL
        conn = psycopg2.connect(DATABASE_URL + "?sslmode=require", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("✅ Conectado ao PostgreSQL do Render")
        
        # Limpar dados anteriores
        try:
            cursor.execute("DELETE FROM vagas")
            cursor.execute("DELETE FROM empresas_esg") 
            cursor.execute("DELETE FROM profissionais_esg")
            conn.commit()
            print("🧹 Dados antigos removidos")
        except Exception as e:
            print(f"⚠️ Aviso na limpeza: {e}")
            conn.rollback()
        
        # Dados de profissionais
        profissionais = [
            ("Maria Silva", "maria@email.com", "Energia Solar", 5, "São Paulo", "SP"),
            ("João Santos", "joao@email.com", "Sustentabilidade", 3, "Rio de Janeiro", "RJ"),
            ("Ana Costa", "ana@email.com", "Gestão Ambiental", 7, "Belo Horizonte", "MG"),
            ("Carlos Lima", "carlos@email.com", "Energia Eólica", 4, "Fortaleza", "CE"),
            ("Lucia Fernandes", "lucia@email.com", "Reciclagem", 6, "Porto Alegre", "RS")
        ]
        
        profissional_ids = []
        for prof in profissionais:
            cursor.execute("""
                INSERT INTO profissionais_esg (nome, email, area_atuacao, experiencia_anos, localizacao_cidade, localizacao_uf)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, prof)
            prof_id = cursor.fetchone()[0]
            profissional_ids.append(prof_id)
        
        print(f"✅ {len(profissionais)} profissionais inseridos")
        
        # Dados de empresas
        empresas = [
            ("EcoTech Solutions", "12345678000123", "Tecnologia Verde", 85, "São Paulo", "SP"),
            ("Verde Energia Ltda", "98765432000156", "Energia Renovável", 92, "Rio de Janeiro", "RJ"),
            ("Sustenta Brasil SA", "11122233000144", "Consultoria ESG", 78, "Brasília", "DF")
        ]
        
        empresa_ids = []
        for emp in empresas:
            cursor.execute("""
                INSERT INTO empresas_esg (nome, cnpj, setor, score_verde, cidade, uf)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, emp)
            emp_id = cursor.fetchone()[0]
            empresa_ids.append(emp_id)
        
        print(f"✅ {len(empresas)} empresas inseridas")
        
        # Dados de vagas
        vagas = [
            ("Analista de Sustentabilidade", "Analista para projetos ESG", empresa_ids[0], "São Paulo", "SP", "CLT", False, 5500.00),
            ("Engenheiro(a) de Energia Solar", "Desenvolvimento de projetos solares", empresa_ids[1], "Rio de Janeiro", "RJ", "CLT", True, 7200.00),
            ("Consultor(a) Ambiental", "Consultoria em gestão ambiental", empresa_ids[2], "Brasília", "DF", "PJ", True, 8500.00),
            ("Especialista em ESG", "Implementação de práticas ESG", empresa_ids[0], "São Paulo", "SP", "CLT", False, 9200.00),
            ("Técnico(a) em Energia Eólica", "Manutenção de turbinas eólicas", empresa_ids[1], "Fortaleza", "CE", "CLT", False, 4800.00)
        ]
        
        for vaga in vagas:
            cursor.execute("""
                INSERT INTO vagas (titulo, descricao, empresa_id, localizacao_cidade, localizacao_uf, tipo_contrato, remoto, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, vaga)
        
        print(f"✅ {len(vagas)} vagas inseridas")
        
        conn.commit()
        conn.close()
        
        print("🎉 DADOS POPULADOS COM SUCESSO!")
        print(f"📊 Total: {len(profissionais)} profissionais, {len(empresas)} empresas, {len(vagas)} vagas")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    populate_postgresql()