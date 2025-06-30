from app.exceptions import CalculatorError, ValidationError, OperationError, ConfigurationError, DataError


def test_exception_hierarchy():
    for exc in (ValidationError, OperationError, ConfigurationError, DataError):
        assert issubclass(exc, CalculatorError)