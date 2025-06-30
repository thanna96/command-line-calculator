from decimal import Decimal
import pytest

from app.input_validators import InputValidator, ValidationError


def test_validate_number_empty():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("")


def test_validate_number_none():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(None)


def test_validate_number_success():
    result = InputValidator.validate_number("3")
    assert isinstance(result, Decimal)
    assert result == Decimal("3")