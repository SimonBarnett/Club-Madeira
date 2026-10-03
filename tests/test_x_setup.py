"""FR #3: surface 2026 X pay-per-use pricing before customer continues setup."""
from __future__ import annotations

import club_madeira.x_setup as xs


def test_pricing_2026_pay_per_use_constants():
    p = xs.pricing_2026()
    assert p["read_per_post_usd"] == 0.005
    assert p["create_per_post_usd"] == 0.015
    assert p["create_with_url_usd"] == 0.20
    assert p["read_cap_per_month"] == 3_000_000
    assert p["legacy_basic_usd"] is None  # retired for new signups
    assert p["legacy_pro_usd"] is None


def test_estimate_monthly_cost():
    est = xs.estimate_monthly_cost(reads=1000, creates=100, creates_with_url=10)
    assert est["reads_usd"] == 5.0
    assert est["creates_usd"] == 1.5
    assert est["creates_with_url_usd"] == 2.0
    assert est["total_usd"] == 8.5


def test_pricing_brief_mentions_pay_per_use_and_retired_tiers():
    brief = xs.pricing_brief()
    assert "pay-per-use" in brief.lower()
    assert "0.005" in brief
    assert "Basic" in brief or "basic" in brief
    assert "retired" in brief.lower()


def test_gate_blocks_until_pricing_acknowledged():
    st = xs.SetupState(go_id="GO-42", domain="example.com")
    ok, why = xs.can_continue_past_pricing(st)
    assert ok is False
    assert why == "pricing_not_acknowledged"
    st2 = xs.acknowledge_pricing(st)
    ok2, why2 = xs.can_continue_past_pricing(st2)
    assert ok2 is True
    assert why2 == "ok"
    assert st2.pricing_acknowledged is True


def test_credential_paths_are_repo_relative_never_inline_secrets():
    paths = xs.credential_paths_for_go_id("GO-42")
    assert paths["repo"] == "club-madeira-go-42"
    assert paths["x_tokens_rel"].endswith(".json") or "x" in paths["x_tokens_rel"]
    assert "password" not in paths["x_tokens_rel"].lower()
