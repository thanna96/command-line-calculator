########################
# Calculator Class      #
########################

from decimal import Decimal
import logging
from pathlib import Path
from typing import Union


from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.input_validators import InputValidator
from app.operations import Operation
from app.history import History

# Type aliases for better readability
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]


class Calculator:

    def __init__(self):
        """Initialize the Calculator and its history manager."""
        self.operation_strategy: Operation = None
        self.history = History()
        logging.info("Calculator initialized with default configuration.")
        


    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    def perform_operation(
        self,
        a: Union[str, Number],
        b: Union[str, Number]
    ) -> CalculationResult:
        if not self.operation_strategy:
            raise OperationError("No operation set")

        try:
            # Validate and convert inputs to Decimal
            validated_a = InputValidator.validate_number(a)
            validated_b = InputValidator.validate_number(b)

            # Execute the operation strategy
            result = self.operation_strategy.execute(validated_a, validated_b)

            # Create a new Calculation instance with the operation details
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=validated_a,
                operand2=validated_b
            )

            # Record the calculation for history management
            self.history.add_calculation(calculation)

            return result

        except ValidationError as e:
            # Log and re-raise validation errors
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            # Log and raise operation errors for any other exceptions
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")

    # ------------------------------------------------------------------
    # History helpers
    def undo(self) -> None:
        """Undo the last calculation."""
        self.history.undo()

    def redo(self) -> None:
        """Redo the last undone calculation."""
        self.history.redo()

    def clear_history(self) -> None:
        """Clear all recorded calculations."""
        self.history.clear()

    def get_history(self) -> list[Calculation]:
        """Return a copy of the calculation history."""
        return self.history.get_history()

    