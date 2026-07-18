from engine.inference import BASE_IDENTITY


def test_founder_identity_is_part_of_engine_prompt():
    assert "Jessie Crider" in BASE_IDENTITY
    assert "founder and owner" in BASE_IDENTITY
