"""
Dados estáticos da Taxonomia Sustentável Brasileira (TSB)
Baseado na Resolução CMN 4.945/2021

Fonte oficial: https://www.bcb.gov.br/estabilidadefinanceira/taxonomiasustentavel
"""

# 11 Objetivos da TSB (7 Ambientais + 4 Sociais)
OBJETIVOS_TSB = [
    {
        "id": 1,
        "codigo": "MA",
        "nome": "Mitigação e Adaptação às Mudanças Climáticas",
        "tipo": "ambiental",
        "descricao": "Atividades que contribuem substancialmente para mitigação das emissões de GEE ou adaptação aos efeitos das mudanças climáticas",
        "exemplos": ["Energias renováveis", "Eficiência energética", "Mobilidade sustentável"]
    },
    {
        "id": 2,
        "codigo": "EA",
        "nome": "Uso Sustentável e Proteção de Recursos Hídricos e Marinhos",
        "tipo": "ambiental",
        "descricao": "Proteção, conservação e uso sustentável de recursos hídricos e ecossistemas marinhos",
        "exemplos": ["Gestão hídrica", "Tratamento de efluentes", "Proteção marinha"]
    },
    {
        "id": 3,
        "codigo": "EC",
        "nome": "Transição para Economia Circular",
        "tipo": "ambiental",
        "descricao": "Promoção de padrões de produção e consumo circulares, minimizando resíduos",
        "exemplos": ["Reciclagem", "Reuso", "Design circular", "Logística reversa"]
    },
    {
        "id": 4,
        "codigo": "PP",
        "nome": "Prevenção e Controle da Poluição",
        "tipo": "ambiental",
        "descricao": "Prevenção, controle e redução da poluição do ar, água e solo",
        "exemplos": ["Controle de emissões", "Tratamento de resíduos", "Redução poluentes"]
    },
    {
        "id": 5,
        "codigo": "BP",
        "nome": "Proteção e Restauração da Biodiversidade e Ecossistemas",
        "tipo": "ambiental",
        "descricao": "Conservação, restauração e uso sustentável da biodiversidade e ecossistemas",
        "exemplos": ["Reflorestamento", "Conservação de biomas", "Restauração ecológica"]
    },
    {
        "id": 6,
        "codigo": "CAA",
        "nome": "Controle de Ameaças Ambientais Associadas",
        "tipo": "ambiental",
        "descricao": "Controle e mitigação de ameaças ambientais decorrentes de atividades econômicas",
        "exemplos": ["Gestão de riscos ambientais", "Controle de impactos"]
    },
    {
        "id": 7,
        "codigo": "AR",
        "nome": "Adequação a Regulamentações Ambientais",
        "tipo": "ambiental",
        "descricao": "Conformidade com regulamentações e padrões ambientais",
        "exemplos": ["Licenciamento", "Certificações", "Compliance ambiental"]
    },
    {
        "id": 8,
        "codigo": "TE",
        "nome": "Trabalho Decente e Emprego",
        "tipo": "social",
        "descricao": "Promoção de trabalho decente, seguro e inclusivo",
        "exemplos": ["Trabalho formal", "Segurança ocupacional", "Direitos trabalhistas"]
    },
    {
        "id": 9,
        "codigo": "IB",
        "nome": "Infraestrutura Básica e Habitação",
        "tipo": "social",
        "descricao": "Acesso a infraestrutura básica e moradia adequada",
        "exemplos": ["Habitação social", "Saneamento", "Infraestrutura urbana"]
    },
    {
        "id": 10,
        "codigo": "DI",
        "nome": "Redução de Desigualdades",
        "tipo": "social",
        "descricao": "Redução de desigualdades sociais e econômicas",
        "exemplos": ["Inclusão produtiva", "Educação", "Geração de renda"]
    },
    {
        "id": 11,
        "codigo": "IS",
        "nome": "Inclusão Social e Acesso a Serviços",
        "tipo": "social",
        "descricao": "Promoção de inclusão social e acesso a serviços essenciais",
        "exemplos": ["Saúde", "Educação", "Serviços básicos"]
    }
]

