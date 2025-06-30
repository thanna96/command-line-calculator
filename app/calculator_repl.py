########################
# Calculator REPL       #
########################

from decimal import Decimal

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError, DataError
from app.calculator_config import config
from app.operations import OperationFactory


def calculator_repl():  # pragma: no cover - interactive loop
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_dif - Perform arithmetic operations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue # pragma: no cover

                if command == 'exit':
                    # Attempt to save history before exiting
                    print("Goodbye!")
                    break

                if command == 'history':
                    for idx, calc_entry in enumerate(calc.get_history(), start=1):
                        print(f"{idx}: {calc_entry}")
                    continue # pragma: no cover

                if command == 'clear':
                    calc.clear_history()
                    print("History cleared.")
                    continue # pragma: no cover

                if command == 'undo':
                    try:
                        calc.undo()
                        print("Last calculation undone.")
                    except IndexError:
                        print("Nothing to undo.")
                    continue # pragma: no cover

                if command == 'redo':
                    try:
                        calc.redo()
                        print("Redo successful.")
                    except IndexError:
                        print("Nothing to redo.")
                    continue # pragma: no cover

                if command == 'save':
                    path = input("File to save to (blank for default): ").strip()
                    if not path:
                        path = str(config.history_dir / "history.csv")
                    try:
                        calc.save_history(path)
                        print(f"History saved to {path}")
                    except DataError as e:
                        print(f"Error: {e}")
                    continue # pragma: no cover

                if command == 'load':
                    path = input("File to load from (blank for default): ").strip()
                    if not path:
                        path = str(config.history_dir / "history.csv")
                    try:
                        calc.load_history(path)
                        print(f"History loaded from {path}")
                    except DataError as e:
                        print(f"Error: {e}")
                    continue # pragma: no cover

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root','int_divide', 'percent', 'abs_dif']:
                    # Perform the specified arithmetic operation
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue # pragma: no cover
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue # pragma: no cover

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(f"Unexpected error: {e}")
                    continue # pragma: no cover

                # Handle unknown commands
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print("\nOperation cancelled")
                continue # pragma: no cover
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"Error: {e}")
                continue # pragma: no cover

    except Exception as e:
        # Handle fatal errors during initialization
        print(f"Fatal error: {e}")
        raise
