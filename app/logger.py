"""Application-wide logging utilities."""

from __future__ import annotations

import logging
from pathlib import Path

from app.calculator_config import config


class Logger:
    """Singleton-style logger configuration."""

    _logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Return a configured logger instance."""
        if cls._logger is None:
            cls._setup_logger()
        return cls._logger

    @classmethod
    def _setup_logger(cls) -> None:  # pragma: no cover - file I/O setup
        logger = logging.getLogger("calculator")
        logger.setLevel(logging.DEBUG)

        # Avoid duplicated handlers when running tests multiple times
        logger.handlers.clear()

        log_file: Path = config.log_file
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding=config.default_encoding)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)

        cls._logger = logger


# Expose a module-level logger for convenience
logger = Logger.get_logger()