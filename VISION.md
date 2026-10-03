# Vision — Club Madeira Skill (post-onboarding)

## Purpose

After the onboarding agent issues a **Go ID**, the Club Madeira Skill (voice + skill book) walks the customer through club infrastructure setup and saves working data to a **private Git repo** named after that Go ID.

## Trigger

Start when the Go ID appears as a DNS **TXT** record on the customer's domain (same record onboarding asked them to create). DNS presence is the gate — no separate activation step.

TXT forms accepted:

- `club-madeira-go=<GoId>`
- `club-madeira-go: <GoId>`

## Success (measurable)

1. **DNS gate:** given domain + expected Go ID, `verify_go_id` returns ok only when a matching TXT is present (unit-tested; live lookup optional with dnspython/nslookup).
2. **Repo naming:** private working-data repo name is deterministic and safe: `club-madeira-<sanitized-go-id>`.
3. **Skill book:** a documented agent skill (`.grok/skills/club-madeira-skill`) covers the flow order: DNS → Git repo → email → X → xAI key → PWA link.
4. **Security:** customer xAI API key never stored in Club Madeira infrastructure; private repo by default; periodic DNS re-check (TTL-aware) rather than one-shot trust.

## Out of scope for FR #1 foundation PR

- Full voice agent runtime (PWA shell + delivery link shipped in FR #5; voice runtime later).
- Live ESP HTTP sends (FR #2 ships checklist + credential template; customer still configures the vendor in browser).
- Live X API HTTP calls (FR #3 ships pricing ack + credential path; customer still signs up in browser).
- Live xAI billing / credit purchase automation (follow-up FR).

## LOCKED

- Umbrella repo: `SimonBarnett/Club-Madeira`
- Ownership proof: DNS TXT Go ID
- Customer tokens stay on customer side
