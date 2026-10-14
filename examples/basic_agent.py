from mosaic_guard import MosaicGuard

guard = MosaicGuard("policies/example.yaml")

result = guard.evaluate(
    existing_context=["calendar", "location_history"],
    incoming_context="purchase_history",
)

print(result.decision.value)
print(sorted(result.newly_inferable))
print(result.reasons)
