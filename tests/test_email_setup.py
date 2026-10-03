"""FR #2: email campaign setup after DNS + Git gate."""
from __future__ import annotations

import club_madeira.email_setup as es


def test_supported_providers_listed():
    providers = es.supported_providers()
    assert "sendgrid" in providers
    assert "mailchimp" in providers
    assert "resend" in providers


def test_credential_paths_for_go_id():
    paths = es.credential_paths_for_go_id("GO-42")
    assert paths["repo"] == "club-madeira-go-42"
    assert paths["email_tokens_rel"].startswith("credentials/")
    assert "password" not in paths["email_tokens_rel"].lower()


def test_gate_requires_dns_and_repo_ready(monkeypatch):
    import club_madeira.dns_gate as gate

    monkeypatch.setattr(gate, "verify_go_id", lambda d, g: (False, {"reason": "go_id_not_found"}))
    ok, why = es.can_start_email_setup("example.com", "GO-42", repo_ready=True)
    assert ok is False
    assert why == "dns_gate_failed"

    monkeypatch.setattr(gate, "verify_go_id", lambda d, g: (True, {"matched": "GO-42"}))
    ok2, why2 = es.can_start_email_setup("example.com", "GO-42", repo_ready=False)
    assert ok2 is False
    assert why2 == "repo_not_ready"

    ok3, why3 = es.can_start_email_setup("example.com", "GO-42", repo_ready=True)
    assert ok3 is True
    assert why3 == "ok"


def test_provider_config_template_has_no_secrets():
    cfg = es.provider_config_template("sendgrid")
    assert cfg["provider"] == "sendgrid"
    assert "api_key" in cfg["fields"]
    blob = str(cfg)
    assert "SG." not in blob
    assert "secret" not in blob.lower() or cfg["fields"]["api_key"] == ""


def test_setup_checklist_orders_dns_git_before_vendor():
    steps = es.setup_checklist()
    assert steps[0].lower().startswith("dns") or "dns" in steps[0].lower()
    assert any("repo" in s.lower() or "git" in s.lower() for s in steps[:3])
    assert any("provider" in s.lower() or "send" in s.lower() for s in steps)
