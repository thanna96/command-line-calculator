from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
import logging

from app.calculation import Calculation
from app.calculator_config import config

class Observer(ABC):
    """Interface for observers reacting to new calculations."""

    @abstractmethod
    def update(self, calculation: Calculation, history: List[Calculation]) -> None:
        """React to a new calculation event."""
        raise NotImplementedError


class LoggingObserver(Observer):
    """Logs calculation details to a file."""

    def __init__(self, log_file: Path | str = config.log_dir / "calculator.log") -> None:
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def update(self, calculation: Calculation, history: List[Calculation]) -> None:
        message = (
            f"{calculation.timestamp.isoformat()},"
            f"{calculation.operation},"
            f"{calculation.operand1},"
            f"{calculation.operand2},"
            f"{calculation.result}\n"
        )
        with open(self.log_file, "a", encoding=config.default_encoding) as fh:
            fh.write(message)
        logging.debug(f"Logged calculation to {self.log_file}: {message.strip()}")


class AutoSaveObserver(Observer):
    """Saves calculation history to a CSV file using pandas."""

    def __init__(self, csv_file: Path | str = config.history_dir / "history.csv") -> None:
        self.csv_file = Path(csv_file)
        self.csv_file.parent.mkdir(parents=True, exist_ok=True)

    def update(self, calculation: Calculation, history: List[Calculation]) -> None:
        try:
            import pandas as pd
        except Exception as exc:  # pragma: no cover - dependency issues
            logging.error(f"Pandas not available: {exc}")
            return

        try:
            data = [calc.to_dict() for calc in history]
            df = pd.DataFrame(data)
            df.to_csv(self.csv_file, index=False, encoding=config.default_encoding)
            logging.debug(f"Auto-saved history to {self.csv_file}")
        except Exception as exc:  # pragma: no cover - I/O errors
            logging.error(f"Auto-save failed: {exc}")