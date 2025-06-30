########################
# Calculator Class      #
########################

from decimal import Decimal, getcontext
from app.logger import logger
from typing import Union, List


from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.input_validators import InputValidator
from app.operations import Operation
from app.history import History
from app.observers import Observer, LoggingObserver, AutoSaveObserver
from app.calculator_config import config

# Type aliases for better readability
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]


class Calculator:

    def __init__(self):
        """Initialize the Calculator and its history manager."""
        self.operation_strategy: Operation = None
        self.history = History()
        self._observers: List[Observer] = []
       
        # Apply configuration settings
        getcontext().prec = config.precision

        # Register default observers
        self.add_observer(LoggingObserver())
        if config.auto_save:
            self.add_observer(AutoSaveObserver())

        logger.info("Calculator initialized with configuration.")
        
    # ------------------------------------------------------------------
    # Observer management
    def add_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, calculation: Calculation) -> None:
        for obs in list(self._observers):
            try:
                obs.update(calculation, self.history.get_history())
            except Exception as exc:  # pragma: no cover - observer errors
                logger.error(f"Observer {obs} failed: {exc}")
        
    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation
        logger.info(f"Set operation: {operation}")

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
        
            self.history.add_calculation(calculation)
            self._notify_observers(calculation)

            return result

        except ValidationError as e:
            # Log and re-raise validation errors
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            # Log and raise operation errors for any other exceptions
            logger.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")

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
    
    def save_history(self, file_path: str | Path) -> None:
        """Save calculation history to a CSV file."""
        self.history.save_to_csv(file_path)

    def load_history(self, file_path: str | Path) -> None:
        """Load calculation history from a CSV file."""
        self.history.load_from_csv(file_path)