"""Twitter / X API setup helpers for Club Madeira Skill (FR #3).

Surfaces 2026 pay-per-use pricing before the customer continues. Does not call
the live X API and never logs secrets.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from club_madeira.dns_gate import repo_name_for_go_id

# As of 2026: pay-per-use for new signups; legacy Basic ($200) / Pro ($5000) retired.
_PRICING_2026: dict[str, Any] = {
    "read_per_post_usd": 0.005,
    "create_per_post_usd": 0.015,
    "create_with_url_usd": 0.20,
    "read_cap_per_month": 3_000_000,
    "legacy_basic_usd": None,
    "legacy_pro_usd": None,
    "notes": (
        "X API is pay-per-use for new signups (2026). "
        "Legacy Basic ($200) and Pro ($5,000) tiers are retired for new accounts."
    ),
}


@dataclass
class SetupState:
    go_id: str
    domain: str
    pricing_acknowledged: bool = False


def pricing_2026() -> dict[str, Any]:
    return dict(_PRICING_2026)


def estimate_monthly_cost(
    *, reads: int = 0, creates: int = 0, creates_with_url: int = 0
) -> dict[str, float]:
    p = pricing_2026()
    reads_usd = round(reads * float(p["read_per_post_usd"]), 6)
    creates_usd = round(creates * float(p["create_per_post_usd"]), 6)
    url_usd = round(creates_with_url * float(p["create_with_url_usd"]), 6)
    return {
        "reads_usd": reads_usd,
        "creates_usd": creates_usd,
        "creates_with_url_usd": url_usd,
        "total_usd": round(reads_usd + creates_usd + url_usd, 6),
    }


def pricing_brief() -> str:
    p = pricing_2026()
    return (
        "X API pricing (2026 pay-per-use for new signups)\n"
        f"- Read post: ${p['read_per_post_usd']} each\n"
        f"- Create post: ${p['create_per_post_usd']} each\n"
        f"- Create post with URL: ${p['create_with_url_usd']} each\n"
        f"- Read cap: {p['read_cap_per_month']:,} / month\n"
        "- Legacy Basic ($200) and Pro ($5,000) tiers are retired for new signups.\n"
        "Acknowledge this pricing before continuing X token setup so you do not hit a paywall mid-flow."
    )


def acknowledge_pricing(state: SetupState) -> SetupState:
    return replace(state, pricing_acknowledged=True)


def can_continue_past_pricing(state: SetupState) -> tuple[bool, str]:
    if not state.pricing_acknowledged:
        return False, "pricing_not_acknowledged"
    return True, "ok"


def credential_paths_for_go_id(go_id: str) -> dict[str, str]:
    """Where X tokens should live inside the private Go-ID working-data repo."""
    repo = repo_name_for_go_id(go_id)
    return {
        "repo": repo,
        "x_tokens_rel": "credentials/x-api-tokens.json",
        "readme_rel": "credentials/README.md",
    }


def setup_checklist() -> list[str]:
    return [
        "Show pricing_brief() and require acknowledge_pricing before continuing",
        "Customer creates X account and enables developer access / API app",
        "Customer generates API tokens (never paste into Club Madeira infra logs)",
        "Store tokens only under credentials/x-api-tokens.json in the private Go-ID repo",
        "Smoke: agent can read/post with customer tokens; estimate_monthly_cost for expected volume",
    ]
