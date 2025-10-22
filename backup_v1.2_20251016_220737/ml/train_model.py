#!/usr/bin/env python3
"""
Modelo de Machine Learning para Matching Inteligente
Random Forest + XGBoost para predição de sucesso de candidaturas
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MatchingMLModel:
    def __init__(self):
        self.rf_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def load_data(self, dataset_path='data/processed/ml_dataset.csv'):
        """Carregar dataset processado"""
        print("📊 Carregando dataset...")
        self.df = pd.read_csv(dataset_path)
        print(f"✅ Dataset carregado: {len(self.df)} amostras")
        return self.df
    
    def prepare_features(self):
        """Preparar features para treinamento"""
        print("🔧 Preparando features...")
        
        # Features para ML (excluindo IDs e target)
        feature_columns = [
            'experiencia_normalizada', 'score_atual',
            'mesmo_estado', 'compatibilidade_geografica', 'compatibilidade_salarial',
            'match_nivel', 'match_cargo', 'skills_overlap', 'ods_overlap',
            'dias_desde_candidatura', 'mes_candidatura', 'dia_semana',
            'aceita_remoto_int', 'vaga_remoto_int', 'tipo_contratacao_encoded',
            'disponibilidade_encoded'
        ]
        
        self.feature_names = feature_columns
        
        # Separar features e target
        X = self.df[feature_columns]
        y = self.df['sucesso_candidatura']
        
        # Normalizar features numéricas
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)
        
        print(f"✅ Features preparadas: {X_scaled.shape}")
        print(f"📊 Distribuição target: {y.value_counts().to_dict()}")
        
        return X_scaled, y
    
    def train_models(self, X, y, test_size=0.2, random_state=42):
        """Treinar Random Forest e XGBoost"""
        print("🤖 Treinando modelos...")
        
        # Split dos dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        self.X_train, self.X_test = X_train, X_test
        self.y_train, self.y_test = y_train, y_test
        
        print(f"📈 Treino: {len(X_train)} amostras")
        print(f"🧪 Teste: {len(X_test)} amostras")
        
        # 1. RANDOM FOREST
        print("\\n🌲 Treinando Random Forest...")
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            class_weight='balanced'
        )
        self.rf_model.fit(X_train, y_train)
        
        # 2. XGBOOST
        print("🚀 Treinando XGBoost...")
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=random_state,
            scale_pos_weight=len(y_train[y_train==0])/len(y_train[y_train==1])
        )
        self.xgb_model.fit(X_train, y_train)
        
        self.is_trained = True
        print("✅ Modelos treinados!")
        
        return self.evaluate_models()
    
    def evaluate_models(self):
        """Avaliar performance dos modelos"""
        print("\\n📊 AVALIAÇÃO DOS MODELOS:")
        
        results = {}
        
        for name, model in [('Random Forest', self.rf_model), ('XGBoost', self.xgb_model)]:
            # Predições
            y_pred_train = model.predict(self.X_train)
            y_pred_test = model.predict(self.X_test)
            
            # Métricas
            train_acc = accuracy_score(self.y_train, y_pred_train)
            test_acc = accuracy_score(self.y_test, y_pred_test)
            
            # Cross-validation
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5)
            
            results[name] = {
                'train_accuracy': train_acc,
                'test_accuracy': test_acc,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            print(f"\\n🎯 {name}:")
            print(f"   Acurácia Treino: {train_acc:.3f}")
            print(f"   Acurácia Teste: {test_acc:.3f}")
            print(f"   CV Score: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
            
            # Relatório detalhado
            print(f"\\n📈 Relatório Classificação ({name}):")
            print(classification_report(self.y_test, y_pred_test, 
                                      target_names=['Não Sucesso', 'Sucesso']))
        
        return results
    
    def feature_importance(self):
        """Analisar importância das features"""
        print("\\n🔍 IMPORTÂNCIA DAS FEATURES:")
        
        # Random Forest
        rf_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance_rf': self.rf_model.feature_importances_
        }).sort_values('importance_rf', ascending=False)
        
        # XGBoost
        xgb_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance_xgb': self.xgb_model.feature_importances_
        }).sort_values('importance_xgb', ascending=False)
        
        # Combinar
        importance_df = rf_importance.merge(xgb_importance, on='feature')
        importance_df['importance_media'] = (importance_df['importance_rf'] + 
                                           importance_df['importance_xgb']) / 2
        importance_df = importance_df.sort_values('importance_media', ascending=False)
        
        print("\\n🏆 TOP 10 FEATURES MAIS IMPORTANTES:")
        for i, row in importance_df.head(10).iterrows():
            print(f"   {row['feature']}: {row['importance_media']:.3f}")
        
        return importance_df
    
    def predict_compatibility(self, profissional_data, vaga_data):
        """Predizer compatibilidade para novo par profissional-vaga"""
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda!")
        
        # Criar features para predição
        features = self.create_features_for_prediction(profissional_data, vaga_data)
        features_scaled = self.scaler.transform([features])
        
        # Predições dos dois modelos
        rf_prob = self.rf_model.predict_proba(features_scaled)[0][1]
        xgb_prob = self.xgb_model.predict_proba(features_scaled)[0][1]
        
        # Média ensemble
        final_prob = (rf_prob + xgb_prob) / 2
        final_score = int(final_prob * 100)
        
        return {
            'compatibility_score': final_score,
            'success_probability': final_prob,
            'rf_score': int(rf_prob * 100),
            'xgb_score': int(xgb_prob * 100),
            'classification': self.classify_match(final_score)
        }
    
    def create_features_for_prediction(self, prof, vaga):
        """Criar features para predição de novo caso"""
        # Implementar lógica de criação de features similar ao script de preparação
        # Por simplicidade, retornar valores padrão por enquanto
        return [
            prof.get('anos_experiencia_esg', 3),  # experiencia_normalizada
            prof.get('score_atual', 65),          # score_atual
            1 if prof.get('uf') == vaga.get('uf') else 0,  # mesmo_estado
            1,  # compatibilidade_geografica
            0.8,  # compatibilidade_salarial
            0,  # match_nivel
            0.3,  # match_cargo
            0.2,  # skills_overlap
            0.1,  # ods_overlap
            5,  # dias_desde_candidatura
            10,  # mes_candidatura
            2,  # dia_semana
            prof.get('aceita_remoto', 1),  # aceita_remoto_int
            vaga.get('remoto', 0),         # vaga_remoto_int
            1,  # tipo_contratacao_encoded
            1   # disponibilidade_encoded
        ]
    
    def classify_match(self, score):
        """Classificar qualidade do match"""
        if score >= 80:
            return 'excelente'
        elif score >= 65:
            return 'bom'
        elif score >= 50:
            return 'regular'
        else:
            return 'baixo'
    
    def save_models(self, models_dir='ml/models'):
        """Salvar modelos treinados"""
        import os
        os.makedirs(models_dir, exist_ok=True)
        
        joblib.dump(self.rf_model, f'{models_dir}/random_forest_model.pkl')
        joblib.dump(self.xgb_model, f'{models_dir}/xgboost_model.pkl')
        joblib.dump(self.scaler, f'{models_dir}/scaler.pkl')
        
        # Salvar metadados
        metadata = {
            'feature_names': self.feature_names,
            'trained_date': datetime.now().isoformat(),
            'dataset_size': len(self.df),
            'test_accuracy_rf': accuracy_score(self.y_test, self.rf_model.predict(self.X_test)),
            'test_accuracy_xgb': accuracy_score(self.y_test, self.xgb_model.predict(self.X_test))
        }
        
        import json
        with open(f'{models_dir}/model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Modelos salvos em {models_dir}/")
    
    def load_models(self, models_dir='ml/models'):
        """Carregar modelos salvos"""
        self.rf_model = joblib.load(f'{models_dir}/random_forest_model.pkl')
        self.xgb_model = joblib.load(f'{models_dir}/xgboost_model.pkl')
        self.scaler = joblib.load(f'{models_dir}/scaler.pkl')
        
        import json
        with open(f'{models_dir}/model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        self.feature_names = metadata['feature_names']
        self.is_trained = True
        
        print(f"✅ Modelos carregados de {models_dir}/")
        return metadata

def main():
    """Função principal para treinar os modelos"""
    print("🤖 GREEN JOBS BRASIL - SISTEMA DE ML")
    print("=====================================")
    
    # Inicializar modelo
    ml_model = MatchingMLModel()
    
    # Carregar e preparar dados
    df = ml_model.load_data()
    X, y = ml_model.prepare_features()
    
    # Treinar modelos
    results = ml_model.train_models(X, y)
    
    # Analisar importância das features
    importance = ml_model.feature_importance()
    
    # Salvar modelos
    ml_model.save_models()
    
    print("\\n🎉 TREINAMENTO CONCLUÍDO!")
    print("📁 Modelos salvos em ml/models/")
    print("🚀 Pronto para integração na API!")
    
    return ml_model, results, importance

if __name__ == "__main__":
    model, results, importance = main()