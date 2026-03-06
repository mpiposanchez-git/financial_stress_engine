from __future__ import annotations

from copy import deepcopy
from threading import Lock

_COUNTER_LOCK = Lock()
_COUNTERS: dict[str, int] = {
    "deterministic_runs_total": 0,
    "montecarlo_runs_total": 0,
    "pdf_exports_total": 0,
    "errors_total": 0,
}
_RUNTIME_BUCKETS: dict[str, int] = {
    "lt_100ms": 0,
    "100_to_499ms": 0,
    "500_to_999ms": 0,
    "gte_1000ms": 0,
}


def _runtime_bucket(runtime_ms: float) -> str:
    if runtime_ms < 100:
        return "lt_100ms"
    if runtime_ms < 500:
        return "100_to_499ms"
    if runtime_ms < 1000:
        return "500_to_999ms"
    return "gte_1000ms"


def record_deterministic_run(runtime_ms: float) -> None:
    with _COUNTER_LOCK:
        _COUNTERS["deterministic_runs_total"] += 1
        _RUNTIME_BUCKETS[_runtime_bucket(runtime_ms)] += 1


def record_montecarlo_run(runtime_ms: float) -> None:
    with _COUNTER_LOCK:
        _COUNTERS["montecarlo_runs_total"] += 1
        _RUNTIME_BUCKETS[_runtime_bucket(runtime_ms)] += 1


def record_pdf_export() -> None:
    with _COUNTER_LOCK:
        _COUNTERS["pdf_exports_total"] += 1


def record_error() -> None:
    with _COUNTER_LOCK:
        _COUNTERS["errors_total"] += 1


def get_telemetry_snapshot() -> dict[str, dict[str, int] | int]:
    with _COUNTER_LOCK:
        counters = deepcopy(_COUNTERS)
        runtime_buckets = deepcopy(_RUNTIME_BUCKETS)
    return {
        **counters,
        "runtime_buckets": runtime_buckets,
    }


def reset_telemetry() -> None:
    with _COUNTER_LOCK:
        for key in _COUNTERS:
            _COUNTERS[key] = 0
        for key in _RUNTIME_BUCKETS:
            _RUNTIME_BUCKETS[key] = 0
