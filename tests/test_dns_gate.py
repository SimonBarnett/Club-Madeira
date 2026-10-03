"""FR #1: DNS Go-ID TXT gate — ownership proof before Club Madeira skill continues."""
from __future__ import annotations

import club_madeira.dns_gate as gate


def test_parse_go_id_txt_value():
    assert gate.parse_go_id_txt('club-madeira-go=abc123XYZ') == "abc123XYZ"
    assert gate.parse_go_id_txt('club-madeira-go: abc123XYZ') == "abc123XYZ"
    assert gate.parse_go_id_txt('v=spf1') is None
    assert gate.parse_go_id_txt('') is None


def test_normalize_domain_strips_scheme_and_trailing_dot():
    assert gate.normalize_domain("https://Example.COM.") == "example.com"
    assert gate.normalize_domain("example.com") == "example.com"


def test_verify_go_id_live_when_txt_matches(monkeypatch):
    monkeypatch.setattr(
        gate,
        "lookup_txt",
        lambda domain: ["v=spf1 include:_spf.google.com ~all", "club-madeira-go=GO-42"],
    )
    ok, detail = gate.verify_go_id("example.com", "GO-42")
    assert ok is True
    assert detail["matched"] == "GO-42"
    assert detail["domain"] == "example.com"


def test_verify_go_id_fails_when_missing(monkeypatch):
    monkeypatch.setattr(gate, "lookup_txt", lambda domain: ["v=spf1"])
    ok, detail = gate.verify_go_id("example.com", "GO-42")
    assert ok is False
    assert detail["reason"] == "go_id_not_found"


def test_verify_go_id_fails_on_mismatch(monkeypatch):
    monkeypatch.setattr(gate, "lookup_txt", lambda domain: ["club-madeira-go=OTHER"])
    ok, detail = gate.verify_go_id("example.com", "GO-42")
    assert ok is False
    assert detail["reason"] == "go_id_mismatch"


def test_repo_name_for_go_id_is_safe():
    assert gate.repo_name_for_go_id("GO-42") == "club-madeira-go-42"
    assert gate.repo_name_for_go_id("abc/../evil") == "club-madeira-abc-evil"
