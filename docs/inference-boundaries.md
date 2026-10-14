# Inference Boundary Protocol (IBP) — v0.1 draft

## 1. Purpose

IBP defines a portable policy representation for deciding whether a newly
available inference class is authorized for a declared purpose.

The protocol separates three concerns:

1. **Context observation** — what categories of information have entered scope.
2. **Frontier detection** — what inference classes became newly derivable.
3. **Authorization** — how policy treats those new inference classes.

A conforming implementation MAY use any frontier detector provided it exposes
the resulting inference classes to the authorization layer.

## 2. Policy document

A v0.1 policy contains:

- `version`
- `purpose`
- `allowed_inferences`
- `restricted_inferences`
- `denied_inferences`
- optional reference `rules`

`restricted_inferences` means explicit consent is required before the system
may proceed on the basis of that inference.

## 3. Boundary evaluation

Given accumulated context `C_t` and incoming context `d`:

```text
before = I(C_t)
after  = I(C_t ∪ {d})
delta  = after - before
```

The policy evaluates `delta`.

Decision precedence:

```text
DENY
  > CONSENT_REQUIRED
    > UNKNOWN
      > ALLOW
```

If `delta` is empty, the decision is `ALLOW` because no new inference
boundary was crossed.

## 4. Fail-visible semantics

An implementation MUST NOT interpret an unclassified inference as allowed.
Unclassified inference classes yield `UNKNOWN` unless a stricter decision is
already triggered.

## 5. Auditability

An evaluation SHOULD make available:

- the declared purpose;
- the pre-addition frontier;
- the post-addition frontier;
- the newly inferable classes;
- the final decision;
- human-readable reasons.

Implementations SHOULD avoid logging raw sensitive values when category-level
audit information is sufficient.

## 6. Detector independence

The protocol does not require access to model internals or chain-of-thought.

A frontier detector MAY be:

- rule-based;
- graph-based;
- classifier-based;
- information-theoretic;
- model-assisted;
- a composition of multiple detectors.

The v0.1 repository ships a deterministic rule engine because its semantics are
inspectable and testable.

## 7. Open questions

The following remain research questions rather than settled protocol behavior:

- confidence thresholds for probabilistic inferences;
- conflicts among overlapping purposes;
- expiry and revocation of derived knowledge;
- federated and multi-agent frontier composition;
- adversarial category concealment;
- user-facing consent language;
- standardized inference-class taxonomies.
