#!/usr/bin/env python3
"""
Extração e preparação de dados para Machine Learning
Processar candidaturas existentes para criar dataset de treinamento
"""

import sqlite3
import pandas as pd
import numpy as np
import json
from datetime import datetime
import re

def extrair_dados_ml():
    """Extrair e processar dados das candidaturas para ML"""
    
    print("🤖 Preparando dados para Machine Learning...")
    
    conn = sqlite3.connect('gjb_dev.db')
    
    # Query complexa para extrair todos os dados relevantes
    query = """
    SELECT 
        c.id as candidatura_id,
        c.profissional_id,
        c.vaga_id,
        c.status,
        c.compatibilidade_score,
        c.data_candidatura,
        
        -- Dados do profissional
        p.nome_completo,
        p.cargo_atual,
        p.anos_experiencia_esg,
        p.localizacao_uf as prof_uf,
        p.aceita_remoto,
        p.pretensao_salarial_min,
        p.pretensao_salarial_max,
        p.habilidades_esg,
        p.ods_interesse,
        p.disponibilidade,
        
        -- Dados da vaga
        v.titulo as vaga_titulo,
        v.nivel_experiencia,
        v.localizacao_uf as vaga_uf,
        v.localizacao_cidade,
        v.salario_min,
        v.salario_max,
        v.remoto,
        v.hibrido,
        v.habilidades_requeridas,
        v.ods_tags,
        v.tipo_contratacao,
        v.status as vaga_status
        
    FROM candidaturas_esg c
    JOIN profissionais_esg p ON c.profissional_id = p.id
    JOIN vagas_esg v ON c.vaga_id = v.id
    ORDER BY c.data_candidatura DESC
    """
    
    print("📊 Extraindo dados do banco...")
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"✅ {len(df)} candidaturas extraídas")
    
    # Processar features
    df_processed = processar_features(df)
    
    # Salvar dataset
    df_processed.to_csv('data/processed/ml_dataset.csv', index=False)
    print(f"💾 Dataset salvo em data/processed/ml_dataset.csv")
    
    # Estatísticas
    print_estatisticas(df_processed)
    
    return df_processed

def processar_features(df):
    """Feature engineering para ML"""
    
    print("🔧 Processando features...")
    
    # 1. TARGET VARIABLE - Sucesso da candidatura
    df['sucesso_candidatura'] = df['status'].apply(lambda x: 1 if x in ['aprovada', 'contratada', 'entrevista'] else 0)
    
    # 2. FEATURES NUMÉRICAS
    df['experiencia_normalizada'] = df['anos_experiencia_esg'].fillna(0)
    df['score_atual'] = df['compatibilidade_score'].fillna(50)
    
    # 3. COMPATIBILIDADE GEOGRÁFICA
    df['mesmo_estado'] = (df['prof_uf'] == df['vaga_uf']).astype(int)
    df['aceita_remoto_int'] = df['aceita_remoto'].astype(int)
    df['vaga_remoto_int'] = df['remoto'].astype(int)
    df['compatibilidade_geografica'] = np.where(
        (df['mesmo_estado'] == 1) | (df['aceita_remoto_int'] == 1) | (df['vaga_remoto_int'] == 1), 1, 0
    )
    
    # 4. COMPATIBILIDADE SALARIAL
    df['pretensao_salarial_min'] = pd.to_numeric(df['pretensao_salarial_min'], errors='coerce').fillna(0)
    df['pretensao_salarial_max'] = pd.to_numeric(df['pretensao_salarial_max'], errors='coerce').fillna(0)
    df['pretensao_media'] = (df['pretensao_salarial_min'] + df['pretensao_salarial_max']) / 2
    df['salario_min'] = pd.to_numeric(df['salario_min'], errors='coerce').fillna(0)
    df['salario_max'] = pd.to_numeric(df['salario_max'], errors='coerce').fillna(0)
    df['salario_medio_vaga'] = (df['salario_min'] + df['salario_max']) / 2
    
    df['compatibilidade_salarial'] = np.where(
        (df['pretensao_media'] == 0) | (df['salario_medio_vaga'] == 0), 0.5,
        np.where(df['pretensao_media'] <= df['salario_max'], 1, 0)
    )
    
    # 5. MATCH DE NÍVEL DE EXPERIÊNCIA
    def nivel_para_numero(nivel):
        mapping = {'Junior': 1, 'Pleno': 2, 'Senior': 3, 'Especialista': 4}
        return mapping.get(nivel, 2)
    
    df['nivel_experiencia_num'] = df['nivel_experiencia'].apply(nivel_para_numero)
    df['nivel_adequado'] = np.where(
        df['experiencia_normalizada'] <= 2, 1,  # Junior
        np.where(df['experiencia_normalizada'] <= 5, 2,  # Pleno
                np.where(df['experiencia_normalizada'] <= 10, 3, 4))  # Senior/Especialista
    )
    df['match_nivel'] = (df['nivel_experiencia_num'] == df['nivel_adequado']).astype(int)
    
    # 6. COMPATIBILIDADE DE CARGO
    df['match_cargo'] = df.apply(calcular_match_cargo, axis=1)
    
    # 7. SKILLS OVERLAP
    df['skills_overlap'] = df.apply(calcular_skills_overlap, axis=1)
    
    # 8. ODS OVERLAP
    df['ods_overlap'] = df.apply(calcular_ods_overlap, axis=1)
    
    # 9. FEATURES TEMPORAIS
    df['data_candidatura'] = pd.to_datetime(df['data_candidatura'], format='mixed')
    df['dias_desde_candidatura'] = (datetime.now() - df['data_candidatura']).dt.days
    df['mes_candidatura'] = df['data_candidatura'].dt.month
    df['dia_semana'] = df['data_candidatura'].dt.dayofweek
    
    # 10. FEATURES CATEGÓRICAS ENCODED
    df['tipo_contratacao_encoded'] = pd.Categorical(df['tipo_contratacao']).codes
    df['disponibilidade_encoded'] = pd.Categorical(df['disponibilidade']).codes
    
    # Selecionar features finais para ML
    features_ml = [
        # Target
        'sucesso_candidatura',
        
        # Features numéricas
        'experiencia_normalizada', 'score_atual',
        
        # Compatibilidades
        'mesmo_estado', 'compatibilidade_geografica', 'compatibilidade_salarial',
        'match_nivel', 'match_cargo', 'skills_overlap', 'ods_overlap',
        
        # Features temporais
        'dias_desde_candidatura', 'mes_candidatura', 'dia_semana',
        
        # Features categóricas
        'aceita_remoto_int', 'vaga_remoto_int', 'tipo_contratacao_encoded',
        'disponibilidade_encoded',
        
        # IDs para referência
        'candidatura_id', 'profissional_id', 'vaga_id'
    ]
    
    return df[features_ml].copy()

