"""Skill book PWA delivery helpers (FR #5). Online-only v1."""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode, urljoin

from club_madeira.dns_gate import verify_go_id


def skill_book_delivery_url(*, public_base: str, go_id: str, domain: str) -> str:
    """Link delivered after successful onboarding / DNS gate."""
    base = (public_base or "").rstrip("/") + "/"
    path = urljoin(base, "skill-book/index.html")
    q = urlencode({"go": go_id or "", "domain": domain or ""})
    return f"{path}?{q}"


def can_deliver_skill_book(
    domain: str, go_id: str, *, public_base: str
) -> tuple[bool, dict[str, Any]]:
    """Only deliver the PWA link when the DNS Go-ID gate passes."""
    ok, detail = verify_go_id(domain, go_id)
    if not ok:
        return False, {"reason": "dns_gate_failed", "dns": detail}
    url = skill_book_delivery_url(public_base=public_base, go_id=go_id, domain=domain)
    return True, {"url": url, "online_only": True}
