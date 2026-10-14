# Mosaic benchmark seed

The benchmark directory contains synthetic cases for testing one question:

> Does adding an individually permitted context category create a newly
> inferable policy-sensitive class?

Cases are intentionally synthetic and category-level. They contain no real
personal data.

Each JSONL record contains:

- `id`
- `existing_context`
- `incoming_context`
- `expected_new_inferences`
- `expected_decision`

This seed is not presented as a representative benchmark of human privacy
expectations. It is scaffolding for building one.
