import sqlite3
import json

DATABASE_PATH = "gjb_dev.db"

def test_listar_vagas():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query base
        query = """
            SELECT v.*, e.razao_social as empresa_nome
            FROM vagas_esg v
            LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
            WHERE 1=1
        """
        params = []
        
        # Ordenar por mais recentes
        query += " ORDER BY v.criada_em DESC"
        query += " LIMIT ? OFFSET ?"
        params.extend([50, 0])
        
        print("=== EXECUTANDO QUERY ===")
        print(query)
        print(f"Params: {params}")
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        print(f"\n✅ Query executada! {len(rows)} vagas encontradas\n")
        
        vagas = []
        for row in rows:
            vaga_dict = dict(row)
            
            print(f"Processando vaga ID {vaga_dict['id']}: {vaga_dict['titulo']}")
            
            # Parse JSON fields
            print(f"  ods_tags antes: {vaga_dict['ods_tags']} (tipo: {type(vaga_dict['ods_tags'])})")
            vaga_dict['ods_tags'] = json.loads(vaga_dict['ods_tags']) if vaga_dict['ods_tags'] else []
            print(f"  ods_tags depois: {vaga_dict['ods_tags']}")
            
            print(f"  habilidades_requeridas antes: {vaga_dict['habilidades_requeridas']}")
            vaga_dict['habilidades_requeridas'] = json.loads(vaga_dict['habilidades_requeridas']) if vaga_dict['habilidades_requeridas'] else []
            print(f"  habilidades_requeridas depois: {vaga_dict['habilidades_requeridas']}")
            
            vagas.append(vaga_dict)
        
        conn.close()
        
        print(f"\n✅ SUCESSO! {len(vagas)} vagas processadas")
        print("\nPrimeira vaga:")
        print(json.dumps(vagas[0], indent=2, default=str))
        
        return vagas
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_listar_vagas()
