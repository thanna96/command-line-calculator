from decimal import Decimal
import types
import sys

import pytest

from app.observers import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation


def test_logging_observer(tmp_path):
    log_file = tmp_path / "log.txt"
    obs = LoggingObserver(log_file)
    calc = Calculation("Addition", Decimal("1"), Decimal("2"))
    obs.update(calc, [calc])
    content = log_file.read_text().strip()
    assert "Addition" in content


def test_auto_save_observer(monkeypatch, tmp_path):
    captured = {}

    class FakeDF:
        def __init__(self, data):
            captured["data"] = data

        def to_csv(self, path, index=False, encoding=None):
            captured["path"] = path

    fake_pd = types.SimpleNamespace(DataFrame=lambda d: FakeDF(d))
    monkeypatch.setitem(sys.modules, "pandas", fake_pd)

    obs = AutoSaveObserver(tmp_path / "hist.csv")
    calc = Calculation("Addition", Decimal("1"), Decimal("2"))
    obs.update(calc, [calc])
    assert captured["path"].name == "hist.csv"