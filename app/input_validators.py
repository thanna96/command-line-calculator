########################
# Input Validation     #
########################

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.exceptions import ValidationError
from app.calculator_config import config

@dataclass
class InputValidator:
    """Validates and sanitizes calculator inputs."""
    
    @staticmethod
    def validate_number(value: Any) -> Decimal:
        """
        Validate and convert input to Decimal.
        
        Args:
            value: Input value to validate
            config: Calculator configuration
            
        Returns:
            Decimal: Validated and converted number
            
        Raises:
            ValidationError: If input is invalid
        """
        try:
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValidationError("Input cannot be empty")
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))

            # Enforce maximum input value if configured
            if abs(number) > config.max_input_value:
                raise ValidationError(
                    f"Input {value} exceeds maximum allowed value {config.max_input_value}"
                )
            
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e
