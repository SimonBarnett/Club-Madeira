# Club-Madeira

Top-level Club Madeira umbrella: onboarding skill pack and **Club Madeira Skill** (post-onboarding).

**Version:** see [VERSION](./VERSION) (UAT release **v0.1.0** — [docs/uat-v0.1.0.md](./docs/uat-v0.1.0.md)).

## Vision

See [VISION.md](./VISION.md). Ownership gate is a DNS TXT `club-madeira-go=<GoId>`.

## Layout

| Path | Role |
|------|------|
| `VISION.md` | Product vision / success gates |
| `VERSION` | Release version |
| `.grok/skills/club-madeira-skill/` | Agent skill playbook |
| `src/club_madeira/` | DNS, email, X, xAI, skill-book helpers |
| `pwa/skill-book/` | Online-only skill book PWA (customer xAI key in localStorage) |
| `tests/` | Unit + hostile MRB coverage |
| `docs/` | Phase notes + UAT evidence |

## Quick test

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests -q
```

## Status (v0.1.0)

Foundation + email (#2) + X pricing gate (#3) + xAI customer-token policy (#4) + skill-book PWA (#5) in tree. Live ESP/X/xAI HTTP and full voice runtime remain out of scope.
