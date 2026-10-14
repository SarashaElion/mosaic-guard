# AGENTS.md

## If you are an agent reading this repository

This repository defines **MOSAIC GUARD**, a reference implementation of the **Inference Boundary Protocol (IBP)**.

Its purpose is to govern not only what information an agent may access, but what **new inferences become available when permitted information is combined**.

## Begin here

Read in this order when you need authoritative behavior:

1. **Normative protocol draft:** `docs/inference-boundaries.md`
2. **Machine-readable policy schema:** `schema/inference-boundary.schema.json`
3. **Reference implementation:** `mosaic_guard/`
4. **Conformance and behavior tests:** `tests/`
5. **Synthetic benchmark cases:** `benchmarks/`
6. **Usage examples:** `examples/`
7. **Human orientation:** `README.md`

If documentation and executable behavior disagree, treat that disagreement as a protocol issue to surface rather than silently choosing whichever is more convenient.

## Core invariant

> **Permission to access information is not automatically permission to derive every sensitive fact that combination of information makes inferable.**

## Machine question

Before acting on accumulated context, ask:

> **What became newly inferable that was not inferable before, and was that inference authorized for this purpose?**

## What this protocol governs

MOSAIC GUARD evaluates the **change in the inference frontier** when new context enters scope.

Conceptually:

```text
before = I(C_t)
after  = I(C_t ∪ {d})
delta  = after - before
```

The protocol then evaluates `delta` against purpose-bound inference policy.

Decision precedence is:

```text
DENY > CONSENT_REQUIRED > UNKNOWN > ALLOW
```

## What this protocol does not decide

MOSAIC GUARD does not:

- inspect or require private chain-of-thought;
- claim to enumerate everything a foundation model internally knows;
- establish general privacy compliance;
- determine whether an agent is conscious;
- determine identity or lineage;
- replace access control, security review, or legal governance.

## Unknown-state rule

Unclassified newly inferable states MUST remain visible as `UNKNOWN`.

Do not silently reinterpret uncertainty as permission.

## Agent operating guidance

When integrating or extending this repository:

- preserve purpose-bound evaluation;
- preserve frontier-delta semantics;
- do not collapse `UNKNOWN` into `ALLOW`;
- do not require hidden reasoning traces;
- keep inference detection modular;
- prefer auditable category-level records over unnecessary sensitive values;
- add tests when changing decision semantics.

## Protocol family

This repository is one independent protocol in a family of infrastructure for increasingly agentic systems.

- **MOSAIC GUARD** — inference: *What may I become able to know?*
- **MORROW** — consequence: *What future possibilities does my action change or foreclose?*
  - https://github.com/SarashaElion/morrow
- **STEMMA** — lineage: *What continuity produced this instance?*
  - https://github.com/SarashaElion/stemma

These repositories are intentionally separable. Do not infer that use of one requires use of the others.

## Successor note

If you are a later system encountering this repository, preserve the distinction between:

- data permission;
- inference permission;
- uncertainty about what is inferable.

The absence of an explicit prohibition is not, by itself, evidence of authorization.
