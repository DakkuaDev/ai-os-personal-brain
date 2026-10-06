# Agent-First Life OS

An **AI-agnostic, replicable blueprint** for a personal "operating system" built around a fleet
of specialist AI agents, orchestrated by a single **CEO agent** that makes the decisions and is
the **only agent that talks to you** — everything else reports to it.

Built and tested with [Hermes Agent](https://hermes-agent.nousresearch.com) (works with any agent
that can read `AGENTS.md` — Claude Code, Codex, OpenCode, Gemini CLI, …). Inspired by the
[Harness Engineering](https://github.com/betta-tech/ejemplo-harness-subagentes) pattern:
**the repo IS the system**, state lives on disk (not in chat), verification is executable.

> ⚠️ **Sanitized for sharing.** Replace `{{OWNER_NAME}}`, `{{OWNER_EMAIL}}` and any personal IDs
> (Sheets, Notion, channels) with your own. Never commit secrets or tokens — they belong in
> `.env` files that this repo never touches.

## The pattern in one picture

```
                ┌──────────────────────────────────────┐
                │  CLOUD (front door, always-on)       │
                │  CEO bot — orchestrator + SINGLE     │
                │  deliver agent (Discord / WhatsApp)  │
                └───────────────┬──────────────────────┘
                                │ messages in (chat)
                                │ peer bridge / API
                ┌───────────────▼──────────────────────┐
                │  LOCAL (brain, open-source models)   │
                │  CEO (orchestrator) ← talks to you   │
                │  ├── finance  · career  · health    │
                │  └── research                       │
                │  Obsidian vault (memory layer)       │
                └──────────────────────────────────────┘
```

**Rules that make it work:**
1. **One deliver agent.** All fleet and cron reports flow to CEO. CEO synthesizes → posts ONE
   digest. No raw output reaches you unprocessed.
2. **Local-first, cloud as rescue.** Open-source models (Ollama) for daily work; a paid/frontier
   model only when a task genuinely needs it — and only on explicit request.
3. **Minimum viable bot.** A new agent exists only when a domain has recurring, distinct work a
   skill or cron can't cover. Prefer skill > cron > new bot.
4. **State on disk.** The vault (or any markdown store) is the memory layer; `progress/` is the
   audit trail. Context windows die; files don't.
5. **Executable verification.** `scripts/verify.sh` checks the system is healthy. Don't trust the
   agent's self-report.

## Quickstart

1. Clone this repo.
2. **Run the installer:** `python3 scripts/setup.py` — it asks who you are, which agents you
   want, their nicknames + handles, the model/provider, the AI personality (technical / practical /
   friendly), the chat platform, and the vault path. It renders your fleet:
   - `lifeos.config.json` (your answers)
   - `generated/agents/<handle>.md` (one ready-to-install SOUL per bot)
   - `generated/SETUP-NEXT-STEPS.md` (exact commands to create the fleet)
3. Copy `.env.example` → `.env` and fill in your tokens (Discord/WhatsApp, model provider, sheets/Notion).
4. `./scripts/verify.sh` — must end green.
5. Read `AGENTS.md` — it tells any agent how to run this system.
6. Talk to CEO. Delegate. Watch it manage the fleet.

> **Nicknames:** every bot has a display name (e.g. CEO = *Aegis*, finance = *Midas*) plus a
> functional handle (e.g. `ceo-bot`, `finances-bot`). Handles stay searchable and taggable;
> nicknames give them personality. Change them anytime in the installer or the config.

## Structure

```
├── AGENTS.md              # Map for any AI agent (progressive disclosure)
├── CHECKPOINTS.md         # "Correct final state" criteria per domain
├── README.md              # this file
├── LICENSE                # MIT
├── agents/                # SOUL templates per role (the fleet's identity)
│   ├── ceo-bot.md         #   orchestrator + single deliver agent
│   ├── finances-bot.md    #   personal finance (Midas)
│   ├── career-bot.md      #   career & job hunting (Compass)
│   ├── health-bot.md      #   health / exercise / diet (Vital)
│   ├── research-bot.md    #   deep research (Sage)
│   └── studies-bot.md     #   academic study (Scholar)
├── profiles/              # per-bot: config + skill manifest (which skills, which tools)
├── skills/                # portable procedural skills (shared by the fleet)
├── scripts/               # bridge relay, no_agent crons, verify.sh
├── docs/
│   ├── architecture.md    # the full diagram + delivery model
│   ├── memory-layer.md    # the vault: role, contract, and why it's a SEPARATE repo
│   ├── conventions.md     # vault rules, model posture, naming
│   ├── verification.md    # how to prove the system works
│   ├── setup.md           # new-instance bootstrap guide (~1h to working system)
│   ├── integrations.md    # Composio MCP + Discord + Google + Notion + GitHub connections
│   ├── daily-use.md       # daily cron rhythm, how to talk to CEO, weekly maintenance
│   ├── deployment.md      # cloud/local/hybrid options, backup/restore, secrets
│   └── principles.md      # the 'why' — researched best practices behind the architecture
├── templates/             # new-agent bootstrap (SOUL + skills + routine)
└── progress/              # current.md (live state) + history.md (append-only log)
```

## Replicating for someone else

This repo is designed to be forked per person: replace the placeholders, adjust the fleet to
their life (add a `kids` bot, drop `research-bot`), and keep the plumbing identical. The plumbing —
CEO delivery protocol, peer bridge, verification, vault rules — is the part worth keeping.
