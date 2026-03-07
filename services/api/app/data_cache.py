from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CacheMeta(BaseModel):
    fetched_at_utc: str = Field(..., min_length=1)
    source_url: str = Field(..., min_length=1)
    sha256: str = Field(..., min_length=1)


class CacheEntry(BaseModel):
    value: Any
    meta: CacheMeta


class InMemoryDataCache:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}

    def get(self, key: str) -> CacheEntry | None:
        return self._store.get(key)

    def set(self, key: str, value: Any, meta: CacheMeta | dict[str, str]) -> CacheEntry:
        entry = CacheEntry(value=value, meta=CacheMeta.model_validate(meta))
        self._store[key] = entry
        return entry


DATA_CACHE = InMemoryDataCache()
