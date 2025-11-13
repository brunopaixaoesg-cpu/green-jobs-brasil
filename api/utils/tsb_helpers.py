"""
Helpers para integração TSB com empresas.
Enriquece dados de empresas com informações da Taxonomia Sustentável Brasileira.
"""
from typing import Dict, Any, List
from api.data.taxonomia_tsb import calcular_score_tsb, get_objetivo_by_id, get_setor_by_id


# Mapeamento simplificado CNAE → TSB para demonstração
# Em produção, isso viria do banco de dados
CNAE_TO_TSB_MAPPING = {
    # Energia Renovável
    "3511-5": {"objetivos": [1], "setores": [1], "cs": True},  # Geração energia elétrica
    "3512-3": {"objetivos": [1], "setores": [1], "cs": True},  # Transmissão energia
    "3513-1": {"objetivos": [1], "setores": [1], "cs": True},  # Distribuição energia
    
    # Gestão de Resíduos
    "3821-1": {"objetivos": [3, 4], "setores": [6], "cs": True},  # Resíduos não perigosos
    "3822-0": {"objetivos": [3, 4], "setores": [6], "cs": True},  # Resíduos perigosos
    "3831-9": {"objetivos": [3], "setores": [6], "cs": True},  # Recuperação materiais
    "3832-7": {"objetivos": [3], "setores": [6], "cs": True},  # Recuperação sucatas
    
    # Água e Saneamento
    "3600-6": {"objetivos": [2], "setores": [5], "cs": True},  # Captação, tratamento água
    "3701-1": {"objetivos": [2, 4], "setores": [5], "cs": True},  # Esgoto
    "3702-9": {"objetivos": [2, 4], "setores": [5], "cs": True},  # Limpeza urbana
    
    # Agropecuária Sustentável
    "0161-0": {"objetivos": [5], "setores": [4], "cs": False},  # Agricultura (depende práticas)
    "0210-1": {"objetivos": [5, 1], "setores": [4], "cs": True},  # Silvicultura
    "0220-9": {"objetivos": [5], "setores": [4], "cs": True},  # Exploração florestal
    
    # Construção Sustentável
    "4120-4": {"objetivos": [1, 3], "setores": [3], "cs": False},  # Construção (depende certificação)
    "4211-1": {"objetivos": [1], "setores": [3], "cs": False},  # Rodovias e ferrovias
    "4212-0": {"objetivos": [2], "setores": [3], "cs": False},  # Obras infra urbana
    
    # Transporte Sustentável
    "4911-6": {"objetivos": [1, 4], "setores": [2], "cs": False},  # Transporte ferroviário
    "4921-3": {"objetivos": [1], "setores": [2], "cs": False},  # Transporte metroviário
    "4929-9": {"objetivos": [1], "setores": [2], "cs": False},  # Transporte rodoviário coletivo
    
    # Turismo Sustentável
    "5510-8": {"objetivos": [11], "setores": [8], "cs": False},  # Hotéis
    "7911-2": {"objetivos": [11], "setores": [8], "cs": False},  # Agências de viagem
    "9103-1": {"objetivos": [5, 11], "setores": [8], "cs": True},  # Parques naturais
    
    # Indústria Limpa
    "2061-4": {"objetivos": [3, 4], "setores": [7], "cs": False},  # Resinas e elastômeros
    "2062-2": {"objetivos": [3, 4], "setores": [7], "cs": False},  # Produtos químicos
}


def enriquecer_empresa_com_tsb(empresa: Dict[str, Any], cnaes: List[str] = None) -> Dict[str, Any]:
    """
    Enriquece dados de uma empresa com informações TSB.
    
    Args:
        empresa: Dict com dados da empresa
        cnaes: Lista de CNAEs da empresa (opcional, pode vir dentro de empresa)
    
    Returns:
        Dict com empresa enriquecida
    """
    # Extrair CNAEs se não fornecidos
    if cnaes is None:
        cnaes = empresa.get("cnaes", [])
        if isinstance(cnaes, str):
            cnaes = [cnaes]
    
    # Classificar empresa na TSB
    objetivos_set = set()
    setores_set = set()
    tem_cs = False
    
    for cnae in cnaes:
        if cnae in CNAE_TO_TSB_MAPPING:
            mapping = CNAE_TO_TSB_MAPPING[cnae]
            objetivos_set.update(mapping.get("objetivos", []))
            setores_set.update(mapping.get("setores", []))
            if mapping.get("cs", False):
                tem_cs = True
    
    # Calcular score TSB
    criterios = {
        "CS": tem_cs,
        "NPS": True,  # Assumir True para demonstração
        "SM": True    # Assumir True para demonstração
    }
    score_tsb = calcular_score_tsb(criterios)
    
    # TSB elegível se tiver pelo menos 1 objetivo
    tsb_elegivel = len(objetivos_set) > 0
    
    # Enriquecer empresa
    empresa_enriquecida = empresa.copy()
    empresa_enriquecida.update({
        "tsb_elegivel": tsb_elegivel,
        "tsb_score": score_tsb if tsb_elegivel else 0,
        "tsb_objetivos": sorted(list(objetivos_set)),
        "tsb_setores": sorted(list(setores_set)),
        "tsb_criterios": criterios if tsb_elegivel else {},
        "tsb_badge": "TSB BR" if tsb_elegivel else None
    })
    
    return empresa_enriquecida


def get_empresas_por_objetivo(objetivo_id: int, limite: int = 50) -> List[Dict]:
    """
    Retorna empresas que atendem um objetivo TSB específico.
    
    Args:
        objetivo_id: ID do objetivo TSB (1-11)
        limite: Número máximo de empresas
    
    Returns:
        Lista de empresas
    """
    # TODO: Implementar query no banco
    # Por enquanto retorna lista vazia
    return []


def get_empresas_por_setor(setor_id: int, limite: int = 50) -> List[Dict]:
    """
    Retorna empresas de um setor TSB específico.
    
    Args:
        setor_id: ID do setor TSB (1-8)
        limite: Número máximo de empresas
    
    Returns:
        Lista de empresas
    """
    # TODO: Implementar query no banco
    # Por enquanto retorna lista vazia
    return []


def get_estatisticas_tsb_empresas() -> Dict[str, Any]:
    """
    Retorna estatísticas agregadas de empresas TSB.
    
    Returns:
        Dict com estatísticas
    """
    # TODO: Implementar query no banco
    # Por enquanto retorna mock
    return {
        "total_empresas_tsb": 0,
        "por_objetivo": {},
        "por_setor": {},
        "score_medio": 0
    }
