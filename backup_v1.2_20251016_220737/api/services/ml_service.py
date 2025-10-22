#!/usr/bin/env python3
"""
Serviço de ML para matching inteligente
Integração dos modelos treinados na API
"""

import joblib
import numpy as np
import json
import sqlite3
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MLMatchingService:
    def __init__(self, models_dir='ml/models'):
        self.models_dir = models_dir
        self.rf_model = None
        self.xgb_model = None
        self.scaler = None
        self.feature_names = []
        self.is_loaded = False
        
        # Não carregar automaticamente para evitar erros de compatibilidade
        logger.info("MLMatchingService inicializado sem carregar modelos automaticamente")
        logger.info("Use load_models() manualmente se necessário")
    
    def load_models(self):
        """Carregar modelos treinados"""
        try:
            self.rf_model = joblib.load(f'{self.models_dir}/random_forest_model.pkl')
            self.xgb_model = joblib.load(f'{self.models_dir}/xgboost_model.pkl')
            self.scaler = joblib.load(f'{self.models_dir}/scaler.pkl')
            
            # Carregar metadados
            with open(f'{self.models_dir}/model_metadata.json', 'r') as f:
                metadata = json.load(f)
            
            self.feature_names = metadata['feature_names']
            self.is_loaded = True
            
            logger.info("✅ Modelos ML carregados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelos ML: {e}")
            return False
    
    def calculate_ml_score(self, profissional_id: int, vaga_id: int) -> Dict:
        """Calcular score usando ML se disponível, senão usar algoritmo tradicional"""
        
        if not self.is_loaded:
            return self.calculate_traditional_score(profissional_id, vaga_id)
        
        try:
            # Buscar dados do profissional e vaga
            prof_data = self.get_profissional_data(profissional_id)
            vaga_data = self.get_vaga_data(vaga_id)
            
            if not prof_data or not vaga_data:
                return self.calculate_traditional_score(profissional_id, vaga_id)
            
            # Criar features para ML
            features = self.create_ml_features(prof_data, vaga_data)
            features_scaled = self.scaler.transform([features])
            
            # Predições dos modelos
            rf_prob = self.rf_model.predict_proba(features_scaled)[0][1]
            xgb_prob = self.xgb_model.predict_proba(features_scaled)[0][1]
            
            # Score final (ensemble)
            final_prob = (rf_prob + xgb_prob) / 2
            final_score = int(final_prob * 100)
            
            # Garantir range válido
            final_score = max(0, min(100, final_score))
            
            return {
                'score_total': final_score,
                'success_probability': final_prob,
                'model_used': 'ML_ensemble',
                'rf_score': int(rf_prob * 100),
                'xgb_score': int(xgb_prob * 100),
                'classificacao': self.classify_match(final_score),
                'breakdown': {
                    'modelo': {
                        'score': final_score,
                        'detalhes': 'Random Forest + XGBoost ensemble'
                    },
                    'probabilidade': {
                        'score': int(final_prob * 100),
                        'detalhes': f'Probabilidade de sucesso: {final_prob:.2%}'
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Erro no cálculo ML para prof {profissional_id}, vaga {vaga_id}: {e}")
            return self.calculate_traditional_score(profissional_id, vaga_id)
    
    def create_ml_features(self, prof_data: Dict, vaga_data: Dict) -> List[float]:
        """Criar features para predição ML"""
        
        # 1. Experiência normalizada
        experiencia = prof_data.get('anos_experiencia_esg', 0) or 0
        
        # 2. Score atual (usar score tradicional como feature)
        score_tradicional = self.calculate_traditional_score_simple(prof_data, vaga_data)
        
        # 3. Compatibilidade geográfica
        mesmo_estado = 1 if prof_data.get('localizacao_uf') == vaga_data.get('localizacao_uf') else 0
        aceita_remoto = 1 if prof_data.get('aceita_remoto') else 0
        vaga_remoto = 1 if vaga_data.get('remoto') else 0
        compat_geo = 1 if (mesmo_estado or aceita_remoto or vaga_remoto) else 0
        
        # 4. Compatibilidade salarial
        pretensao_min = prof_data.get('pretensao_salarial_min', 0) or 0
        pretensao_max = prof_data.get('pretensao_salarial_max', 0) or 0
        salario_min = vaga_data.get('salario_min', 0) or 0
        salario_max = vaga_data.get('salario_max', 0) or 0
        
        if pretensao_min > 0 and salario_max > 0:
            compat_salarial = 1 if pretensao_min <= salario_max else 0
        else:
            compat_salarial = 0.5
        
        # 5. Match de nível
        nivel_mapping = {'Junior': 1, 'Pleno': 2, 'Senior': 3, 'Especialista': 4}
        nivel_vaga = nivel_mapping.get(vaga_data.get('nivel_experiencia', 'Pleno'), 2)
        
        if experiencia <= 2:
            nivel_adequado = 1
        elif experiencia <= 5:
            nivel_adequado = 2
        elif experiencia <= 10:
            nivel_adequado = 3
        else:
            nivel_adequado = 4
            
        match_nivel = 1 if nivel_vaga == nivel_adequado else 0
        
        # 6. Match de cargo (simplificado)
        cargo_prof = str(prof_data.get('cargo_atual', '')).lower()
        titulo_vaga = str(vaga_data.get('titulo', '')).lower()
        
        palavras_prof = set(cargo_prof.split())
        palavras_vaga = set(titulo_vaga.split())
        
        if palavras_vaga:
            match_cargo = len(palavras_prof.intersection(palavras_vaga)) / len(palavras_vaga)
        else:
            match_cargo = 0
        
        # 7. Skills overlap (simplificado)
        try:
            prof_skills = json.loads(prof_data.get('habilidades_esg', '[]')) if prof_data.get('habilidades_esg') else []
            vaga_skills = json.loads(vaga_data.get('habilidades_requeridas', '[]')) if vaga_data.get('habilidades_requeridas') else []
            
            if prof_skills and vaga_skills:
                prof_set = set([s.lower() for s in prof_skills])
                vaga_set = set([s.lower() for s in vaga_skills])
                skills_overlap = len(prof_set.intersection(vaga_set)) / len(vaga_set) if vaga_set else 0
            else:
                skills_overlap = 0
        except:
            skills_overlap = 0
        
        # 8. ODS overlap (simplificado)
        try:
            prof_ods = json.loads(prof_data.get('ods_interesse', '[]')) if prof_data.get('ods_interesse') else []
            vaga_ods = json.loads(vaga_data.get('ods_tags', '[]')) if vaga_data.get('ods_tags') else []
            
            if prof_ods and vaga_ods:
                ods_overlap = len(set(prof_ods).intersection(set(vaga_ods))) / len(set(vaga_ods)) if vaga_ods else 0
            else:
                ods_overlap = 0
        except:
            ods_overlap = 0
        
        # 9. Features temporais (valores padrão)
        dias_desde_candidatura = 5  # Simular candidatura recente
        mes_candidatura = 10
        dia_semana = 2
        
        # 10. Features categóricas
        tipo_contratacao_encoded = 1
        disponibilidade_encoded = 1
        
        # Retornar features na ordem esperada pelo modelo
        return [
            experiencia,                    # experiencia_normalizada
            score_tradicional,              # score_atual
            mesmo_estado,                   # mesmo_estado
            compat_geo,                     # compatibilidade_geografica
            compat_salarial,                # compatibilidade_salarial
            match_nivel,                    # match_nivel
            match_cargo,                    # match_cargo
            skills_overlap,                 # skills_overlap
            ods_overlap,                    # ods_overlap
            dias_desde_candidatura,         # dias_desde_candidatura
            mes_candidatura,                # mes_candidatura
            dia_semana,                     # dia_semana
            aceita_remoto,                  # aceita_remoto_int
            vaga_remoto,                    # vaga_remoto_int
            tipo_contratacao_encoded,       # tipo_contratacao_encoded
            disponibilidade_encoded         # disponibilidade_encoded
        ]
    
    def get_profissional_data(self, profissional_id: int) -> Optional[Dict]:
        """Buscar dados do profissional no banco"""
        try:
            conn = sqlite3.connect('gjb_dev.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM profissionais_esg WHERE id = ?
            """, (profissional_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Converter para dict
            columns = [description[0] for description in cursor.description]
            prof_data = dict(zip(columns, row))
            
            conn.close()
            return prof_data
            
        except Exception as e:
            logger.error(f"Erro ao buscar profissional {profissional_id}: {e}")
            return None
    
    def get_vaga_data(self, vaga_id: int) -> Optional[Dict]:
        """Buscar dados da vaga no banco"""
        try:
            conn = sqlite3.connect('gjb_dev.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM vagas_esg WHERE id = ?
            """, (vaga_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Converter para dict
            columns = [description[0] for description in cursor.description]
            vaga_data = dict(zip(columns, row))
            
            conn.close()
            return vaga_data
            
        except Exception as e:
            logger.error(f"Erro ao buscar vaga {vaga_id}: {e}")
            return None
    
    def calculate_traditional_score_simple(self, prof_data: Dict, vaga_data: Dict) -> int:
        """Versão simplificada do algoritmo tradicional para usar como feature"""
        score = 50
        
        # Experiência
        experiencia = prof_data.get('anos_experiencia_esg', 0) or 0
        if experiencia >= 5:
            score += 15
        elif experiencia >= 2:
            score += 10
        
        # Localização
        if prof_data.get('localizacao_uf') == vaga_data.get('localizacao_uf'):
            score += 10
        elif prof_data.get('aceita_remoto') or vaga_data.get('remoto'):
            score += 5
        
        # Cargo similar
        cargo_prof = str(prof_data.get('cargo_atual', '')).lower()
        titulo_vaga = str(vaga_data.get('titulo', '')).lower()
        
        if 'analista' in cargo_prof and 'analista' in titulo_vaga:
            score += 15
        elif 'coordenador' in cargo_prof and 'coordenador' in titulo_vaga:
            score += 15
        
        return max(0, min(100, score))
    
    def calculate_traditional_score(self, profissional_id: int, vaga_id: int) -> Dict:
        """Algoritmo tradicional como fallback"""
        
        # Buscar dados
        prof_data = self.get_profissional_data(profissional_id)
        vaga_data = self.get_vaga_data(vaga_id)
        
        if not prof_data or not vaga_data:
            return {
                'score_total': 50,
                'classificacao': 'regular',
                'model_used': 'fallback',
                'breakdown': {
                    'erro': {
                        'score': 50,
                        'detalhes': 'Dados não encontrados'
                    }
                }
            }
        
        score = self.calculate_traditional_score_simple(prof_data, vaga_data)
        
        return {
            'score_total': score,
            'classificacao': self.classify_match(score),
            'model_used': 'traditional',
            'breakdown': {
                'algoritmo_tradicional': {
                    'score': score,
                    'detalhes': 'Algoritmo baseado em regras'
                }
            }
        }
    
    def classify_match(self, score: int) -> str:
        """Classificar qualidade do match"""
        if score >= 80:
            return 'excelente'
        elif score >= 65:
            return 'bom'
        elif score >= 50:
            return 'regular'
        else:
            return 'baixo'

# Instância global do serviço (sem carregar modelos automaticamente)
try:
    ml_service = MLMatchingService()
    logger.info("✅ MLMatchingService instanciado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao instanciar MLMatchingService: {e}")
    ml_service = None