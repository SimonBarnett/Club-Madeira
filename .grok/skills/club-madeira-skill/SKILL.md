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
3. **Email campaign setup** — configure customer tooling (follow-up FR).
4. **Twitter / X** — customer signs up for X API (pay-per-use as of 2026); surface pricing before mid-setup paywall (follow-up FR).
5. **xAI API key** — customer creates their own xAI account/credits; skill book runs on **their** tokens only (follow-up FR).
6. **Skill book PWA** — deliver installable web skill book link after successful onboarding (follow-up FR). Online-only OK for v1.

## Security

- Never store customer xAI keys in Club Madeira infra.
- Private repo by default; no shared credentials.
- Go ID JWT (~2h) is delivery-only; long-term proof is DNS.

## Code

- `src/club_madeira/dns_gate.py` — parse / verify / repo naming
- `tests/test_dns_gate.py` — unit gates
