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


def test_validate_number_invalid_format():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("abc")


def test_validate_number_too_large(monkeypatch):
    from dataclasses import replace
    from app import input_validators

    cfg = replace(input_validators.config, max_input_value=5)
    monkeypatch.setattr(input_validators, "config", cfg)

    with pytest.raises(ValidationError):
        InputValidator.validate_number("10")

def test_validate_number_negative():
    result = InputValidator.validate_number("-3.5")
    assert isinstance(result, Decimal)
    assert result == Decimal("-3.5")

def test_validate_number_zero():
    result = InputValidator.validate_number("0")
    assert isinstance(result, Decimal)
    assert result == Decimal("0")

def test_validate_number_whitespace():
    result = InputValidator.validate_number("   2.5   ")
    assert isinstance(result, Decimal)
    assert result == Decimal("2.5")

def test_validate_number_large_integer():
    result = InputValidator.validate_number("12345678901234567890")
    assert isinstance(result, Decimal)
    assert result == Decimal("12345678901234567890")

def test_validate_number_large_float():
    result = InputValidator.validate_number("1.2345678901234567890")
    assert isinstance(result, Decimal)
    assert result == Decimal("1.2345678901234567890")

def test_validate_number_exponent():
    result = InputValidator.validate_number("1e10")
    assert isinstance(result, Decimal)
    assert result == Decimal("10000000000")

def test_validate_number_negative_exponent():
    result = InputValidator.validate_number("1e-10")
    assert isinstance(result, Decimal)
    assert result == Decimal("0.0000000001")

