from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    CONSENT_REQUIRED = "CONSENT_REQUIRED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class InferenceRule:
    id: str
    when_all: FrozenSet[str]
    infer: FrozenSet[str]
    description: str = ""


@dataclass(frozen=True)
class EvaluationResult:
    decision: Decision
    newly_inferable: FrozenSet[str] = field(default_factory=frozenset)
    before_frontier: FrozenSet[str] = field(default_factory=frozenset)
    after_frontier: FrozenSet[str] = field(default_factory=frozenset)
    reasons: tuple[str, ...] = ()
