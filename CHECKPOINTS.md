# CHECKPOINTS.md — "correct final state" criteria

A task is done when its checkpoint passes — executable where possible, observable otherwise.
These are the acceptance criteria for the whole system and for each domain.

## System health (`scripts/verify.sh` must end green)
- [ ] All fleet profiles exist (`ceo`, `finanzas`, `carrera`, `salud`, `research`) and respond to a
      Bot Chat ping.
- [ ] Exactly ONE profile owns the chat platform (Discord/WhatsApp) — the CEO. No token conflicts.
- [ ] All report crons deliver to `bot-chat:ceo` (or equivalent CEO channel); zero crons post raw
      output to the owner.
- [ ] Vault exists, is git-tracked, and `git status` is clean after each session.
- [ ] `.env` exists locally with required keys; no secrets appear in this repo or in chat.
- [ ] The CEO's last digest was delivered within its schedule window (no silent gap > 48h).

## Delivery protocol
- [ ] Every fleet bot's message to the owner went through CEO (verify CEO's digest references it).
- [ ] CEO digests: one message, merged/deduped, numbers over prose.
- [ ] Owner-facing posts land in the home channel / DM, not scattered channels.

## Finance (finanzas)
- [ ] Trackers (Sheets) updated with real data; formulas valid; `;`-separator es_ES locale respected.
- [ ] DCA plan numbers match the live portfolio; coast-fire target recomputed from current age/portfolio.
- [ ] Tax calendar posts correct deadlines for the current quarter.
- [ ] No fabricated numbers — if OAuth is dead, the report says so.

## Career (carrera)
- [ ] Digests include real, clickable source links with one-line context.
- [ ] Max 5 offers, match-scored against the owner's profile (XR/Unity/PM, Mid-Senior, Remote/Spain/EU).
- [ ] CV/brand deliverables are bilingual ES+EN and pass a visual check.

## Health (salud)
- [ ] Tracker updated with the owner's real input; trends flagged only when meaningful.
- [ ] One nudge per day max; recommendations are sustainable, not heroic.

## Research (research)
- [ ] Every claim has a cited, verifiable source with recency marker.
- [ ] Deliverable = brief (TL;DR, findings, sources, open questions, recommendation) saved to vault.
- [ ] House-hunting: criteria confirmed before listing comparisons.

## Cost discipline
- [ ] Weekly cloud spend ≤ budget (target €0–2/mo beyond base subscription); verified by the
      credit watchdog.
- [ ] No agent auto-switched models without the owner's explicit instruction.

## Migration / replication
- [ ] A fresh fork can go from clone to working fleet in < 1 hour using only this repo + `.env`
      (prove it: run the quickstart on a clean machine).
