from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


@dataclass
class CalculatorConfig:
    log_dir: Path = Path("logs")
    history_dir: Path = Path("history")
    max_history_size: int = 100
    auto_save: bool = True
    precision: int = 10
    max_input_value: int = 1_000_000
    default_encoding: str = "utf-8"


def load_config(dotenv_path: str | Path = ".env") -> CalculatorConfig:
    load_dotenv(dotenv_path, override=True)
    try:
        cfg = CalculatorConfig(
            log_dir=Path(os.getenv("CALCULATOR_LOG_DIR", "logs")),
            history_dir=Path(os.getenv("CALCULATOR_HISTORY_DIR", "history")),
            max_history_size=int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")),
            auto_save=os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true",
            precision=int(os.getenv("CALCULATOR_PRECISION", "10")),
            max_input_value=int(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")),
            default_encoding=os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
        )
    except ValueError as exc:  # pragma: no cover - configuration errors
        raise ConfigurationError(f"Invalid configuration value: {exc}") from exc

    cfg.log_dir.mkdir(parents=True, exist_ok=True)
    cfg.history_dir.mkdir(parents=True, exist_ok=True)

    return cfg


config = load_config()