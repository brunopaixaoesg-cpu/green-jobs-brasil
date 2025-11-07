"""Central logger for the Green Jobs Brasil project.

DEPRECATED: Este arquivo é mantido para compatibilidade retroativa.
Use `from api.logging_config import logger` para novos códigos.

O novo sistema suporta:
- Logs JSON para produção
- Rotation automático
- Níveis configuráveis via env
- Funções de utilidade (log_request, log_db_query, etc)
"""
import warnings

# Importar o novo logger
from api.logging_config import logger, log_request, log_db_query, log_error, log_metric

# Avisar sobre deprecação em desenvolvimento
warnings.warn(
    "api.logger está deprecated. Use 'from api.logging_config import logger' em vez disso.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["logger", "log_request", "log_db_query", "log_error", "log_metric"]

