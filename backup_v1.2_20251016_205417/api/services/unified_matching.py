#!/usr/bin/env python3
"""
Serviço unificado de matching com ML e fallback tradicional
"""

import logging
from typing import Dict, List, Optional
from .match_calculator import match_calculator
from .ml_service import ml_service

logger = logging.getLogger(__name__)

class UnifiedMatchingService:
    """Serviço unificado que combina ML e algoritmo tradicional"""
    
    def __init__(self):
        self.ml_service = ml_service
        self.traditional_calculator = match_calculator
        
    def calculate_compatibility(self, profissional_id: int, vaga_id: int) -> Dict:
        """
        Calcular compatibilidade usando ML ou algoritmo tradicional
        
        Args:
            profissional_id: ID do profissional
            vaga_id: ID da vaga
            
        Returns:
            Dict com score e detalhes do matching
        """
        
        try:
            # Tentar usar ML primeiro
            if self.ml_service.is_loaded:
                logger.info(f"Usando ML para match prof {profissional_id} x vaga {vaga_id}")
                return self.ml_service.calculate_ml_score(profissional_id, vaga_id)
            else:
                logger.info(f"ML não disponível, usando algoritmo tradicional")
                return self._calculate_traditional_match(profissional_id, vaga_id)
                
        except Exception as e:
            logger.error(f"Erro no cálculo ML: {e}")
            return self._calculate_traditional_match(profissional_id, vaga_id)
    
    def _calculate_traditional_match(self, profissional_id: int, vaga_id: int) -> Dict:
        """Usar algoritmo tradicional como fallback"""
        
        try:
            # Buscar dados do profissional e vaga
            prof_data = self.ml_service.get_profissional_data(profissional_id)
            vaga_data = self.ml_service.get_vaga_data(vaga_id)
            
            if not prof_data or not vaga_data:
                return {
                    'score_total': 50,
                    'classificacao': 'regular',
                    'model_used': 'fallback_error',
                    'breakdown': {
                        'erro': {
                            'score': 50,
                            'detalhes': 'Dados não encontrados'
                        }
                    }
                }
            
            # Usar calculadora tradicional
            match_result = self.traditional_calculator.calcular_match(vaga_data, prof_data)
            
            # Adicionar metadados sobre o modelo usado
            match_result['model_used'] = 'traditional'
            
            return match_result
            
        except Exception as e:
            logger.error(f"Erro no cálculo tradicional: {e}")
            return {
                'score_total': 40,
                'classificacao': 'baixo',
                'model_used': 'error_fallback',
                'breakdown': {
                    'erro': {
                        'score': 40,
                        'detalhes': f'Erro no cálculo: {str(e)}'
                    }
                }
            }
    
    def get_service_status(self) -> Dict:
        """Retornar status dos serviços de matching"""
        
        return {
            'ml_available': self.ml_service.is_loaded,
            'ml_models_loaded': self.ml_service.is_loaded,
            'traditional_available': True,
            'current_mode': 'ML' if self.ml_service.is_loaded else 'Traditional'
        }

# Instância global do serviço unificado
unified_matching = UnifiedMatchingService()