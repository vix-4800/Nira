import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str, max_bytes: int, backup_count: int) -> logging.Logger:
    """Create and configure a logger with a rotating file handler."""
    logger = logging.getLogger(name)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

__all__ = ["setup_logger"]
