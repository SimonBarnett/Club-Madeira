"""xAI API key provisioning helpers (FR #4).

Customer creates their own xAI account/credits. The skill book runs on **their**
tokens only. Club Madeira infrastructure never stores the key.
"""
from __future__ import annotations

import re
from typing import Any

from club_madeira import dns_gate

_XAI_KEY_RX = re.compile(r"^xai-[A-Za-z0-9_\-]{16,}$")


def storage_policy() -> dict[str, Any]:
    return {
        "customer_owned": True,
        "store_in_club_madeira_infra": False,
        "allowed_locations": (
            "browser localStorage (skill-book PWA)",
            "customer device / OS secret store",
            "customer private notes (never committed to public git)",
        ),
        "forbidden_locations": (
            "Club Madeira servers",
            "Club Madeira shared repos",
            "agent session logs / outbox / harvest filings",
        ),
    }


def looks_like_xai_key(value: str) -> bool:
    return bool(_XAI_KEY_RX.match((value or "").strip()))


def redact_key(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return ""
    if looks_like_xai_key(v):
        return "xai-****<redacted>"
    if len(v) <= 8:
        return "<redacted>"
    return v[:4] + "****<redacted>"


def can_start_xai_setup(domain: str, go_id: str) -> tuple[bool, str]:
    ok, _detail = dns_gate.verify_go_id(domain, go_id)
    if not ok:
        return False, "dns_gate_failed"
    return True, "ok"


def device_key_locations(go_id: str) -> dict[str, str | None]:
    """Where the customer may keep the key. No repo secret path on Club infra."""
    _ = go_id  # go_id scopes the skill book session; key stays on device
    return {
        "browser": "localStorage key club-madeira-xai-key (pwa/skill-book)",
        "repo_secret_path": None,
    }


def setup_checklist() -> list[str]:
    return [
        "DNS Go-ID TXT verified (can_start_xai_setup)",
        "Customer creates an xAI account and buys credits / enables billing (browser)",
        "Customer generates an API key in the xAI console",
        "Enter key only in the skill-book PWA (localStorage) or OS secret store",
        "Never store the key in Club Madeira infra, logs, outbox, or public git",
        "Smoke: skill book call succeeds with customer tokens; redact_key in any diagnostics",
    ]
