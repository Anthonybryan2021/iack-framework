def validate_metric_input(value):
    if value is None:
        raise ValueError("value cannot be None")
    if not isinstance(value, (int, float)):
        raise TypeError("value must be numeric")
    if value < 0:
        raise ValueError("value must be non-negative")
    return float(value)
