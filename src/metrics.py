from dataclasses import dataclass
from typing import Optional


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(value, maximum))


@dataclass
class IntegrityInputs:
    breach_events: int
    modification_events: int
    hash_failures: int
    legitimate_reads: int


@dataclass
class AvailabilityInputs:
    uptime_ratio: float
    auth_success_ratio: float
    response_time_score: float
    uptime_weight: float = 0.4
    auth_weight: float = 0.4
    response_weight: float = 0.2


def compute_integrity(inputs: IntegrityInputs) -> float:
    if inputs.legitimate_reads <= 0:
        return 0.0

    event_total = (
        inputs.breach_events
        + inputs.modification_events
        + inputs.hash_failures
    )
    score = 1 - (event_total / inputs.legitimate_reads)
    return clamp(score)


def compute_availability(inputs: AvailabilityInputs) -> float:
    total_weight = (
        inputs.uptime_weight
        + inputs.auth_weight
        + inputs.response_weight
    )

    if total_weight <= 0:
        return 0.0

    weighted_score = (
        inputs.uptime_ratio * inputs.uptime_weight
        + inputs.auth_success_ratio * inputs.auth_weight
        + inputs.response_time_score * inputs.response_weight
    ) / total_weight

    return clamp(weighted_score)


def compute_confidentiality_proxy(integrity_score: float, availability_score: float) -> float:
    return clamp(integrity_score) * clamp(availability_score)


def compute_windowed_efficiency(confidentiality_values: list[float]) -> float:
    if not confidentiality_values:
        return 0.0

    clean_values = [clamp(value) for value in confidentiality_values]
    return sum(clean_values) / len(clean_values)


def compute_iack(
    breach_events: int,
    modification_events: int,
    hash_failures: int,
    legitimate_reads: int,
    uptime_ratio: float,
    auth_success_ratio: float,
    response_time_score: float,
    previous_confidentiality_values: Optional[list[float]] = None,
) -> dict:
    integrity_inputs = IntegrityInputs(
        breach_events=breach_events,
        modification_events=modification_events,
        hash_failures=hash_failures,
        legitimate_reads=legitimate_reads,
    )

    availability_inputs = AvailabilityInputs(
        uptime_ratio=uptime_ratio,
        auth_success_ratio=auth_success_ratio,
        response_time_score=response_time_score,
    )

    integrity_score = compute_integrity(integrity_inputs)
    availability_score = compute_availability(availability_inputs)
    confidentiality_score = compute_confidentiality_proxy(
        integrity_score,
        availability_score,
    )

    history = previous_confidentiality_values or []
    efficiency_score = compute_windowed_efficiency(history + [confidentiality_score])

    return {
        "integrity": round(integrity_score, 4),
        "availability": round(availability_score, 4),
        "confidentiality_proxy": round(confidentiality_score, 4),
        "windowed_efficiency": round(efficiency_score, 4),
    }


if __name__ == "__main__":
    sample_result = compute_iack(
        breach_events=2,
        modification_events=1,
        hash_failures=1,
        legitimate_reads=100,
        uptime_ratio=0.98,
        auth_success_ratio=0.95,
        response_time_score=0.93,
        previous_confidentiality_values=[0.91, 0.92, 0.9],
    )

    print(sample_result)
