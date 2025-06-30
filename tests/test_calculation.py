from decimal import Decimal
import pytest

from app.calculation import Calculation
from app.exceptions import OperationError


def test_calculation_basic():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert calc.result == Decimal("5")
    assert "Addition" in str(calc)


def test_calculation_to_from_dict():
    calc = Calculation("Multiplication", Decimal("2"), Decimal("4"))
    data = calc.to_dict()
    new_calc = Calculation.from_dict(data)
    assert calc == new_calc


def test_calculation_from_dict_invalid():
    with pytest.raises(OperationError):
        Calculation.from_dict({"operand1": "1"})


def test_format_result_precision():
    calc = Calculation("Division", Decimal("1"), Decimal("2"))
    assert calc.format_result(2) == "0.5"

def test_format_result_no_precision():
    calc = Calculation("Division", Decimal("1"), Decimal("3"))
    assert calc.format_result() == "0.3333333333333333"

def test_calculation_invalid_operation():
    with pytest.raises(OperationError):
        Calculation("InvalidOperation", Decimal("1"), Decimal("2"))

def test_calculation_zero_division():
    with pytest.raises(OperationError):
        Calculation("Division", Decimal("1"), Decimal("0"))

