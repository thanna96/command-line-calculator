# Command Line Calculator

## Project Description
This project provides a fully featured command–line calculator. It supports
common arithmetic operations such as addition, subtraction, multiplication,
division, exponentiation, roots and several others. Calculation history is
maintained with undo/redo functionality and can be saved to or loaded from CSV
files. Logging is configurable and operations can be extended through a simple
factory pattern.

## Installation
1. Clone this repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Application behaviour is controlled via environment variables stored in an
`.env` file. Copy the provided sample or create a new one in the project root
with entries like the following:

```
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_DIR=history
CALCULATOR_HISTORY_FILE=history.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=16
CALCULATOR_MAX_INPUT_VALUE=100000000000000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

The logger writes to `CALCULATOR_LOG_DIR/CALCULATOR_LOG_FILE`. History files are
stored using the directory and file names defined above. Adjust these variables
as needed and ensure the directories exist or will be created on first run.

## Usage
Start the interactive calculator by running:
```bash
python main.py
```
Type `help` inside the REPL to see a list of available commands. Supported
operations include `add`, `subtract`, `multiply`, `divide`, `power`, `root`,
`modulus`, `int_divide`, `percent` and `abs_dif`. Additional commands manage the
history (`history`, `clear`, `undo`, `redo`), persistence (`save`, `load`) and
session control (`help`, `exit`).

## Testing
Run the unit test suite with coverage using:
```bash
pytest --cov=app --cov-report=term-missing
```
To ensure the same coverage checks performed in CI use:
```bash
pytest --cov=app --cov-fail-under=90
```

## CI/CD
The GitHub Actions workflow defined in
[`.github/workflows/python-app.yml`](.github/workflows/python-app.yml) sets up
Python 3.11, installs dependencies and runs the test suite. The workflow fails
if coverage drops below 90%, helping maintain code quality.
