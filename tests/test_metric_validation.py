import pytest
from src.metric_validation import validate_metric_input

def test_validate_metric_input_accepts_int():
    assert validate_metric_input(5) == 5.0

def test_validate_metric_input_accepts_float():
    assert validate_metric_input(2.5) == 2.5

def test_validate_metric_input_rejects_none():
    with pytest.raises(ValueError, match="value cannot be None"):
        validate_metric_input(None)

def test_validate_metric_input_rejects_non_numeric():
    with pytest.raises(TypeError, match="value must be numeric"):
        validate_metric_input("abc")

def test_validate_metric_input_rejects_negative():
    with pytest.raises(ValueError, match="value must be non-negative"):
        validate_metric_input(-1)
