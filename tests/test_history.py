from decimal import Decimal
import importlib.util
import pytest

from app.history import History
from app.calculation import Calculation
from app.exceptions import DataError


def test_save_and_load(tmp_path):
    if importlib.util.find_spec("pandas") is None:
        pytest.skip("pandas not installed")
    hist = History()
    hist.add_calculation(Calculation("Addition", Decimal("1"), Decimal("2")))
    file_path = tmp_path / "hist.csv"
    hist.save_to_csv(file_path)

    new_hist = History()
    new_hist.load_from_csv(file_path)

    assert len(new_hist.get_history()) == 1
    assert new_hist.get_history()[0].operation == "Addition"


def test_load_missing_file(tmp_path):
    hist = History()
    missing_file = tmp_path / "missing.csv"
    with pytest.raises(DataError):
        hist.load_from_csv(missing_file)

def test_history_undo_redo():
    hist = History()
    calc = Calculation("Addition", Decimal("1"), Decimal("1"))
    hist.add_calculation(calc)
    hist.add_calculation(calc)
    assert len(hist.get_history()) == 2
    hist.undo()
    assert len(hist.get_history()) == 1
    hist.redo()
    assert len(hist.get_history()) == 2


def test_history_undo_error():
    hist = History()
    with pytest.raises(IndexError):
        hist.undo()


def test_history_redo_error():
    hist = History()
    with pytest.raises(IndexError):
        hist.redo()