from dataclasses import dataclass
from typing import List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """Snapshot of the calculator history state."""
    
    state: List[Calculation]