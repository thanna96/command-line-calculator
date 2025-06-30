from __future__ import annotations

from typing import List

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.calculator_config import config
from pathlib import Path


class History:
    """Manages a list of calculations with undo/redo support."""

    def __init__(self) -> None:
        self._calculations: List[Calculation] = []
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    # ------------------------------------------------------------------
    # Memento helpers
    def _create_memento(self) -> CalculatorMemento:
        return CalculatorMemento(self._calculations.copy())

    def _restore_memento(self, memento: CalculatorMemento) -> None:
        self._calculations = memento.state.copy()

    # ------------------------------------------------------------------
    # History manipulation
    def add_calculation(self, calculation: Calculation) -> None:
        """Add a new calculation and update undo stack."""
        self._undo_stack.append(self._create_memento())
        self._calculations.append(calculation)
        self._redo_stack.clear()
          
        # Trim history if it exceeds the configured maximum size
        if config.max_history_size and len(self._calculations) > config.max_history_size:
            self._calculations = self._calculations[-config.max_history_size :]

    def clear(self) -> None:
        self._calculations.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_history(self) -> List[Calculation]:
        return self._calculations.copy()

    # ------------------------------------------------------------------
    # Undo/Redo operations
    def undo(self) -> None:
        if not self._undo_stack:
            raise IndexError("No operations to undo")
        self._redo_stack.append(self._create_memento())
        memento = self._undo_stack.pop()
        self._restore_memento(memento)

    def redo(self) -> None:
        if not self._redo_stack:
            raise IndexError("No operations to redo")
        self._undo_stack.append(self._create_memento())
        memento = self._redo_stack.pop()
        self._restore_memento(memento)

    # ------------------------------------------------------------------
    # Persistence operations
    def to_dataframe(self):
        """Return the history as a pandas DataFrame."""
        import pandas as pd

        data = [c.to_dict() for c in self._calculations]
        return pd.DataFrame(
            data,
            columns=["operation", "operand1", "operand2", "result", "timestamp"],
        )

    def from_dataframe(self, df) -> None:
        """Load history from a pandas DataFrame."""
        calculations = [
            Calculation.from_dict(row.to_dict())
            for _, row in df.iterrows()
        ]
        self._calculations = calculations
        self._undo_stack.clear()
        self._redo_stack.clear()

    def save_to_csv(self, file_path: str | Path | None = None) -> None:
        """Save history to a CSV file."""
        try:
            import pandas as pd
            path = Path(file_path) if file_path else config.history_dir / config.history_file
            df = self.to_dataframe()
            df.to_csv(path, index=False, encoding=config.default_encoding)
        except Exception as exc:  # pragma: no cover - I/O errors
            from app.exceptions import DataError
            raise DataError(f"Failed to save history to CSV: {exc}") from exc

    def load_from_csv(self, file_path: str | Path | None = None) -> None:
        """Load history from a CSV file."""
        try:
            import pandas as pd
            path = Path(file_path) if file_path else config.history_dir / config.history_file
            df = pd.read_csv(path, encoding=config.default_encoding)
            self.from_dataframe(df)
        except FileNotFoundError as exc:
            from app.exceptions import DataError
            raise DataError(f"File not found: {path}") from exc
        except Exception as exc:  # pragma: no cover - I/O errors
            from app.exceptions import DataError
            raise DataError(f"Failed to load history from CSV: {exc}") from exc
