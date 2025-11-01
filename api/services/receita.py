"""
Serviço para integração com a Receita Federal (API externa configurável).

Comportamento:
- Se a variável de ambiente `RECEITA_INTEGRATION_ENABLED` for 'true' (case-insensitive)
  e `RECEITA_API_URL` estiver configurada, faz uma chamada HTTP GET para a URL
  formatada com o CNPJ (por padrão usa receitaws: https://www.receitaws.com.br/v1/cnpj/{cnpj}).
- Caso contrário, retorna um mock simples (útil para desenvolvimento off-line).

Use variáveis de ambiente para controlar o comportamento em produção:
  RECEITA_INTEGRATION_ENABLED (true|false)
  RECEITA_API_URL (ex: https://www.receitaws.com.br/v1/cnpj/{cnpj})
  RECEITA_TIMEOUT (segundos)
"""

import os
import logging
from typing import Dict, Any

logger = logging.getLogger("api.services.receita")

DEFAULT_URL = "https://www.receitaws.com.br/v1/cnpj/{cnpj}"


def _is_enabled() -> bool:
    return os.getenv("RECEITA_INTEGRATION_ENABLED", "false").lower() == "true"


def fetch_company(cnpj: str, timeout: int | None = None) -> Dict[str, Any]:
    """Fetch company data from the configured Receita service or return mock.

    Args:
        cnpj: numeric-only CNPJ string
        timeout: optional timeout in seconds

    Returns:
        Dict with the parsed response (varies by provider). If integration is
        disabled, returns a deterministic mock object.
    """
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    api_url = os.getenv("RECEITA_API_URL", DEFAULT_URL)
    if timeout is None:
        try:
            timeout = int(os.getenv("RECEITA_TIMEOUT", "6"))
        except ValueError:
            timeout = 6

    if not _is_enabled():
        logger.info("Receita integration disabled - returning mock for %s", cnpj_clean)
        return {
            "mock": True,
            "cnpj": cnpj_clean,
            "nome": "Empresa Externa (mock)",
            "atividade_principal": [{"code": "0000", "text": "Atividade exemplo"}],
            "situacao": "NAO_INFORMADO",
        }

    # Real HTTP call
    try:
        import requests

        url = api_url.format(cnpj=cnpj_clean)
        logger.info("Consultando Receita: %s", url)
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            # Normalizar chaves básicas
            return data
        else:
            logger.warning("Receita service returned status %s for %s", resp.status_code, cnpj_clean)
            return {"error": f"receita_status_{resp.status_code}", "status_code": resp.status_code}

    except Exception as e:
        logger.exception("Erro ao consultar Receita para %s: %s", cnpj_clean, e)
        return {"error": "exception", "message": str(e)}
