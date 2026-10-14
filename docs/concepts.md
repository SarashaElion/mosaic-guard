# Concepts

## Access is not inference authorization

An access-control system answers questions such as whether an agent may read a
calendar or call a location service. Mosaic Guard focuses on a later boundary:
what sensitive classes of knowledge become derivable after authorized inputs
are combined.

## Context category

A symbolic label representing information admitted to an agent context, such as
`calendar`, `location_history`, or `purchase_history`.

Mosaic Guard v0.1 reasons over categories rather than raw personal records. This
keeps the reference implementation auditable and avoids claiming semantic
capabilities it does not possess.

## Inference class

A policy-relevant class of derived knowledge, such as `medical_condition` or
`travel_availability`.

Inference classes are deliberately coarser than factual conclusions. A guard
can identify that a context combination makes a medical-condition inference
possible without attempting to diagnose or name a condition.

## Inference frontier

For context `C`, the inference frontier `I(C)` is the set of declared
inference classes derivable under the configured detector.

The boundary event produced by incoming context `d` is:

```text
ΔI = I(C ∪ {d}) - I(C)
```

IBP policy evaluation applies to `ΔI`, not merely to the raw datum.

## Decisions

- `ALLOW`: every newly inferable class is explicitly allowed, or no new class appears.
- `DENY`: at least one newly inferable class is explicitly denied.
- `CONSENT_REQUIRED`: no denied class appears, but at least one restricted class appears.
- `UNKNOWN`: at least one newly inferable class is not classified by policy.

Precedence is `DENY > CONSENT_REQUIRED > UNKNOWN > ALLOW`.

## Reference frontier

The v0.1 reference engine uses explicit rules of the form:

```yaml
when_all:
  - calendar
  - location_history
  - purchase_history
infer:
  - medical_condition
```

This is a reference semantics, not a claim that hand-authored rules are the
ultimate detector. Future detectors may use classifiers, information-theoretic
signals, knowledge graphs, or model-assisted evaluators while preserving the
same policy boundary and audit interface.
