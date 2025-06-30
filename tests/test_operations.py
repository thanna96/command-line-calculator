from decimal import Decimal
import pytest

from app.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
    OperationFactory,
)
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "cls,a,b,expected",
    [
        (Addition, 1, 2, 3),
        (Subtraction, 5, 3, 2),
        (Multiplication, 2, 4, 8),
        (Division, 6, 3, 2),
        (Power, 2, 3, 8),
        (Root, 9, 2, 3),
        (Modulus, 7, 4, 3),
        (IntegerDivision, 7, 3, 2),
        (Percentage, 25, 100, 25),
        (AbsoluteDifference, 10, 6, 4),
    ],
)
def test_operations_execute(cls, a, b, expected):
    op = cls()
    result = op.execute(Decimal(a), Decimal(b))
    assert result == Decimal(expected)


@pytest.mark.parametrize(
    "cls,a,b",
    [
        (Division, 1, 0),
        (Modulus, 5, 0),
        (IntegerDivision, 5, 0),
        (Percentage, 5, 0),
    ],
)
def test_operations_validation_error(cls, a, b):
    op = cls()
    with pytest.raises(ValidationError):
        op.execute(Decimal(a), Decimal(b))


def test_power_negative_exponent():
    op = Power()
    with pytest.raises(ValidationError):
        op.execute(Decimal(2), Decimal(-1))


@pytest.mark.parametrize("a,b", [(-1, 2), (4, 0)])
def test_root_invalid(a, b):
    op = Root()
    with pytest.raises(ValidationError):
        op.execute(Decimal(a), Decimal(b))


@pytest.mark.parametrize(
    "name,cls",
    [
        ("add", Addition),
        ("subtract", Subtraction),
        ("multiply", Multiplication),
        ("divide", Division),
        ("power", Power),
        ("root", Root),
        ("modulus", Modulus),
        ("int_divide", IntegerDivision),
        ("percent", Percentage),
        ("abs_dif", AbsoluteDifference),
    ],
)
def test_operation_factory(name, cls):
    op = OperationFactory.create_operation(name)
    assert isinstance(op, cls)


def test_operation_factory_unknown():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown")


def test_operation_factory_register():
    class Dummy(OperationFactory._operations["add"].__base__):
        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return Decimal(42)

    OperationFactory.register_operation("dummy", Dummy)
    op = OperationFactory.create_operation("dummy")
    assert isinstance(op, Dummy)
