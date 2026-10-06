# Deployment — profiles, not presets

> This blueprint is deployment-agnostic: **one pattern, three profiles, optional modules**.
> Pick the profile per person — the plumbing (CEO delivery, verification, memory rules)
> stays identical everywhere.

## A. Local-only — laptop/desktop (client, private, single machine)

```
┌───────────────────────────────┐
│  YOUR LAPTOP                  │
│  Hermes + Ollama (€0 models)  │
│  CEO ── finance · career · …  │
│  Desktop app = front door     │
│  Vault (optional) on disk     │
└───────────────────────────────┘
```

- **Models:** local, open-source (Ollama: qwen3, llama, deepseek-distill…) — €0 inference.
- **Front door:** the Hermes desktop app. No Discord/WhatsApp needed (optional if wanted).
- **Always-on:** no — only when the machine is running. Fine for private use.
- **Inbound access:** full freedom (no firewall weirdness) — can even expose APIs via Tailscale.
- **Pros:** €0, private, you own everything. **Cons:** not 24/7, laptop is the bottleneck.
- **Modules that make sense:** vault optional, Composio optional, gateway usually off.

## B. Cloud VPS — hosted, always-on (partner, family member, remote client)

```
┌──────────────────────────────────┐
│  HOSTED VPS / PORTAL INSTANCE    │
│  Hermes, always-on               │
│  CEO owns Discord/WhatsApp       │
│  Dashboard = web front door      │
│  Vault (optional) synced to git  │
└──────────────────────────────────┘
```

- **Models:** hosted provider (Nous subscription, OpenRouter, etc.) — free/cheap tiers by
  default, frontier only on demand.
- **Front door:** chat gateway on CEO (Discord DM/channel or WhatsApp later).
- **Always-on:** yes — crons, heartbeats, digests run 24/7.
- **Inbound limit:** a hosted container usually exposes only its dashboard (no public ports).
  WhatsApp webhooks need a relay (e.g. a tiny queue you poll) — see the hybrid pattern.
- **Pros:** works from anywhere, no machine dependency. **Cons:** small monthly cost, less privacy.
- **Modules that make sense:** gateway on, Composio on, vault optional (the person may not
  care about notes — keep it simple).

## C. Hybrid — cloud front door + local workers (power user)

```
        CLOUD (24/7)                    LOCAL (when you're home)
  ┌──────────────────────┐        ┌──────────────────────────┐
  │ CEO — owns chat      │◀──────▶│ workers: research, heavy │
  │ cron + heartbeat     │ bridge  │ finance, local models   │
  │ rescue model on call │        │ vault workspace          │
  └──────────────────────┘        └──────────────────────────┘
         │  Tailscale / peer bridge (private network tunnel)
         ▼
      PHONE (WhatsApp / mobile)
```

- **Cloud:** CEO + gateway + crons + rescue — always reachable.
- **Local:** heavyweight workers (deep research, big computations) with local models = €0.
- **Bridge:** peer DMs or a Tailscale tunnel; the cloud relays results through CEO.
- **Pros:** best of both. **Cons:** more moving parts — worth it only for power users.

## Choosing for someone else (worked examples)

| Person | Profile | Modules | Bots |
|---|---|---|---|
| Non-technical partner | `cloud` | gateway ON · Composio ON (the apps they use) · vault OFF | CEO + 2–3 (finance, health…) |
| Client / single machine | `local` | gateway OFF · Composio OFF or minimal · vault OFF | CEO + 1–2 domain bots |
| Power user (e.g. the repo owner) | `hybrid` | everything ON + custom bots | full fleet + own domains |

Keep it smaller than you think necessary: **fewer bots and modules = easier to maintain**,
and the pattern lets you add more later without rework.

## Backup & restore

### Native full backup (Hermes) — every profile
```bash
hermes backup          # zip + sha256 of config, skills, sessions, cron, memory, profile data
hermes import <zip>    # exact clone on a new machine
```

### Selective restore
- **Vault alone:** `git clone <vault-repo>` (it's a git repo by design).
- **Blueprint + config:** this repo + `lifeos.config.json` (keep a private copy of that file).
- **Crons:** re-created from `progress/history.md` + `docs/daily-use.md` notes.

## Secrets

- Never put tokens, API keys, or credentials in any repo — they belong in `.env`
  (gitignored) or the runtime's protected config.
- Vault rule: refer to secrets **by name**, never by value.
- Before committing anything: `grep -rnE "(sk-|ghp_|ck_|AKIA|AIza)" .` — catches pasted keys.

## Hosted-instance constraints (know before you choose B or C)

- The machine has **no public IP**: the dashboard URL is the only inbound route; you cannot
  expose other ports or receive webhooks directly.
- You **cannot install long-running services** beyond the agent itself.
- Machine lifecycle, billing, and subscription are managed from the hosting portal — not by
  the agent.
