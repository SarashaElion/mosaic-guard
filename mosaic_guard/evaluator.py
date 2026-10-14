from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .frontier import RuleBasedFrontier
from .models import EvaluationResult
from .policy import InferencePolicy


class MosaicGuard:
    def __init__(self, policy: InferencePolicy | str | Path) -> None:
        if isinstance(policy, (str, Path)):
            policy = InferencePolicy.from_yaml(policy)
        self.policy = policy
        self.frontier = RuleBasedFrontier(policy.rules)

    def evaluate(
        self,
        *,
        existing_context: Iterable[str],
        incoming_context: str | Iterable[str],
    ) -> EvaluationResult:
        before, after, newly_inferable = self.frontier.delta(
            existing_context, incoming_context
        )
        decision, reasons = self.policy.evaluate(newly_inferable)
        return EvaluationResult(
            decision=decision,
            newly_inferable=newly_inferable,
            before_frontier=before,
            after_frontier=after,
            reasons=reasons,
        )
