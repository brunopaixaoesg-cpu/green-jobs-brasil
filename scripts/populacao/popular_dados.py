from scripts.db_wrapper import get_connection
import os

def popular_dados_exemplo():
    """Popula o banco com dados de exemplo"""
    print("📊 Populando banco com dados de exemplo...")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            # Empresa exemplo
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
                'hash123',  # Em produção usar hash real
                '(11) 98765-4321',
                'https://greentech.com.br',
                'Empresa focada em soluções sustentáveis e tecnologia verde',
                95.0,
                'ODS 7,ODS 9,ODS 11',
                'ativa'
            ))

            empresa_id = cursor.lastrowid
            print(f"✅ Empresa criada com ID: {empresa_id}")

            # Vaga exemplo
            cursor.execute("""
                INSERT INTO vagas 
                (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, 
                 localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'Analista de Sustentabilidade Jr',
                'Vaga para profissional júnior em ESG com foco em relatórios de sustentabilidade',
                '60.331.021/0001-11',
                'junior',
                'clt',
                'São Paulo',
                'SP',
                0,
                'ativa',
                4000.0,
                6000.0
            ))

            vaga_id = cursor.lastrowid
            print(f"✅ Vaga criada com ID: {vaga_id}")

            # Segunda vaga
            cursor.execute("""
                INSERT INTO vagas 
                (titulo, descricao, cnpj, nivel_experiencia, tipo_contratacao, 
                 localizacao_cidade, localizacao_uf, remoto, status, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'Coordenador de ESG',
                'Coordenação de projetos ESG e relatórios de sustentabilidade para clientes',
                '60.331.021/0001-11',
                'pleno',
                'clt',
                'São Paulo',
                'SP',
                1,  # Remoto
                'ativa',
                7000.0,
                10000.0
            ))

            vaga_id2 = cursor.lastrowid
            print(f"✅ Segunda vaga criada com ID: {vaga_id2}")

            conn.commit()
            print("🎉 Dados populados com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao popular dados: {e}")
            conn.rollback()

    # connection closed by context manager

if __name__ == "__main__":
    popular_dados_exemplo()