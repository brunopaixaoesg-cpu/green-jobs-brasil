"""
Migration: Adicionar campos de storytelling completo e imagens
Data: 2025-11-01
Objetivo: Adicionar campos foto_perfil_url, banner_url e outros campos storytelling
"""
import sqlite3
import sys
from pathlib import Path

# Adicionar api ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.db import get_db

def run_migration():
    """Executar migration"""
    print("🔧 Iniciando migration: add_storytelling_images\n")
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Verificar se campos já existem
        cursor.execute("PRAGMA table_info(profissionais_esg)")
        existing_cols = [col[1] for col in cursor.fetchall()]
        
        # Lista de campos para adicionar
        campos_para_adicionar = {
            'foto_perfil_url': 'TEXT',
            'banner_url': 'TEXT',
            'linkedin_url': 'TEXT',
            'portfolio_url': 'TEXT',
            'nome_completo': 'TEXT',
            'telefone': 'TEXT',
            'aceita_remoto': 'BOOLEAN DEFAULT 1',
            'disponivel_mudanca': 'BOOLEAN DEFAULT 0',
            'anos_experiencia_total': 'INTEGER',
            'anos_experiencia_esg': 'INTEGER',
            'cargo_atual': 'TEXT',
            'empresa_atual': 'TEXT',
            'formacao_nivel': 'TEXT',
            'formacao_area': 'TEXT',
            'instituicao': 'TEXT',
            'ods_interesse': 'TEXT',
            'ods_experiencia': 'TEXT',
            'habilidades_esg': 'TEXT',
            'certificacoes': 'TEXT',
            'areas_interesse': 'TEXT',
            'nivel_desejado': 'TEXT',
            'tipo_contratacao_desejado': 'TEXT',
            'pretensao_salarial_min': 'REAL',
            'pretensao_salarial_max': 'REAL',
            'curriculo_url': 'TEXT',
            'carta_apresentacao': 'TEXT',
            'resumo_profissional': 'TEXT',
            'motivacao_esg': 'TEXT',
            'perfil_completo': 'BOOLEAN DEFAULT 0',
            'aceita_contato': 'BOOLEAN DEFAULT 1',
            'disponibilidade': 'TEXT',
            'visualizacoes_perfil': 'INTEGER DEFAULT 0',
            'candidaturas_enviadas': 'INTEGER DEFAULT 0',
            'matches_recebidos': 'INTEGER DEFAULT 0',
            'ultimo_acesso': 'TIMESTAMP',
            'historia_verde': 'TEXT',
            'valores_pessoais': 'TEXT',
            'objetivos_carreira': 'TEXT',
            'conquistas_json': 'TEXT',
            'portfolio_projetos_json': 'TEXT',
            'redes_sociais_json': 'TEXT',
            'idiomas_json': 'TEXT',
            'voluntariado_json': 'TEXT',
            'publicacoes_json': 'TEXT'
        }
        
        # Adicionar campos faltantes
        campos_adicionados = []
        for campo, tipo in campos_para_adicionar.items():
            if campo not in existing_cols:
                print(f"  ➕ Adicionando campo: {campo} ({tipo})")
                cursor.execute(f"ALTER TABLE profissionais_esg ADD COLUMN {campo} {tipo}")
                campos_adicionados.append(campo)
            else:
                print(f"  ✓ Campo já existe: {campo}")
        
        conn.commit()
        
        print(f"\n✅ Migration concluída!")
        print(f"   📊 {len(campos_adicionados)} novos campos adicionados")
        print(f"   📊 {len(existing_cols)} campos já existiam")
        print(f"   📊 {len(existing_cols) + len(campos_adicionados)} campos totais")
        
        # Verificar resultado
        cursor.execute("PRAGMA table_info(profissionais_esg)")
        final_cols = cursor.fetchall()
        print(f"\n📋 Estrutura final da tabela profissionais_esg:")
        print(f"   Total de colunas: {len(final_cols)}")
        
        # Mostrar campos de imagem
        print(f"\n📸 Campos de imagem adicionados:")
        image_cols = [col for col in final_cols if any(x in col[1].lower() for x in ['foto', 'banner', 'url'])]
        for col in image_cols:
            print(f"   ✓ {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erro na migration: {str(e)}")
        conn.rollback()
        conn.close()
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
