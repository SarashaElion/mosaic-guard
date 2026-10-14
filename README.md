# Mosaic Guard

**Open-source inference authorization for AI agents.**

Mosaic Guard explores a missing authorization layer between **data access** and **derived knowledge**.

Traditional access control asks whether an agent may read a source or perform an action. Mosaic Guard asks a different question:

> **What becomes newly inferable when another piece of permitted information enters the context, and is the agent authorized to cross that inference boundary?**

## Status

Mosaic Guard is an early reference implementation and research project for the proposed **Inference Boundary Protocol (IBP)**.

The v0.1 goal is deliberately narrow:

1. represent context as typed information categories;
2. represent known inference rules over combinations of those categories;
3. compute the *new* inference classes activated by an incoming datum;
4. evaluate those new inferences against an explicit policy; and
5. return one of four decisions:
   - `ALLOW`
   - `DENY`
   - `CONSENT_REQUIRED`
   - `UNKNOWN`

Mosaic Guard does **not** claim to determine everything a foundation model internally knows or infers. The reference implementation operates at the system boundary, using declared context categories and policy-defined or pluggable inference detectors.

## Core idea

Let `C_t` be the accumulated context at time `t`, and let `I(C)` denote the inference frontier: the set of inference classes reasonably derivable from context `C`.

When new information `d` enters context:

```text
ΔI = I(C_t ∪ {d}) − I(C_t)
```

Mosaic Guard evaluates `ΔI` against an inference-boundary policy.

This makes privacy and authorization partly a property of **knowledge emergence**, not only data possession.

## Why this exists

A system may be permitted to access several individually innocuous sources while their combination enables a sensitive inference the user never intended to authorize.

Examples include combinations that reveal or strongly suggest:

- a medical condition,
- an intimate relationship,
- religious or political affiliation,
- employment instability,
- financial distress,
- identity or location patterns.

Mosaic Guard provides a place to formalize and test that transition.

## Repository direction

This repository will contain:

- the IBP policy/schema proposal;
- a Python reference implementation;
- a context ledger;
- an inference-frontier engine;
- policy evaluation;
- synthetic mosaic-effect benchmarks;
- integration examples for agent and tool systems.

## Design principles

- **Model-agnostic** — enforcement should not depend on hidden chain-of-thought.
- **Purpose-bound** — authorization can differ by declared task or purpose.
- **Compositional** — combinations matter, not just individual records.
- **Auditable** — boundary decisions should be inspectable.
- **Consent-aware** — sensitive inference can trigger explicit consent rather than silent continuation.
- **Fail-visible** — uncertainty should surface as `UNKNOWN`, not be silently treated as safe.

## License

Apache License 2.0.

---

Mosaic Guard is experimental security/privacy infrastructure. It should not be treated as a complete privacy guarantee or a substitute for legal, security, or governance review.
