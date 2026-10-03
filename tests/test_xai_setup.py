"""FR #4: customer-owned xAI tokens; never store in Club Madeira infra."""
from __future__ import annotations

import club_madeira.xai_setup as xs


def test_storage_policy_forbids_club_infra():
    pol = xs.storage_policy()
    assert pol["store_in_club_madeira_infra"] is False
    assert pol["customer_owned"] is True
    assert "localStorage" in pol["allowed_locations"] or "device" in str(pol["allowed_locations"]).lower()


def test_redact_key_never_echoes_secret():
    key = "xai-abcdefghijklmnopqrstuvwxyz0123456789"
    assert xs.redact_key(key) != key
    assert key not in xs.redact_key(key)
    assert "****" in xs.redact_key(key) or "<redacted>" in xs.redact_key(key).lower()


def test_looks_like_xai_key():
    assert xs.looks_like_xai_key("xai-abcdefghijklmnopqrstuvwxyz012345")
    assert not xs.looks_like_xai_key("sk-openai-not-this")
    assert not xs.looks_like_xai_key("")


def test_gate_requires_dns(monkeypatch):
    import club_madeira.dns_gate as gate

    monkeypatch.setattr(gate, "verify_go_id", lambda d, g: (False, {"reason": "go_id_not_found"}))
    ok, why = xs.can_start_xai_setup("example.com", "GO-42")
    assert ok is False
    assert why == "dns_gate_failed"
    monkeypatch.setattr(gate, "verify_go_id", lambda d, g: (True, {"matched": "GO-42"}))
    ok2, why2 = xs.can_start_xai_setup("example.com", "GO-42")
    assert ok2 is True
    assert why2 == "ok"


def test_device_paths_point_at_pwa_local_not_repo_secrets():
    paths = xs.device_key_locations("GO-42")
    assert "localStorage" in paths["browser"]
    assert paths.get("repo_secret_path") in (None, "")


def test_setup_checklist_mentions_customer_credits():
    steps = xs.setup_checklist()
    blob = " ".join(steps).lower()
    assert "xai" in blob
    assert "credit" in blob or "billing" in blob or "account" in blob
    assert "never" in blob and ("club" in blob or "infra" in blob or "store" in blob)
