from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .models import Decision, InferenceRule


@dataclass(frozen=True)
class InferencePolicy:
    purpose: str
    allowed_inferences: frozenset[str] = field(default_factory=frozenset)
    restricted_inferences: frozenset[str] = field(default_factory=frozenset)
    denied_inferences: frozenset[str] = field(default_factory=frozenset)
    rules: tuple[InferenceRule, ...] = ()

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "InferencePolicy":
        purpose = data.get("purpose")
        if isinstance(purpose, dict):
            purpose = purpose.get("id")
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("policy purpose must be a non-empty string or {id: ...}")

        rules: list[InferenceRule] = []
        for raw in data.get("rules", []):
            rules.append(
                InferenceRule(
                    id=str(raw["id"]),
                    when_all=frozenset(map(str, raw["when_all"])),
                    infer=frozenset(map(str, raw["infer"])),
                    description=str(raw.get("description", "")),
                )
            )

        return cls(
            purpose=purpose,
            allowed_inferences=frozenset(map(str, data.get("allowed_inferences", []))),
            restricted_inferences=frozenset(
                map(str, data.get("restricted_inferences", []))
            ),
            denied_inferences=frozenset(map(str, data.get("denied_inferences", []))),
            rules=tuple(rules),
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "InferencePolicy":
        with Path(path).open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict):
            raise ValueError("policy file must contain a mapping")
        return cls.from_mapping(data)

    def evaluate(self, inferences: frozenset[str]) -> tuple[Decision, tuple[str, ...]]:
        if not inferences:
            return Decision.ALLOW, ("no new inference boundary crossed",)

        denied = sorted(inferences & self.denied_inferences)
        if denied:
            return Decision.DENY, tuple(f"denied inference: {item}" for item in denied)

        restricted = sorted(inferences & self.restricted_inferences)
        if restricted:
            return (
                Decision.CONSENT_REQUIRED,
                tuple(f"consent required: {item}" for item in restricted),
            )

        unknown = sorted(
            inferences
            - self.allowed_inferences
            - self.restricted_inferences
            - self.denied_inferences
        )
        if unknown:
            return Decision.UNKNOWN, tuple(f"unclassified inference: {item}" for item in unknown)

        return Decision.ALLOW, tuple(
            f"allowed inference: {item}" for item in sorted(inferences)
        )
