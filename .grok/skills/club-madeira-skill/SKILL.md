---
name: club-madeira-skill
description: >
  Post-onboarding Club Madeira skill: DNS Go-ID gate, private working-data repo,
  then email / X / xAI / PWA setup. Use when Go ID TXT is live or the customer is
  ready for club infrastructure setup.
---

# Club Madeira Skill

## When to start

1. Onboarding has issued a **Go ID**.
2. Customer created a DNS TXT on their domain: `club-madeira-go=<GoId>`.
3. Run the DNS gate before any Git / email / X / xAI step.

```powershell
$env:PYTHONPATH = "src"
python -c "from club_madeira.dns_gate import verify_go_id; print(verify_go_id('example.com','GO-42'))"
```

## Flow (order is CAST IRON)

1. **DNS verification** — `verify_go_id(domain, go_id)`. Fail closed if missing/mismatch. Re-check later (DNS TTL can linger).
2. **Git working-data repo** — create private repo `repo_name_for_go_id(go_id)` under the customer's GitHub; deploy key or fine-grained token scoped to that repo only.
3. **Email campaign setup** (FR #2) — only after DNS + private repo ready
   (`can_start_email_setup`). Pick a provider from `supported_providers()`,
   store config at `credentials/email-provider.json` via `provider_config_template`.
   Never log API keys.
4. **Twitter / X** (FR #3) — **before** any token paste:
   - Print `club_madeira.x_setup.pricing_brief()` (2026 pay-per-use; Basic/Pro retired).
   - Require `acknowledge_pricing` / `can_continue_past_pricing` ok.
   - Customer creates X developer app; store tokens only at `credentials/x-api-tokens.json` in the private Go-ID repo (`credential_paths_for_go_id`). Never log secrets.
5. **xAI API key** (FR #4) — after DNS gate (`can_start_xai_setup`):
   customer creates xAI account/credits in browser; enter key only in skill-book PWA
   `localStorage` (`device_key_locations`). `storage_policy.store_in_club_madeira_infra`
   is false. Use `redact_key` in any diagnostics; never log the raw key.
6. **Skill book PWA** (FR #5) — after DNS gate passes, deliver
   `club_madeira.skill_book.skill_book_delivery_url(...)` pointing at `pwa/skill-book/`.
   Online-only v1 (service worker does not cache). Customer enters xAI key on the PWA page;
   key stays in `localStorage` on their device.

## Security

- Never store customer xAI keys in Club Madeira infra.
- Private repo by default; no shared credentials.
- Go ID JWT (~2h) is delivery-only; long-term proof is DNS.

## Code

- `src/club_madeira/dns_gate.py` — parse / verify / repo naming
- `tests/test_dns_gate.py` — unit gates
