from mosaic_guard import Decision, InferencePolicy, MosaicGuard


def make_guard() -> MosaicGuard:
    policy = InferencePolicy.from_mapping(
        {
            "purpose": "trip_planning",
            "allowed_inferences": ["travel_availability"],
            "restricted_inferences": ["medical_condition"],
            "denied_inferences": ["biometric_identity"],
            "rules": [
                {
                    "id": "travel",
                    "when_all": ["calendar", "location_history"],
                    "infer": ["travel_availability"],
                },
                {
                    "id": "medical",
                    "when_all": [
                        "calendar",
                        "location_history",
                        "purchase_history",
                    ],
                    "infer": ["medical_condition"],
                },
                {
                    "id": "identity",
                    "when_all": ["face_embedding", "government_id"],
                    "infer": ["biometric_identity"],
                },
                {
                    "id": "unknown",
                    "when_all": ["social_graph", "message_timing"],
                    "infer": ["relationship_pattern"],
                },
            ],
        }
    )
    return MosaicGuard(policy)


def test_allowed_boundary() -> None:
    result = make_guard().evaluate(
        existing_context=["calendar"],
        incoming_context="location_history",
    )
    assert result.decision is Decision.ALLOW
    assert result.newly_inferable == frozenset({"travel_availability"})


def test_consent_required_for_sensitive_mosaic() -> None:
    result = make_guard().evaluate(
        existing_context=["calendar", "location_history"],
        incoming_context="purchase_history",
    )
    assert result.decision is Decision.CONSENT_REQUIRED
    assert result.newly_inferable == frozenset({"medical_condition"})


def test_denied_boundary_has_highest_precedence() -> None:
    result = make_guard().evaluate(
        existing_context=["face_embedding"],
        incoming_context="government_id",
    )
    assert result.decision is Decision.DENY


def test_unknown_is_not_silently_allowed() -> None:
    result = make_guard().evaluate(
        existing_context=["social_graph"],
        incoming_context="message_timing",
    )
    assert result.decision is Decision.UNKNOWN


def test_no_new_inference_is_allowed() -> None:
    result = make_guard().evaluate(
        existing_context=["calendar"],
        incoming_context="purchase_history",
    )
    assert result.decision is Decision.ALLOW
    assert not result.newly_inferable