def calcular_match_cargo(row):
    """Calcular compatibilidade entre cargo atual e título da vaga"""
    cargo = str(row['cargo_atual']).lower()
    titulo = str(row['vaga_titulo']).lower()
    
    # Palavras-chave importantes
    palavras_cargo = set(re.findall(r'\b\w+\b', cargo))
    palavras_titulo = set(re.findall(r'\b\w+\b', titulo))
    
    # Interseção normalizada
    if len(palavras_titulo) == 0:
        return 0
    
    intersecao = len(palavras_cargo.intersection(palavras_titulo))
    return intersecao / len(palavras_titulo)

def calcular_skills_overlap(row):
    """Calcular overlap entre habilidades do profissional e requeridas"""
    try:
        prof_skills = json.loads(row['habilidades_esg']) if row['habilidades_esg'] else []
        vaga_skills = json.loads(row['habilidades_requeridas']) if row['habilidades_requeridas'] else []
        
        if not prof_skills or not vaga_skills:
            return 0
        
        prof_set = set([s.lower() for s in prof_skills])
        vaga_set = set([s.lower() for s in vaga_skills])
        
        if len(vaga_set) == 0:
            return 0
        
        return len(prof_set.intersection(vaga_set)) / len(vaga_set)
    except:
        return 0

def calcular_ods_overlap(row):
    """Calcular overlap entre ODS de interesse e da vaga"""
    try:
        prof_ods = json.loads(row['ods_interesse']) if row['ods_interesse'] else []
        vaga_ods = json.loads(row['ods_tags']) if row['ods_tags'] else []
        
        if not prof_ods or not vaga_ods:
            return 0
        
        prof_set = set(prof_ods)
        vaga_set = set(vaga_ods)
        
        if len(vaga_set) == 0:
            return 0
        
        return len(prof_set.intersection(vaga_set)) / len(vaga_set)
    except:
        return 0

def print_estatisticas(df):
    """Imprimir estatísticas do dataset"""
    
    print("\n📈 ESTATÍSTICAS DO DATASET:")
    print(f"Total de candidaturas: {len(df)}")
    print(f"Candidaturas bem-sucedidas: {df['sucesso_candidatura'].sum()} ({df['sucesso_candidatura'].mean():.1%})")
    
    print(f"\n🎯 DISTRIBUIÇÃO DE FEATURES:")
    print(f"Compatibilidade geográfica: {df['compatibilidade_geografica'].mean():.1%}")
    print(f"Match de nível: {df['match_nivel'].mean():.1%}")
    print(f"Score atual médio: {df['score_atual'].mean():.1f}")
    print(f"Skills overlap médio: {df['skills_overlap'].mean():.2f}")
    print(f"ODS overlap médio: {df['ods_overlap'].mean():.2f}")
    
    print(f"\n🔍 MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("Nenhum valor faltante!")

if __name__ == "__main__":
    # Criar diretório se não existir
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    # Extrair e processar dados
    dataset = extrair_dados_ml()
    print("\n✅ Preparação de dados concluída!")
    print("📁 Próximo passo: Treinar modelo ML com este dataset")