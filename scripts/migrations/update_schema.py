from scripts.db_wrapper import get_connection

try:
    with get_connection() as conn:
        cursor = conn.cursor()
        # Adicionar colunas que estão faltando
        print("Adicionando colunas faltantes...")

        # Verificar se a coluna já existe antes de adicionar
        cursor.execute("PRAGMA table_info(empresas_esg)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        columns_to_add = [
            ('website', 'TEXT'),
            ('ods_tags', 'TEXT'),
            ('score_verde', 'REAL DEFAULT 0')
        ]

        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE empresas_esg ADD COLUMN {column_name} {column_type}")
                    print(f"✅ Coluna {column_name} adicionada")
                except Exception as e:
                    print(f"⚠️ Erro ao adicionar {column_name}: {e}")
            else:
                print(f"ℹ️ Coluna {column_name} já existe")

        conn.commit()

        print("\n=== ESTRUTURA ATUALIZADA ===")
        cursor.execute("PRAGMA table_info(empresas_esg)")
        cols = cursor.fetchall()
        for col in cols:
            print(f"  • {col[1]} ({col[2]})")

    print("\n✅ Script concluído!")
except Exception as e:
    print(f"Erro: {e}")