"""Hostile MRB coverage for Club-Madeira#10 / FR #4 xAI customer-owned keys."""
from __future__ import annotations

import club_madeira.xai_setup as xs


def test_forbidden_locations_name_club_infra_and_logs():
    pol = xs.storage_policy()
    blob = " ".join(pol["forbidden_locations"]).lower()
    assert "club madeira" in blob or "club" in blob
    assert "server" in blob or "infra" in blob or "repo" in blob
    assert "log" in blob or "outbox" in blob or "harvest" in blob


def test_redact_empty_and_short_and_non_xai():
    assert xs.redact_key("") == ""
    assert xs.redact_key("short") == "<redacted>"
    assert xs.redact_key("not-an-xai-key-value") != "not-an-xai-key-value"
    assert "not-an-xai-key-value" not in xs.redact_key("not-an-xai-key-value")


def test_looks_like_rejects_prefix_only_and_whitespace_junk():
    assert not xs.looks_like_xai_key("xai-")
    assert not xs.looks_like_xai_key("xai-short")
    assert not xs.looks_like_xai_key("  xai-  ")
    assert xs.looks_like_xai_key("  xai-abcdefghijklmnopqrstuvwxyz  ")


def test_device_key_matches_pwa_localstorage_name():
    paths = xs.device_key_locations("GO-99")
    assert "club-madeira-xai-key" in paths["browser"]
    assert paths["repo_secret_path"] is None


def test_blank_domain_fail_closed():
    ok, why = xs.can_start_xai_setup("", "GO-42")
    assert ok is False
    assert why == "dns_gate_failed"


def test_checklist_requires_pwa_or_device_not_club_servers():
    blob = " ".join(xs.setup_checklist()).lower()
    assert "localstorage" in blob or "pwa" in blob or "device" in blob or "os secret" in blob
    assert "never" in blob
