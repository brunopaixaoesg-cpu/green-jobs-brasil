"""
Utilities para paginação, filtros e ordenação da API
"""
from typing import Optional, List, Dict, Any, Tuple
from fastapi import Query, HTTPException
from sqlalchemy.orm import Query as SQLQuery
from sqlalchemy import asc, desc


class PaginationParams:
    """Parâmetros de paginação padrão"""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
        limit: int = Query(20, ge=1, le=100, description="Items por página (máx 100)")
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit


class SortParams:
    """Parâmetros de ordenação"""
    
    def __init__(
        self,
        sort: Optional[str] = Query(None, description="Campo para ordenação"),
        order: str = Query("asc", regex="^(asc|desc)$", description="Direção: asc ou desc")
    ):
        self.sort = sort
        self.order = order


def parse_comma_separated(value: Optional[str]) -> List[str]:
    """
    Converte string separada por vírgulas em lista
    
    Args:
        value: String como "ODS7,ODS13" ou None
        
    Returns:
        Lista de valores ou lista vazia
    """
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def apply_filters(
    query: SQLQuery,
    filters: Dict[str, Any],
    model: Any
) -> SQLQuery:
    """
    Aplica filtros dinâmicos à query SQLAlchemy
    
    Args:
        query: Query SQLAlchemy
        filters: Dicionário de filtros {campo: valor}
        model: Modelo SQLAlchemy para referência de campos
        
    Returns:
        Query com filtros aplicados
    """
    for field, value in filters.items():
        if value is not None:
            # Verifica se o campo existe no modelo
            if not hasattr(model, field):
                continue
                
            # Aplica filtro baseado no tipo
            if isinstance(value, list) and len(value) > 0:
                # Filtro IN para listas
                query = query.filter(getattr(model, field).in_(value))
            elif isinstance(value, str) and "%" in value:
                # Filtro LIKE para padrões
                query = query.filter(getattr(model, field).like(value))
            else:
                # Filtro de igualdade simples
                query = query.filter(getattr(model, field) == value)
                
    return query


def apply_sorting(
    query: SQLQuery,
    sort_field: Optional[str],
    order: str,
    model: Any,
    default_sort: str = "id"
) -> SQLQuery:
    """
    Aplica ordenação à query
    
    Args:
        query: Query SQLAlchemy
        sort_field: Campo para ordenar (None usa default)
        order: 'asc' ou 'desc'
        model: Modelo SQLAlchemy
        default_sort: Campo padrão se sort_field não fornecido
        
    Returns:
        Query com ordenação aplicada
    """
    # Usa campo padrão se não especificado
    field = sort_field or default_sort
    
    # Verifica se o campo existe
    if not hasattr(model, field):
        raise HTTPException(
            status_code=400,
            detail=f"Campo '{field}' não existe para ordenação"
        )
    
    # Aplica ordenação
    column = getattr(model, field)
    if order == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))
        
    return query


def paginate_query(
    query: SQLQuery,
    page: int,
    limit: int
) -> Tuple[List[Any], Dict[str, int]]:
    """
    Executa paginação e retorna resultados + metadados
    
    Args:
        query: Query SQLAlchemy configurada com filtros/sorting
        page: Número da página (1-indexed)
        limit: Items por página
        
    Returns:
        Tupla (items, pagination_meta) onde pagination_meta contém:
        - total: Total de items
        - page: Página atual
        - pages: Total de páginas
        - limit: Items por página
    """
    # Conta total (antes de aplicar offset/limit)
    total = query.count()
    
    # Aplica paginação
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    
    # Calcula total de páginas
    pages = (total + limit - 1) // limit  # Ceiling division
    
    # Metadata
    meta = {
        "total": total,
        "page": page,
        "pages": pages,
        "limit": limit
    }
    
    return items, meta


def create_pagination_headers(meta: Dict[str, int]) -> Dict[str, str]:
    """
    Cria headers HTTP com informações de paginação
    
    Args:
        meta: Dicionário com total, page, pages, limit
        
    Returns:
        Dicionário de headers para Response
    """
    return {
        "X-Total-Count": str(meta["total"]),
        "X-Page": str(meta["page"]),
        "X-Total-Pages": str(meta["pages"]),
        "X-Per-Page": str(meta["limit"])
    }


def build_pagination_response(
    items: List[Any],
    meta: Dict[str, int],
    serializer=None
) -> Dict[str, Any]:
    """
    Constrói resposta padronizada com paginação
    
    Args:
        items: Lista de items do banco
        meta: Metadados de paginação
        serializer: Função opcional para serializar items
        
    Returns:
        Dict com data e pagination
    """
    # Serializa items se necessário
    if serializer:
        data = [serializer(item) for item in items]
    else:
        data = items
    
    return {
        "data": data,
        "pagination": meta
    }
