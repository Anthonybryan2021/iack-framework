def compute_iack_metrics(total_events=1, window_size=1):
    if isinstance(total_events, bool):
        raise TypeError("total_events must be an int or float, not bool")
    if isinstance(window_size, bool):
        raise TypeError("window_size must be an int or float, not bool")

    if total_events <= 0:
        raise ValueError("total_events must be greater than 0")
    if window_size <= 0:
        raise ValueError("window_size must be greater than 0")

    integrity = min(1.0, total_events / 10)
    windowed_efficiency = min(1.0, total_events / window_size)

    return {
        "integrity": integrity,
        "availability": 1.0,
        "confidentiality_proxy": 1.0,
        "windowed_efficiency": windowed_efficiency,
    }