from threading import Lock
from typing import Any


class IdempotencyStore:
    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            return self._items.get(key)

    def put(self, key: str, value: dict[str, Any]) -> None:
        with self._lock:
            self._items[key] = value

