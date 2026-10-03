# UAT v0.1.0 — Club-Madeira repo acceptance

**Verdict: UAT PASS**
**Commit tested:** `9f59dfca43751f850c71fcbb77302553d5669b2d` (main)
**Machine:** WIN-MPRE8VI4U6U (worker seat win-mpre8vi4u6u-20596)
**Suite:** `PYTHONPATH=src python -m pytest tests -q` → **39 passed**

Repo was clear at assign: 0 open issues, 0 open PRs. Closed FRs #1–#5; merged cycle includes #6–#13.

## Vision success criteria

| # | Criterion | Evidence | Result |
|---|-----------|----------|--------|
| 1 | DNS gate `verify_go_id` ok only when matching TXT present | Unit tests in `tests/test_dns_gate.py` (match/miss/mismatch/blank); live `example.com` fail-closed `go_id_not_found` | PASS |
| 2 | Repo name `club-madeira-<sanitized-go-id>` | `repo_name_for_go_id("GO-42")` → `club-madeira-go-42`; path tricks sanitized | PASS |
| 3 | Skill covers DNS → Git → email → X → xAI → PWA | `.grok/skills/club-madeira-skill/SKILL.md` Flow steps 1–6; modules in Code section | PASS |
| 4 | xAI key never in Club infra; private repo default; DNS re-check | `storage_policy.store_in_club_madeira_infra is False`; PWA `localStorage` `club-madeira-xai-key`; skill "Re-check later (DNS TTL can linger)"; `verify_go_id` re-callable (no one-shot cache). TTL SOA parser not shipped — operator/skill practice is the measure for v0.1.0 | PASS |

## Out-of-scope (confirmed not implemented — correct)

- Full voice agent runtime
- Live ESP / X API / xAI billing HTTP automation

## Module smoke (merged main)

- Email: providers sendgrid/mailchimp/resend; gate needs DNS + `repo_ready`
- X: pricing ack required before continue; credentials path under private Go-ID repo
- xAI: redact + device locations only (`repo_secret_path` is None)
- PWA: online-only SW (no Cache Storage); manifest installable

## Visual (PWA source review)

| gate | where | expected | actual | severity | delta_px | delta_hex |
|------|-------|----------|--------|----------|----------|-----------|
| G1 | index.html copy | Club Madeira Skill Book; device-local key note | Matches; UTF-8 em dash / middle dot | none | n/a | n/a |
| G3 | controls | password field + Save; no server upload chrome | Matches brief / FR #5 | none | n/a | n/a |

Pixel G2 against a design mock: **could not test** (no mock fixtures in repo). Browser installability on customer Win/Mac: **could not test** in this seat.

## Reviewer note

This seat also ran MRB for PR #10; chair still assigned repo UAT (ledger offered).

## Release

Tag **v0.1.0** after this docs PR merges.
