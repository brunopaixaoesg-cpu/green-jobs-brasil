"""Central logger for the Green Jobs Brasil project.

Use `from api.logger import logger` in modules and call logger.info()/warning()/error().
Configuration is environment-driven via GJB_LOG_LEVEL.
"""
import logging
import os

LOG_LEVEL = os.getenv("GJB_LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("green_jobs")
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

__all__ = ["logger"]
