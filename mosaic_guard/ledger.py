from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field


@dataclass
class ContextLedger:
    """Minimal append-only ledger of context categories seen by a guard."""

    _categories: list[str] = field(default_factory=list)

    @property
    def categories(self) -> tuple[str, ...]:
        return tuple(self._categories)

    def add(self, category: str) -> None:
        category = category.strip()
        if not category:
            raise ValueError("context category must be non-empty")
        if category not in self._categories:
            self._categories.append(category)

    def extend(self, categories: Iterable[str]) -> None:
        for category in categories:
            self.add(category)
