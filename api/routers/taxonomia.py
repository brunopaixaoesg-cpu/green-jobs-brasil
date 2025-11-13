"""
Router para Taxonomia Sustentável Brasileira (TSB)
Endpoints básicos para consulta de objetivos e setores
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from api.data.taxonomia_tsb import (
    OBJETIVOS_TSB,
    SETORES_TSB,
    CRITERIOS_TSB,
    get_objetivo_by_id,
    get_objetivo_by_codigo,
    get_setor_by_id,
    get_objetivos_ambientais,
    get_objetivos_sociais
)
from api.settings import settings
from api.logger_setup import get_logger

router = APIRouter(prefix="/api/taxonomia", tags=["Taxonomia TSB"])
logger = get_logger(__name__)


@router.get("/")
async def taxonomia_info():
    """
    Informações gerais sobre a Taxonomia Sustentável Brasileira.
    
    Retorna resumo executivo da TSB integrada na plataforma.
    """
    return {
        "nome": "Taxonomia Sustentável Brasileira",
        "sigla": "TSB",
        "fonte": "Resolução CMN 4.945/2021",
        "descricao": "Framework oficial do governo brasileiro para classificação de atividades econômicas sustentáveis",
        "total_objetivos": len(OBJETIVOS_TSB),
        "total_setores": len(SETORES_TSB),
        "objetivos_ambientais": len(get_objetivos_ambientais()),
        "objetivos_sociais": len(get_objetivos_sociais()),
        "criterios": list(CRITERIOS_TSB.keys()),
        "integracao_gjb": {
            "ativa": settings.enable_tsb,
            "empresas_classificadas": "Em processamento",
            "api_versao": settings.app_version
        },
        "endpoints": {
            "objetivos": "/api/taxonomia/objetivos",
            "setores": "/api/taxonomia/setores",
            "criterios": "/api/taxonomia/criterios"
        }
    }


@router.get("/objetivos")
async def listar_objetivos(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: ambiental ou social")
):
    """
    Lista todos os objetivos da TSB.
    
    **11 Objetivos:**
    - 7 Ambientais (MA, EA, EC, PP, BP, CAA, AR)
    - 4 Sociais (TE, IB, DI, IS)
    
    Query params:
    - tipo: "ambiental" ou "social" (opcional)
    """
    objetivos = OBJETIVOS_TSB
    
    if tipo:
        tipo_lower = tipo.lower()
        if tipo_lower not in ["ambiental", "social"]:
            raise HTTPException(
                status_code=400,
                detail="Tipo deve ser 'ambiental' ou 'social'"
            )
        objetivos = [obj for obj in OBJETIVOS_TSB if obj["tipo"] == tipo_lower]
    
    logger.info(f"Listando objetivos TSB - Tipo: {tipo}, Total: {len(objetivos)}")
    
    return {
        "total": len(objetivos),
        "tipo_filtro": tipo,
        "objetivos": objetivos,
        "fonte": "Resolução CMN 4.945/2021 - Banco Central do Brasil"
    }


@router.get("/objetivos/{objetivo_id}")
async def detalhar_objetivo(objetivo_id: int):
    """
    Retorna detalhes de um objetivo específico da TSB.
    
    Path params:
    - objetivo_id: ID do objetivo (1-11)
    """
    objetivo = get_objetivo_by_id(objetivo_id)
    
    if not objetivo:
        raise HTTPException(
            status_code=404,
            detail=f"Objetivo {objetivo_id} não encontrado"
        )
    
    logger.info(f"Detalhando objetivo TSB {objetivo_id} - {objetivo['codigo']}")
    
    # Buscar setores relacionados
    setores_relacionados = [
        {"id": setor["id"], "nome": setor["nome"]}
        for setor in SETORES_TSB
        if objetivo_id in setor.get("objetivos_principais", [])
    ]
    
    return {
        **objetivo,
        "setores_relacionados": setores_relacionados,
        "total_setores": len(setores_relacionados)
    }


@router.get("/objetivos/codigo/{codigo}")
async def buscar_objetivo_por_codigo(codigo: str):
    """
    Busca objetivo TSB por código (MA, EA, EC, etc).
    
    Path params:
    - codigo: Código do objetivo (MA, EA, EC, PP, BP, CAA, AR, TE, IB, DI, IS)
    """
    objetivo = get_objetivo_by_codigo(codigo)
    
    if not objetivo:
        raise HTTPException(
            status_code=404,
            detail=f"Objetivo com código '{codigo}' não encontrado"
        )
    
    return objetivo


@router.get("/setores")
async def listar_setores():
    """
    Lista todos os 8 setores prioritários da TSB.
    
    **Setores:**
    1. Energia
    2. Transportes
    3. Construção Civil
    4. Agropecuária e Florestas
    5. Água e Saneamento
    6. Gestão de Resíduos
    7. Indústria
    8. Turismo
    """
    logger.info(f"Listando setores TSB - Total: {len(SETORES_TSB)}")
    
    return {
        "total": len(SETORES_TSB),
        "setores": SETORES_TSB,
        "fonte": "Taxonomia Sustentável Brasileira - BCB"
    }


@router.get("/setores/{setor_id}")
async def detalhar_setor(setor_id: int):
    """
    Retorna detalhes de um setor específico da TSB.
    
    Path params:
    - setor_id: ID do setor (1-8)
    """
    setor = get_setor_by_id(setor_id)
    
    if not setor:
        raise HTTPException(
            status_code=404,
            detail=f"Setor {setor_id} não encontrado"
        )
    
    logger.info(f"Detalhando setor TSB {setor_id} - {setor['nome']}")
    
    # Buscar objetivos relacionados
    objetivos_relacionados = [
        get_objetivo_by_id(obj_id)
        for obj_id in setor.get("objetivos_principais", [])
    ]
    
    return {
        **setor,
        "objetivos_detalhados": objetivos_relacionados,
        "total_objetivos": len(objetivos_relacionados)
    }


@router.get("/criterios")
async def listar_criterios():
    """
    Lista os 3 critérios de elegibilidade da TSB.
    
    **Critérios:**
    1. CS - Contribuição Substancial (40 pontos)
    2. NPS - Não Prejudicar Significativamente (30 pontos)
    3. SM - Salvaguardas Mínimas (30 pontos)
    
    Total máximo: 100 pontos
    """
    return {
        "total": len(CRITERIOS_TSB),
        "criterios": CRITERIOS_TSB,
        "score_maximo": 100,
        "metodologia": {
            "CS": "Atividade contribui substancialmente para pelo menos 1 objetivo",
            "NPS": "Atividade não causa dano significativo aos demais objetivos",
            "SM": "Atividade cumpre salvaguardas de direitos humanos e governança"
        }
    }


@router.get("/estatisticas")
async def estatisticas_tsb():
    """
    Estatísticas agregadas da integração TSB.
    
    Retorna resumo quantitativo da taxonomia.
    """
    return {
        "resumo": {
            "total_objetivos": len(OBJETIVOS_TSB),
            "objetivos_ambientais": len(get_objetivos_ambientais()),
            "objetivos_sociais": len(get_objetivos_sociais()),
            "total_setores": len(SETORES_TSB),
            "total_criterios": len(CRITERIOS_TSB)
        },
        "distribuicao_objetivos": {
            "ambiental": [obj["codigo"] for obj in get_objetivos_ambientais()],
            "social": [obj["codigo"] for obj in get_objetivos_sociais()]
        },
        "setores_por_objetivo": [
            {
                "setor": setor["nome"],
                "objetivos_principais": [
                    get_objetivo_by_id(obj_id)["codigo"]
                    for obj_id in setor.get("objetivos_principais", [])
                ]
            }
            for setor in SETORES_TSB
        ],
        "fonte": "Resolução CMN 4.945/2021",
        "ultima_atualizacao": "2025-11-12",
        "integracao_status": "TSB Light - Endpoints Básicos Ativos"
    }
