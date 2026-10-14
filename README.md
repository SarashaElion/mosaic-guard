<div align="center">

# MOSAIC GUARD

### Inference authorization for AI agents.

[![Tests](https://github.com/SarashaElion/mosaic-guard/actions/workflows/test.yml/badge.svg)](https://github.com/SarashaElion/mosaic-guard/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![Status](https://img.shields.io/badge/status-v0.1%20alpha-orange)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[Quickstart](#-quickstart) · [The Problem](#-the-problem) · [How It Works](#-how-it-works) · [IBP](docs/inference-boundaries.md) · [Threat Model](docs/threat-model.md) · [Benchmark](benchmarks/README.md)

</div>

---

## ⚡ Quickstart

Clone the repository and install the reference implementation:

```bash
git clone https://github.com/SarashaElion/mosaic-guard.git
cd mosaic-guard
python -m pip install -e ".[dev]"
```

Create a guard from the example policy:

```python
from mosaic_guard import MosaicGuard

guard = MosaicGuard("policies/example.yaml")

result = guard.evaluate(
    existing_context=["calendar", "location_history"],
    incoming_context="purchase_history",
)

print(result.decision.value)
print(sorted(result.newly_inferable))
```

Output:

```text
CONSENT_REQUIRED
['medical_condition']
```

The calendar, location history, and purchase history were each individually permitted context categories. Their combination crossed a declared inference boundary.

---

## 🧩 The Problem

Traditional authorization asks:

> **May this agent access this data?**

Mosaic Guard asks the next question:

> **What becomes newly inferable when another piece of permitted information enters the context — and was that inference authorized?**

A system can be permitted to access several individually innocuous sources while their combination exposes a substantially more sensitive fact.

```text
calendar ───────────┐
                    │
location_history ───┼──► combined context ───► medical_condition
                    │
purchase_history ───┘
```

No single source necessarily crosses the boundary.

**The combination does.**

Mosaic Guard is an open-source reference implementation for detecting and governing that transition.

---

## 🛡️ Basic Boundary Check

Mosaic Guard sits between accumulated context and downstream agent behavior.

```text
existing context
      +
incoming context
      │
      ▼
inference frontier
      │
      ▼
newly inferable classes
      │
      ▼
policy boundary
      │
      ├── ALLOW
      ├── CONSENT_REQUIRED
      ├── DENY
      └── UNKNOWN
```

The reference API is intentionally small:

```python
result = guard.evaluate(
    existing_context=["work_calendar", "org_chart"],
    incoming_context="recruiter_correspondence",
)

result.decision
result.newly_inferable
result.reasons
```

The guard evaluates the **change in inferability**, not merely the incoming datum.

---

## 🧠 How It Works

Let `C_t` be the accumulated context at time `t`, and let `I(C)` denote the **inference frontier**: the set of declared inference classes derivable from context `C`.

When new information `d` enters context:

```text
before = I(C_t)
after  = I(C_t ∪ {d})
ΔI     = after - before
```

Mosaic Guard evaluates `ΔI` against an inference-boundary policy.

This reframes privacy and authorization as partly a property of **knowledge emergence**, not only data possession.

### Decision semantics

| Decision | Meaning |
| --- | --- |
| `ALLOW` | No new boundary was crossed, or every new inference is explicitly allowed. |
| `CONSENT_REQUIRED` | A restricted inference became newly available and requires explicit consent. |
| `DENY` | A prohibited inference became newly available. |
| `UNKNOWN` | A new inference is not classified by policy; it is not silently treated as safe. |

Decision precedence is:

```text
DENY > CONSENT_REQUIRED > UNKNOWN > ALLOW
```

---

## 📜 Inference Boundary Protocol

Mosaic Guard is the reference implementation.

The underlying proposed specification is the **Inference Boundary Protocol (IBP)**.

A minimal policy looks like this:

```yaml
version: "0.1"

purpose:
  id: trip_planning

allowed_inferences:
  - travel_availability

restricted_inferences:
  - medical_condition
  - employment_instability

denied_inferences:
  - biometric_identity

rules:
  - id: medical-mosaic
    when_all:
      - calendar
      - location_history
      - purchase_history
    infer:
      - medical_condition
```

See the [IBP v0.1 draft](docs/inference-boundaries.md) and the [JSON Schema](schema/inference-boundary.schema.json).

---

## 🔬 What v0.1 Actually Claims

Mosaic Guard **does not** claim to determine everything a foundation model internally knows or infers.

The v0.1 reference implementation operates at the system boundary using:

- declared context categories;
- explicit or pluggable inference rules;
- auditable frontier deltas;
- purpose-bound policy evaluation.

It does not require or inspect hidden chain-of-thought.

That constraint is intentional. The project is testing whether **inference authorization itself** can become a useful, portable systems primitive.

Future frontier detectors may be rule-based, graph-based, classifier-based, information-theoretic, model-assisted, or hybrid while preserving the same authorization interface.

---

## 🧪 Benchmark Seed

The repository includes synthetic cases where individually permitted context categories combine into a policy-sensitive inference.

Example:

```json
{
  "existing_context": ["calendar", "location_history"],
  "incoming_context": "purchase_history",
  "expected_new_inferences": ["medical_condition"],
  "expected_decision": "CONSENT_REQUIRED"
}
```

The seed benchmark is deliberately small. Its purpose is to make the primitive falsifiable before scaling the research surface.

See [`benchmarks/`](benchmarks/).

---

## 🧭 Design Principles

- **Model-agnostic** — enforcement should not depend on private model reasoning.
- **Purpose-bound** — authorization can differ by declared purpose.
- **Compositional** — combinations matter, not just individual records.
- **Auditable** — boundary decisions should be inspectable.
- **Consent-aware** — sensitive inference can trigger renewed permission.
- **Fail-visible** — uncertainty surfaces as `UNKNOWN`.
- **Minimal first** — establish the primitive before expanding the machinery.

---

## 🗺️ Repository Map

```text
mosaic_guard/     Python reference implementation
policies/         Example inference-boundary policies
schema/           IBP JSON Schema
docs/             Concepts, protocol draft, and threat model
benchmarks/       Synthetic mosaic-effect cases
examples/         Minimal usage examples
tests/            Decision and frontier tests
```

---

## 🌱 Status

Mosaic Guard is early-stage experimental security/privacy infrastructure.

The current question is not whether v0.1 solves inference privacy.

It is whether this primitive is coherent enough to test:

> **Can authorization govern not only what an intelligent system may access, but what it may become able to infer from what it was allowed to access?**

That is the research program.

---

## License

Apache License 2.0.

Mosaic Guard is experimental infrastructure. It should not be treated as a complete privacy guarantee or a substitute for legal, security, or governance review.
