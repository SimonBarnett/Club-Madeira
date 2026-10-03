"""Email campaign setup helpers for Club Madeira Skill (FR #2).

Runs only after DNS Go-ID gate + private Git working-data repo are ready.
Does not call live ESP APIs and never logs secrets.
"""
from __future__ import annotations

from typing import Any

from club_madeira import dns_gate

_PROVIDERS = ("sendgrid", "mailchimp", "resend")


def supported_providers() -> tuple[str, ...]:
    return _PROVIDERS


def credential_paths_for_go_id(go_id: str) -> dict[str, str]:
    repo = dns_gate.repo_name_for_go_id(go_id)
    return {
        "repo": repo,
        "email_tokens_rel": "credentials/email-provider.json",
        "readme_rel": "credentials/README.md",
    }


def can_start_email_setup(
    domain: str, go_id: str, *, repo_ready: bool
) -> tuple[bool, str]:
    ok, _detail = dns_gate.verify_go_id(domain, go_id)
    if not ok:
        return False, "dns_gate_failed"
    if not repo_ready:
        return False, "repo_not_ready"
    return True, "ok"


def provider_config_template(provider: str) -> dict[str, Any]:
    p = (provider or "").strip().lower()
    if p not in _PROVIDERS:
        raise ValueError(f"unsupported provider: {provider!r}; choose from {_PROVIDERS}")
    return {
        "provider": p,
        "fields": {
            "api_key": "",
            "from_email": "",
            "from_name": "Club Madeira",
            "list_or_audience_id": "",
        },
        "store_at": "credentials/email-provider.json",
        "notes": "Fill locally; never commit real keys to a public repo. Private Go-ID repo only.",
    }


def setup_checklist() -> list[str]:
    return [
        "DNS Go-ID TXT verified (verify_go_id)",
        "Private Git working-data repo ready (repo_name_for_go_id)",
        "Pick ESP provider from supported_providers()",
        "Customer creates ESP account and API key in browser",
        "Write provider_config_template into credentials/email-provider.json (private repo only)",
        "Smoke: send one test campaign/segment using customer tokens (out of band)",
    ]
