# Threat Model

## Protected property

Mosaic Guard attempts to preserve a user's declared boundary around **derived
knowledge**, even when each contributing source was individually authorized.

The protected object is not secrecy of every input. It is the transition from
permitted context to a policy-sensitive inference class.

## Primary threats

### Mosaic accumulation

Individually low-sensitivity categories combine to expose a high-sensitivity
inference.

### Cross-purpose reuse

Context authorized for one purpose is reused to derive knowledge for another
purpose without renewed authorization.

### Temporal accumulation

No single interaction crosses a boundary, but context accumulated across time
eventually does.

### Derived chaining

One inferred class becomes an input to another rule, producing a sensitive
second-order inference.

### Policy gaps

A new inference class is possible but absent from policy. Mosaic Guard returns
`UNKNOWN` rather than silently treating the gap as permission.

### Detector incompleteness

The configured frontier detector fails to identify a real inferential pathway.
This is a core research risk and must remain visible in claims about the system.

## Trust assumptions

The reference implementation assumes:

- context categories presented to the guard are truthful enough to evaluate;
- the agent runtime actually consults the guard before acting on protected
  derived knowledge;
- policy configuration is authentic and has not been maliciously altered.

## Out of scope for v0.1

Mosaic Guard v0.1 does not:

- read or expose hidden chain-of-thought;
- prove what a foundation model internally knows;
- prevent exfiltration by a fully compromised runtime;
- solve training-data extraction or model inversion;
- infer legal compliance from a policy decision;
- guarantee detection of every semantic inference;
- replace data minimization, encryption, sandboxing, or conventional access
  control.

These boundaries are intentional. The project is testing an authorization
primitive, not claiming a complete privacy system.
