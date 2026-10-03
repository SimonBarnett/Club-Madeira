"""FR #5: Club Madeira skill book PWA (online-only v1)."""
from __future__ import annotations

import json
from pathlib import Path

import club_madeira.skill_book as sb

ROOT = Path(__file__).resolve().parents[1]
PWA = ROOT / "pwa" / "skill-book"


def test_manifest_is_installable_pwa():
    data = json.loads((PWA / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert data["name"]
    assert data["start_url"]
    assert data["display"] in ("standalone", "minimal-ui")
    assert data.get("offline") is not True
    assert "icons" in data and len(data["icons"]) >= 1


def test_index_has_customer_xai_key_field_not_server_store():
    html = (PWA / "index.html").read_text(encoding="utf-8")
    assert 'type="password"' in html or "xai" in html.lower()
    assert "localStorage" in html or "sessionStorage" in html
    assert "never sent to Club Madeira servers" in html or "stays on this device" in html.lower()


def test_service_worker_is_online_only_no_cache_shell():
    sw = (PWA / "sw.js").read_text(encoding="utf-8")
    assert "online-only" in sw.lower() or "ONLINE_ONLY" in sw
    assert "caches.open" not in sw
    assert "cache.add" not in sw.lower()


def test_delivery_link_after_onboarding():
    url = sb.skill_book_delivery_url(
        public_base="https://skills.example.com",
        go_id="GO-42",
        domain="club.example.com",
    )
    assert url.startswith("https://skills.example.com/")
    assert "GO-42" in url or "go=" in url.lower()
    assert "club.example.com" in url or "domain=" in url


def test_delivery_blocked_until_dns_ok(monkeypatch):
    import club_madeira.dns_gate as gate

    monkeypatch.setattr(gate, "verify_go_id", lambda d, g: (False, {"reason": "go_id_not_found"}))
    ok, detail = sb.can_deliver_skill_book("example.com", "GO-42", public_base="https://x.test")
    assert ok is False
    assert detail["reason"] == "dns_gate_failed"
