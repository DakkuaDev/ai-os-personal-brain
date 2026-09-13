# Architecture

## The pattern
A personal AI operation system in three layers:

```
                ┌─────────────────────────────────────────────┐
                │  CLOUD (front door, always-on)              │
                │  CEO bot — orchestrator + SINGLE DELIVER    │
                │  agent (Discord now, WhatsApp later)        │
                │  rescue model (frontier, on demand only)    │
                │  critical no_agent crons (€0, 24/7)         │
                └──────────────┬──────────────────────────────┘
                               │ ① chat messages (24/7)
                               │ ② peer DM / API bridge
                               │ ③ rescue escalation (local → cloud)
                ┌──────────────▼──────────────────────────────┐
                │  LOCAL (brain) — open-source models (Ollama)│
                │  €0 runtime                                 │
                │                                             │
                │  CEO (orchestrator) ← talks to the owner    │
                │  ├── finance  ·  career  ·  health         │
                │  └── research                               │
                │                                             │
                │  Obsidian vault (memory layer) · crons      │
                │  Desktop app (direct local connection)      │
                └──────────────┬──────────────────────────────┘
                               │ Tailscale (reachable anywhere)
                               ▼
                          PHONE (WhatsApp / mobile data)
```

## Delivery model (the core invariant)
1. All cron reports deliver into CEO's Bot Chat (`deliver=bot-chat:ceo` in Hermes cron terms).
2. Fleet bots message CEO with summaries after every meaningful task.
3. CEO merges/dedupes into ONE digest and posts it to the owner (home channel / DM).
4. Owner replies only to CEO. CEO decides: answer, delegate to a bot, or escalate to cloud rescue.

## Bridge (local ↔ cloud)
- **Tailscale** mesh (laptop + phone + cloud VPS): the local node is reachable from anywhere
  without public IP/port forwarding.
- **Peer registration** (`hermes peer add`): bots on different machines DM each other natively
  (`hermes peer dm`, `message_agent`).
- **Relay bot** (cloud, free model): owner's chat message → forwards to local CEO → returns reply.
- **Escalation**: local CEO requests a frontier/cloud model via peer DM when a task genuinely needs
  it; result relayed back. Gated by cost discipline.

## Reachability truth
Chat platforms connect over the internet, not the LAN — the local machine does NOT need to share
WiFi with the phone. What matters: the machine is on, online, and the chat session is alive.
Tailscale covers API/peer access.

## Why local-first
- €0 runtime with open-source models; cloud subscription reserved for the always-on front door.
- Data (vault, trackers, conversations) stays on hardware the owner controls.
- Cloud keeps only what must run 24/7: the chat front door, rescue model, critical no_agent crons.

## Portability
SOULs + skills + vault rules live in this repo. Profiles/machines are disposable: rebuild a fleet
from `agents/` + `profiles/` + `skills/` in under an hour (see CHECKPOINTS.md migration criteria).
