from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.engine.inputs import ShockSchedule


def _clamp_bps(value: int) -> int:
    return max(0, min(10_000, value))


def resolve_schedule_levels(
    base_level_bps: int,
    horizon_months: int,
    schedule: ShockSchedule | None,
) -> list[int]:
    """Resolve schedule into month-by-month bps levels.

    Returns a list with length == horizon_months for months 1..horizon.
    """
    if horizon_months < 1:
        raise ValueError("horizon_months must be >= 1")

    base = _clamp_bps(base_level_bps)
    levels = [base for _ in range(horizon_months)]

    if schedule is None:
        return levels

    if schedule.kind == "step":
        level = _clamp_bps(int(schedule.level_bps if schedule.level_bps is not None else base))
        return [level for _ in range(horizon_months)]

    if schedule.kind == "ramp":
        target = _clamp_bps(int(schedule.level_bps if schedule.level_bps is not None else base))
        raw_end_month = int(schedule.end_month if schedule.end_month is not None else 1)
        end_month = max(1, min(horizon_months, raw_end_month))

        if end_month == 1:
            levels[0] = target
        else:
            for month_idx in range(end_month):
                fraction = month_idx / (end_month - 1)
                interpolated = round(base + (target - base) * fraction)
                levels[month_idx] = _clamp_bps(int(interpolated))

        for month_idx in range(end_month, horizon_months):
            levels[month_idx] = target

        return levels

    # kind == "stepped"
    points = list(schedule.points or [])
    current = base
    point_index = 0

    for month in range(1, horizon_months + 1):
        while point_index < len(points) and points[point_index][0] == month:
            current = _clamp_bps(points[point_index][1])
            point_index += 1
        levels[month - 1] = current

    return levels
