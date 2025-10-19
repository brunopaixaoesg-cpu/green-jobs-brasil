"""
Motor de Matching Green Jobs Brasil
Sistema de pontuação para match entre vagas e profissionais ESG
Critérios: ODS (40%), Habilidades (30%), Experiência (15%), Localização (10%), Salário (5%)
"""

from typing import Dict, List, Tuple
import json


class MatchCalculator:
    """Calculador de compatibilidade entre vagas e profissionais"""
    
    # Pesos dos critérios de matching
    PESOS = {
        'ods': 0.40,           # 40% - Alinhamento de ODS
        'habilidades': 0.30,   # 30% - Match de habilidades
        'experiencia': 0.15,   # 15% - Nível de experiência
        'localizacao': 0.10,   # 10% - Compatibilidade de localização
        'salario': 0.05        # 5% - Faixa salarial
    }
    
    def __init__(self):
        """Inicializa o calculador"""
        pass
    
    def calcular_match(
        self, 
        vaga: Dict, 
        profissional: Dict
    ) -> Dict:
        """
        Calcula score de compatibilidade entre vaga e profissional
        
        Args:
            vaga: Dados da vaga (dict)
            profissional: Dados do profissional (dict)
            
        Returns:
            Dict com score total e breakdown por critério
        """
        
        # Calcular cada componente
        ods_score = self._calcular_ods_match(vaga, profissional)
        skills_score = self._calcular_skills_match(vaga, profissional)
        exp_score = self._calcular_experiencia_match(vaga, profissional)
        loc_score = self._calcular_localizacao_match(vaga, profissional)
        sal_score = self._calcular_salario_match(vaga, profissional)
        
        # Score total ponderado
        score_total = (
            ods_score * self.PESOS['ods'] +
            skills_score * self.PESOS['habilidades'] +
            exp_score * self.PESOS['experiencia'] +
            loc_score * self.PESOS['localizacao'] +
            sal_score * self.PESOS['salario']
        )
        
        # Arredondar para 2 casas decimais
        score_total = round(score_total, 2)
        
        # Classificar match
        classificacao = self._classificar_match(score_total)
        
        return {
            'score_total': score_total,
            'classificacao': classificacao,
            'breakdown': {
                'ods': {
                    'score': round(ods_score, 2),
                    'peso': self.PESOS['ods'],
                    'contribuicao': round(ods_score * self.PESOS['ods'], 2)
                },
                'habilidades': {
                    'score': round(skills_score, 2),
                    'peso': self.PESOS['habilidades'],
                    'contribuicao': round(skills_score * self.PESOS['habilidades'], 2)
                },
                'experiencia': {
                    'score': round(exp_score, 2),
                    'peso': self.PESOS['experiencia'],
                    'contribuicao': round(exp_score * self.PESOS['experiencia'], 2)
                },
                'localizacao': {
                    'score': round(loc_score, 2),
                    'peso': self.PESOS['localizacao'],
                    'contribuicao': round(loc_score * self.PESOS['localizacao'], 2)
                },
                'salario': {
                    'score': round(sal_score, 2),
                    'peso': self.PESOS['salario'],
                    'contribuicao': round(sal_score * self.PESOS['salario'], 2)
                }
            }
        }
    
    def _calcular_ods_match(self, vaga: Dict, profissional: Dict) -> float:
        """
        Calcula compatibilidade de ODS (0-100)
        
        Score = (ODS em comum / Total de ODS da vaga) * 100
        Bônus: +10 pontos se profissional tem experiência comprovada nos ODS
        """
        
        vaga_ods = self._parse_json_field(vaga.get('ods_tags', []))
        prof_ods = self._parse_json_field(profissional.get('ods_interesse', []))
        prof_ods_exp = self._parse_json_field(profissional.get('ods_experiencia', {}))
        
        if not vaga_ods:
            return 100.0  # Se vaga não especifica ODS, aceita qualquer profissional
        
        # ODS em comum
        comum = set(vaga_ods) & set(prof_ods)
        
        if not comum:
            return 0.0  # Nenhum ODS em comum
        
        # Score base: proporção de match
        score = (len(comum) / len(vaga_ods)) * 100
        
        # Bônus por experiência comprovada
        if isinstance(prof_ods_exp, dict):
            ods_com_experiencia = set(int(k) for k in prof_ods_exp.keys() if prof_ods_exp[k] > 0)
            overlap_experiente = comum & ods_com_experiencia
            
            if overlap_experiente:
                bonus = min(10, len(overlap_experiente) * 3)  # Até 10 pontos de bônus
                score = min(100, score + bonus)
        
        return score
    
    def _calcular_skills_match(self, vaga: Dict, profissional: Dict) -> float:
        """
        Calcula compatibilidade de habilidades (0-100)
        
        Score = (Habilidades em comum / Total de habilidades requeridas) * 100
        """
        
        vaga_skills = self._parse_json_field(vaga.get('habilidades_requeridas', []))
        prof_skills = self._parse_json_field(profissional.get('habilidades_esg', []))
        
        if not vaga_skills:
            return 100.0  # Se vaga não especifica habilidades, aceita qualquer um
        
        # Normalizar habilidades (lowercase, strip)
        vaga_skills_norm = {s.lower().strip() for s in vaga_skills}
        prof_skills_norm = {s.lower().strip() for s in prof_skills}
        
        # Calcular overlap
        comum = vaga_skills_norm & prof_skills_norm
        
        if not comum:
            return 0.0
        
        # Score proporcional
        score = (len(comum) / len(vaga_skills_norm)) * 100
        
        return score
    
    def _calcular_experiencia_match(self, vaga: Dict, profissional: Dict) -> float:
        """
        Calcula compatibilidade de experiência (0-100)
        
        Baseado em:
        - Nível da vaga vs. nível do profissional
        - Anos de experiência ESG
        """
        
        vaga_nivel = vaga.get('nivel_experiencia', '') or ''
        prof_nivel = profissional.get('nivel_desejado', '') or ''
        prof_exp_esg = profissional.get('anos_experiencia_esg', 0) or 0
        
        # Garantir que são strings antes de chamar lower()
        vaga_nivel = str(vaga_nivel).lower() if vaga_nivel else 'pleno'
        prof_nivel = str(prof_nivel).lower() if prof_nivel else 'pleno'
        
        # Mapeamento de níveis para score
        niveis_hierarchy = {
            'estagio': 1,
            'junior': 2,
            'pleno': 3,
            'senior': 4,
            'especialista': 5,
            'gerencial': 6
        }
        
        vaga_nivel_num = niveis_hierarchy.get(vaga_nivel, 3)  # Default: pleno
        prof_nivel_num = niveis_hierarchy.get(prof_nivel, 3)
        
        # Experiência mínima esperada por nível
        exp_minima_por_nivel = {
            1: 0,   # Estágio
            2: 1,   # Júnior
            3: 3,   # Pleno
            4: 5,   # Sênior
            5: 7,   # Especialista
            6: 10   # Gerencial
        }
        
        exp_esperada = exp_minima_por_nivel.get(vaga_nivel_num, 3)
        
        # Score baseado em match de nível
        diff_nivel = abs(vaga_nivel_num - prof_nivel_num)
        
        if diff_nivel == 0:
            nivel_score = 100  # Match perfeito
        elif diff_nivel == 1:
            nivel_score = 80   # Próximo (aceitável)
        elif diff_nivel == 2:
            nivel_score = 50   # Distante
        else:
            nivel_score = 20   # Muito distante
        
        # Ajuste por experiência real
        if prof_exp_esg >= exp_esperada:
            exp_score = 100
        elif prof_exp_esg >= exp_esperada * 0.7:
            exp_score = 80
        elif prof_exp_esg >= exp_esperada * 0.5:
            exp_score = 60
        else:
            exp_score = 40
        
        # Score final: média ponderada (60% nível, 40% experiência)
        score = (nivel_score * 0.6) + (exp_score * 0.4)
        
        return score
    
    def _calcular_localizacao_match(self, vaga: Dict, profissional: Dict) -> float:
        """
        Calcula compatibilidade de localização (0-100)
        
        Considera:
        - Trabalho remoto
        - Mesmo estado
        - Mesma cidade
        - Disponibilidade para mudança
        """
        
        vaga_uf = vaga.get('localizacao_uf', '').upper()
        vaga_remoto = vaga.get('remoto', False)
        
        prof_uf = profissional.get('localizacao_uf', '').upper()
        prof_aceita_remoto = profissional.get('aceita_remoto', False)
        prof_mudanca = profissional.get('disponivel_mudanca', False)
        
        # Trabalho remoto = match perfeito
        if vaga_remoto and prof_aceita_remoto:
            return 100.0
        
        # Vaga presencial
        if not vaga_uf:
            return 100.0  # Vaga não especifica localização
        
        # Mesmo estado
        if vaga_uf == prof_uf:
            # Mesma cidade?
            vaga_cidade = vaga.get('localizacao_cidade', '').lower()
            prof_cidade = profissional.get('localizacao_cidade', '').lower()
            
            if vaga_cidade and prof_cidade and vaga_cidade == prof_cidade:
                return 100.0  # Mesma cidade
            else:
                return 80.0   # Mesmo estado, cidades diferentes
        
        # Estados diferentes
        if prof_mudanca:
            return 60.0  # Disponível para mudança
        else:
            return 20.0  # Incompatível
    
    def _calcular_salario_match(self, vaga: Dict, profissional: Dict) -> float:
        """
        Calcula compatibilidade salarial (0-100)
        
        Verifica overlap entre faixa oferecida e pretensão
        """
        
        vaga_min = vaga.get('salario_min')
        vaga_max = vaga.get('salario_max')
        prof_min = profissional.get('pretensao_salarial_min')
        prof_max = profissional.get('pretensao_salarial_max')
        
        # Se algum não informou, assume compatível
        if not all([vaga_min, vaga_max, prof_min, prof_max]):
            return 100.0
        
        # Calcular overlap
        range_start = max(vaga_min, prof_min)
        range_end = min(vaga_max, prof_max)
        
        # Há overlap?
        if range_end >= range_start:
            # Calcular % de overlap
            overlap_size = range_end - range_start
            vaga_range = vaga_max - vaga_min
            prof_range = prof_max - prof_min
            
            avg_range = (vaga_range + prof_range) / 2
            
            if avg_range == 0:
                return 100.0
            
            overlap_ratio = overlap_size / avg_range
            score = min(100, overlap_ratio * 100)
            
            return score
        else:
            # Nenhum overlap - calcular distância
            gap = range_start - range_end
            avg_salary = (vaga_min + vaga_max + prof_min + prof_max) / 4
            
            if avg_salary == 0:
                return 0.0
            
            gap_ratio = gap / avg_salary
            
            # Penalizar proporcionalmente à distância
            if gap_ratio <= 0.1:
                return 80.0  # 10% de diferença
            elif gap_ratio <= 0.2:
                return 60.0  # 20% de diferença
            elif gap_ratio <= 0.3:
                return 40.0  # 30% de diferença
            else:
                return 20.0  # >30% de diferença
    
    def _classificar_match(self, score: float) -> str:
        """
        Classifica o match baseado no score
        
        Returns:
            'excelente', 'bom', 'regular', 'baixo'
        """
        
        if score >= 80:
            return 'excelente'
        elif score >= 60:
            return 'bom'
        elif score >= 40:
            return 'regular'
        else:
            return 'baixo'
    
    def _parse_json_field(self, field):
        """Parse de campos JSON (pode ser string ou objeto)"""
        
        if field is None:
            return []
        
        if isinstance(field, str):
            try:
                return json.loads(field)
            except:
                return []
        
        return field
    
    def rankear_candidatos(
        self, 
        vaga: Dict, 
        profissionais: List[Dict],
        min_score: float = 40.0
    ) -> List[Tuple[Dict, Dict]]:
        """
        Rankeia profissionais para uma vaga
        
        Args:
            vaga: Dados da vaga
            profissionais: Lista de profissionais
            min_score: Score mínimo para considerar (default: 40)
            
        Returns:
            Lista de tuplas (profissional, match_data) ordenada por score
        """
        
        matches = []
        
        for prof in profissionais:
            match_data = self.calcular_match(vaga, prof)
            
            if match_data['score_total'] >= min_score:
                matches.append((prof, match_data))
        
        # Ordenar por score (maior primeiro)
        matches.sort(key=lambda x: x[1]['score_total'], reverse=True)
        
        return matches
    
    def rankear_vagas(
        self, 
        profissional: Dict, 
        vagas: List[Dict],
        min_score: float = 40.0
    ) -> List[Tuple[Dict, Dict]]:
        """
        Rankeia vagas para um profissional
        
        Args:
            profissional: Dados do profissional
            vagas: Lista de vagas
            min_score: Score mínimo para considerar (default: 40)
            
        Returns:
            Lista de tuplas (vaga, match_data) ordenada por score
        """
        
        matches = []
        
        for vaga in vagas:
            match_data = self.calcular_match(vaga, profissional)
            
            if match_data['score_total'] >= min_score:
                matches.append((vaga, match_data))
        
        # Ordenar por score (maior primeiro)
        matches.sort(key=lambda x: x[1]['score_total'], reverse=True)
        
        return matches


# Instância global
match_calculator = MatchCalculator()
