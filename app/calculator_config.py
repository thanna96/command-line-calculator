from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    def load_dotenv(path: str | Path, override: bool = True) -> None:
        """Minimal .env loader used when python-dotenv is unavailable."""
        path = Path(path)
        if not path.exists():
            return
        for line in path.read_text().splitlines():
            if '=' not in line or line.strip().startswith('#'):
                continue
            key, value = line.split('=', 1)
            if override or key not in os.environ:
                os.environ[key] = value

from app.exceptions import ConfigurationError


@dataclass
class CalculatorConfig:
    log_dir: Path = Path("logs")
    log_file: Path = Path("calculator.log")
    history_dir: Path = Path("history")
    history_file: Path = Path("history.csv")
    max_history_size: int = 100
    auto_save: bool = True
    precision: int = 16
    max_input_value: int = 10 ** 20
    default_encoding: str = "utf-8"


def load_config(dotenv_path: str | Path = ".env") -> CalculatorConfig:
    load_dotenv(dotenv_path, override=True)
    try:
        cfg = CalculatorConfig(
            log_dir=Path(os.getenv("CALCULATOR_LOG_DIR", "logs")),
            log_file=Path(os.getenv("CALCULATOR_LOG_FILE", "calculator.log")),
            history_dir=Path(os.getenv("CALCULATOR_HISTORY_DIR", "history")),
            history_file=Path(os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")),
            max_history_size=int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")),
            auto_save=os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true",
            precision=int(os.getenv("CALCULATOR_PRECISION", "16")),
            max_input_value=int(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "100000000000000000000")),
            default_encoding=os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
        )
    except ValueError as exc:  # pragma: no cover - configuration errors
        raise ConfigurationError(f"Invalid configuration value: {exc}") from exc

    cfg.log_dir.mkdir(parents=True, exist_ok=True)
    cfg.history_dir.mkdir(parents=True, exist_ok=True)
    if not cfg.log_file.is_absolute():
        cfg.log_file = cfg.log_dir / cfg.log_file
    if not cfg.history_file.is_absolute():
        cfg.history_file = cfg.history_dir / cfg.history_file
    cfg.log_file.parent.mkdir(parents=True, exist_ok=True)
    cfg.history_file.parent.mkdir(parents=True, exist_ok=True)
    return cfg


config = load_config()