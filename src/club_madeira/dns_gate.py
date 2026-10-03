"""DNS Go-ID TXT verification — ownership gate for the Club Madeira skill (FR #1).

TXT form (either):
  club-madeira-go=<GoId>
  club-madeira-go: <GoId>
"""
from __future__ import annotations

import re
import socket
from typing import Any

_GO_TXT_RX = re.compile(
    r"(?i)^\s*club-madeira-go\s*[=:]\s*([A-Za-z0-9._\-]+)\s*$"
)
_UNSAFE_REPO = re.compile(r"[^A-Za-z0-9._\-]+")


def normalize_domain(domain: str) -> str:
    d = (domain or "").strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0].rstrip(".")
    return d


def parse_go_id_txt(value: str) -> str | None:
    m = _GO_TXT_RX.match((value or "").strip().strip('"'))
    return m.group(1) if m else None


def lookup_txt(domain: str) -> list[str]:
    """Resolve TXT records. Overridable in tests."""
    d = normalize_domain(domain)
    if not d:
        return []
    try:
        answers = socket.getaddrinfo  # noqa: F841 — keep import side effects minimal
    except Exception:
        pass
    try:
        import dns.resolver  # type: ignore

        r = dns.resolver.resolve(d, "TXT")
        out: list[str] = []
        for rr in r:
            # dnspython returns quoted chunks
            text = b"".join(rr.strings).decode("utf-8", errors="replace") if hasattr(rr, "strings") else str(rr).strip('"')
            out.append(text)
        return out
    except ImportError:
        # stdlib fallback via nslookup-style: use getaddrinfo unavailable for TXT;
        # return empty so callers treat as not found unless dnspython is installed.
        return _lookup_txt_nslookup(d)
    except Exception:
        return []


def _lookup_txt_nslookup(domain: str) -> list[str]:
    """Best-effort Windows/Linux nslookup parse when dnspython is absent."""
    import subprocess

    try:
        p = subprocess.run(
            ["nslookup", "-type=TXT", domain],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return []
    out: list[str] = []
    for line in (p.stdout or "").splitlines():
        if "text =" in line.lower() or '="' in line:
            m = re.search(r'"([^"]+)"', line)
            if m:
                out.append(m.group(1))
    return out


def verify_go_id(domain: str, expected_go_id: str) -> tuple[bool, dict[str, Any]]:
    """Return (ok, detail). DNS presence of the Go ID is the ownership proof."""
    d = normalize_domain(domain)
    expected = (expected_go_id or "").strip()
    detail: dict[str, Any] = {"domain": d, "expected": expected}
    if not d or not expected:
        detail["reason"] = "missing_domain_or_go_id"
        return False, detail
    records = lookup_txt(d)
    detail["txt_count"] = len(records)
    found: list[str] = []
    for raw in records:
        gid = parse_go_id_txt(raw)
        if gid:
            found.append(gid)
            continue
        # Some resolvers glue adjacent TXT strings; scan for the key inline.
        m = re.search(r"(?i)club-madeira-go\s*[=:]\s*([A-Za-z0-9._\-]+)", raw or "")
        if m:
            found.append(m.group(1))
    detail["found"] = found
    if not found:
        detail["reason"] = "go_id_not_found"
        return False, detail
    if expected not in found:
        detail["reason"] = "go_id_mismatch"
        return False, detail
    detail["matched"] = expected
    return True, detail


def repo_name_for_go_id(go_id: str) -> str:
    """Private working-data repo name derived from the Go ID."""
    raw = (go_id or "").strip().replace("\\", "/").lower()
    # Drop path tricks (.. / .) before sanitising.
    parts = [p for p in raw.split("/") if p and p not in (".", "..")]
    joined = "-".join(parts) if parts else "unknown"
    safe = _UNSAFE_REPO.sub("-", joined)
    safe = re.sub(r"-{2,}", "-", safe).strip("-._")
    if not safe:
        safe = "unknown"
    return f"club-madeira-{safe}"
