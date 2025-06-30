from __future__ import annotations

from typing import List

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.calculator_config import config


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