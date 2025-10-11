# Green Jobs Brasil - Copilot Instructions

## Project Overview
Sistema para identificação e classificação de empresas verdes no Brasil baseado em códigos CNAE e mapeamento para Objetivos de Desenvolvimento Sustentável (ODS).

## Architecture
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **ETL**: Python + DuckDB para processamento de dados
- **Data**: CNAEs verdes classificados + empresas exemplo
- **API**: Endpoints REST para consulta de empresas e CNAEs verdes

## Key Components
- `/api/app.py` - Aplicação FastAPI principal
- `/etl/main.py` - Pipeline ETL completo
- `/etl_simple.py` - ETL simplificado para testes
- `/gjb_dev.db` - Banco SQLite com dados
- `/start_api.py` - Script para iniciar API

## Development Guidelines
- Use Python 3.13 como base
- Mantenha consistência com SQLAlchemy models
- Siga padrões FastAPI para endpoints
- Documente adequadamente as funções
- Use tipo hints em Python

## Running the System
```bash
# Iniciar API
python start_api.py

# Acessar documentação
http://127.0.0.1:8000/docs
```

## Data Structure
- 43 CNAEs verdes classificados (Core/Adjacent/Secondary)
- 10 empresas exemplo com pontuação verde
- Sistema de pontuação 0-100 baseado em CNAEs

## Contribution Notes
- Código limpo e bem documentado
- Testes unitários desejáveis
- Seguir padrões Python (PEP 8)
- Manter APIs RESTful consistentes