# 8 Setores Prioritários da TSB
SETORES_TSB = [
    {
        "id": 1,
        "nome": "Energia",
        "descricao": "Geração e distribuição de energia renovável e eficiência energética",
        "subsetores": [
            "Energia solar",
            "Energia eólica",
            "Biomassa e biogás",
            "Hidrelétricas sustentáveis",
            "Eficiência energética"
        ],
        "objetivos_principais": [1],  # MA
        "cnaes_exemplo": ["3511-5", "3512-3", "3513-1"]
    },
    {
        "id": 2,
        "nome": "Transportes",
        "descricao": "Mobilidade sustentável e transporte de baixo carbono",
        "subsetores": [
            "Transporte público elétrico",
            "Veículos elétricos",
            "Ciclovias e mobilidade ativa",
            "Logística verde"
        ],
        "objetivos_principais": [1, 4],  # MA, PP
        "cnaes_exemplo": ["4911-6", "4921-3", "4929-9"]
    },
    {
        "id": 3,
        "nome": "Construção Civil",
        "descricao": "Edificações sustentáveis e construções verdes",
        "subsetores": [
            "Certificações LEED/AQUA",
            "Materiais sustentáveis",
            "Eficiência hídrica e energética",
            "Retrofit verde"
        ],
        "objetivos_principais": [1, 2, 3],  # MA, EA, EC
        "cnaes_exemplo": ["4120-4", "4211-1", "4212-0"]
    },
    {
        "id": 4,
        "nome": "Agropecuária e Florestas",
        "descricao": "Agricultura sustentável, silvicultura e reflorestamento",
        "subsetores": [
            "Agricultura orgânica",
            "Sistemas agroflorestais",
            "Reflorestamento",
            "Pecuária sustentável",
            "Bioeconomia florestal"
        ],
        "objetivos_principais": [5, 1],  # BP, MA
        "cnaes_exemplo": ["0210-1", "0220-9", "0161-0"]
    },
    {
        "id": 5,
        "nome": "Água e Saneamento",
        "descricao": "Gestão sustentável de recursos hídricos e saneamento básico",
        "subsetores": [
            "Tratamento de água",
            "Tratamento de esgoto",
            "Reuso de água",
            "Gestão de bacias hidrográficas"
        ],
        "objetivos_principais": [2, 4],  # EA, PP
        "cnaes_exemplo": ["3600-6", "3701-1", "3702-9"]
    },
    {
        "id": 6,
        "nome": "Gestão de Resíduos",
        "descricao": "Economia circular e gestão sustentável de resíduos",
        "subsetores": [
            "Reciclagem",
            "Compostagem",
            "Logística reversa",
            "Valorização energética",
            "Economia circular"
        ],
        "objetivos_principais": [3, 4],  # EC, PP
        "cnaes_exemplo": ["3821-1", "3822-0", "3831-9"]
    },
    {
        "id": 7,
        "nome": "Indústria",
        "descricao": "Processos industriais limpos e eficiência de recursos",
        "subsetores": [
            "Eficiência de recursos",
            "Produção mais limpa",
            "Química verde",
            "Economia circular industrial"
        ],
        "objetivos_principais": [4, 3, 1],  # PP, EC, MA
        "cnaes_exemplo": ["2061-4", "2062-2", "2063-1"]
    },
    {
        "id": 8,
        "nome": "Turismo",
        "descricao": "Ecoturismo e turismo sustentável",
        "subsetores": [
            "Ecoturismo",
            "Turismo de base comunitária",
            "Hospedagem sustentável",
            "Turismo rural"
        ],
        "objetivos_principais": [5, 11],  # BP, IS
        "cnaes_exemplo": ["5510-8", "7911-2", "9103-1"]
    }
]

# 3 Critérios de Elegibilidade TSB
CRITERIOS_TSB = {
    "CS": {
        "nome": "Contribuição Substancial",
        "descricao": "A atividade deve contribuir substancialmente para pelo menos um objetivo ambiental ou social",
        "peso": 40
    },
    "NPS": {
        "nome": "Não Prejudicar Significativamente (Do No Significant Harm)",
        "descricao": "A atividade não deve causar dano significativo a nenhum dos outros objetivos",
        "peso": 30
    },
    "SM": {
        "nome": "Salvaguardas Mínimas",
        "descricao": "A atividade deve cumprir salvaguardas mínimas de direitos humanos e governança",
        "peso": 30
    }
}


def get_objetivo_by_id(objetivo_id: int) -> dict | None:
    """Retorna objetivo TSB por ID"""
    return next((obj for obj in OBJETIVOS_TSB if obj["id"] == objetivo_id), None)


def get_objetivo_by_codigo(codigo: str) -> dict | None:
    """Retorna objetivo TSB por código (MA, EA, etc)"""
    return next((obj for obj in OBJETIVOS_TSB if obj["codigo"] == codigo.upper()), None)


def get_setor_by_id(setor_id: int) -> dict | None:
    """Retorna setor TSB por ID"""
    return next((setor for setor in SETORES_TSB if setor["id"] == setor_id), None)


def get_objetivos_ambientais() -> list[dict]:
    """Retorna apenas objetivos ambientais (7)"""
    return [obj for obj in OBJETIVOS_TSB if obj["tipo"] == "ambiental"]


def get_objetivos_sociais() -> list[dict]:
    """Retorna apenas objetivos sociais (4)"""
    return [obj for obj in OBJETIVOS_TSB if obj["tipo"] == "social"]


def calcular_score_tsb(criterios: dict) -> float:
    """
    Calcula score de aderência TSB baseado nos 3 critérios.
    
    Args:
        criterios: Dict com chaves CS, NPS, SM (bool)
    
    Returns:
        Score de 0-100
    """
    score = 0.0
    
    if criterios.get("CS", False):
        score += CRITERIOS_TSB["CS"]["peso"]
    
    if criterios.get("NPS", True):  # Default True
        score += CRITERIOS_TSB["NPS"]["peso"]
    
    if criterios.get("SM", True):  # Default True
        score += CRITERIOS_TSB["SM"]["peso"]
    
    return score
