from pathlib import Path
from dataclasses import replace

import pytest

from app.calculator_config import load_config, CalculatorConfig
from app.input_validators import InputValidator, ValidationError
from app import history as history_module
from app.calculation import Calculation


def test_load_config_defaults(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("")
    cfg = load_config(env_file)
    assert isinstance(cfg, CalculatorConfig)
    assert cfg.log_dir.name == "logs"
    assert cfg.log_file.name == "calculator.log"
    assert cfg.auto_save is True


def test_load_config_override(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "CALCULATOR_LOG_DIR=data_logs",
                "CALCULATOR_LOG_FILE=my.log",
                "CALCULATOR_HISTORY_DIR=data_history",
                "CALCULATOR_MAX_HISTORY_SIZE=5",
                "CALCULATOR_AUTO_SAVE=false",
                "CALCULATOR_PRECISION=5",
                "CALCULATOR_MAX_INPUT_VALUE=10",
                "CALCULATOR_DEFAULT_ENCODING=latin-1",
            ]
        )
    )
    cfg = load_config(env_file)
    assert cfg.log_dir.name == "data_logs"
    assert cfg.log_file.name == "my.log"
    assert cfg.history_dir.name == "data_history"
    assert cfg.max_history_size == 5
    assert cfg.auto_save is False
    assert cfg.precision == 5
    assert cfg.max_input_value == 10
    assert cfg.default_encoding == "latin-1"


def test_input_validator_respects_max(monkeypatch):
    from app import input_validators
    cfg = replace(input_validators.config, max_input_value=5)
    monkeypatch.setattr(input_validators, "config", cfg)

    with pytest.raises(ValidationError):
        InputValidator.validate_number("10")


def test_history_respects_size(monkeypatch):
    from decimal import Decimal
    from dataclasses import replace

    cfg = replace(history_module.config, max_history_size=2)
    monkeypatch.setattr(history_module, "config", cfg)

    hist = history_module.History()
    c = Calculation("Addition", Decimal("1"), Decimal("1"))
    hist.add_calculation(c)
    hist.add_calculation(c)
    hist.add_calculation(c)
    assert len(hist.get_history()) == 2