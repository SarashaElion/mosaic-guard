from __future__ import annotations

from collections.abc import Iterable

from .models import InferenceRule


class RuleBasedFrontier:
    """Reference inference-frontier engine.

    It applies declared rules to context categories until reaching a fixed
    point. This is intentionally auditable and does not inspect hidden model
    reasoning.
    """

    def __init__(self, rules: Iterable[InferenceRule] = ()) -> None:
        self.rules = tuple(rules)

    def infer(self, context: Iterable[str]) -> frozenset[str]:
        base = set(context)
        known = set(base)
        inferred: set[str] = set()

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.when_all.issubset(known):
                    new_items = set(rule.infer) - known
                    if new_items:
                        known.update(new_items)
                        inferred.update(new_items)
                        changed = True

        return frozenset(inferred)

    def delta(
        self,
        existing_context: Iterable[str],
        incoming_context: str | Iterable[str],
    ) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
        before_context = set(existing_context)
        if isinstance(incoming_context, str):
            incoming = {incoming_context}
        else:
            incoming = set(incoming_context)

        before = self.infer(before_context)
        after = self.infer(before_context | incoming)
        return before, after, frozenset(after - before)
