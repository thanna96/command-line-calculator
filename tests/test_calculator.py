from decimal import Decimal
import pytest

from app.calculator import Calculator
from app.operations import OperationFactory
from app.exceptions import OperationError


def test_calculator_addition_history_and_undo_redo():
    calc = Calculator()
    calc.set_operation(OperationFactory.create_operation("add"))
    result = calc.perform_operation("2", "3")
    assert result == Decimal("5")
    assert len(calc.get_history()) == 1

    calc.undo()
    assert len(calc.get_history()) == 0

    calc.redo()
    assert len(calc.get_history()) == 1


def test_calculator_requires_operation():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.perform_operation("1", "1")


def test_calculator_clear_history():
    calc = Calculator()
    calc.set_operation(OperationFactory.create_operation("add"))
    calc.perform_operation("1", "1")
    calc.clear_history()
    assert calc.get_history() == []


def test_calculator_observer_called(tmp_path):
    calls = []

    class DummyObserver:
        def update(self, calculation, history):
            calls.append((calculation, history))

    calc = Calculator()
    calc._observers = [DummyObserver()]
    calc.set_operation(OperationFactory.create_operation("add"))
    calc.perform_operation("1", "2")
    assert calls and calls[0][0].result == Decimal("3")