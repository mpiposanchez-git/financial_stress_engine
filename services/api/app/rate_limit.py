from __future__ import annotations

import time
from collections import defaultdict, deque


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._windows: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, max_requests_per_minute: int) -> bool:
        now = time.time()
        window_start = now - 60.0
        events = self._windows[key]

        while events and events[0] < window_start:
            events.popleft()

        if len(events) >= max_requests_per_minute:
            return False

        events.append(now)
        return True


rate_limiter = InMemoryRateLimiter()
