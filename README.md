# Club-Madeira

Top-level Club Madeira umbrella: onboarding skill pack and **Club Madeira Skill** (post-onboarding).

## Vision

See [VISION.md](./VISION.md). Ownership gate is a DNS TXT `club-madeira-go=<GoId>`.

## Layout

| Path | Role |
|------|------|
| `VISION.md` | Product vision / success gates |
| `.grok/skills/club-madeira-skill/` | Agent skill playbook |
| `src/club_madeira/` | DNS gate + helpers |
| `tests/` | Unit tests |
| `docs/` | Phase notes |

## Quick test

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests -q
```

## FR #1 status

Foundation shipped: vision, skill playbook, DNS Go-ID gate + tests. Email / X / xAI / PWA are follow-up FRs.
