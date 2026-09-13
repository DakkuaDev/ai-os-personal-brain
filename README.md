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
                │  ├── finanzas  · career  · health    │
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
2. Copy `.env.example` → `.env` and fill in your tokens (Discord/WhatsApp, model provider, Sheets/Notion).
3. `./scripts/verify.sh` — must end green.
4. Read `AGENTS.md` — it tells any agent how to run this system.
5. Create the fleet profiles (Hermes: `hermes profile create <name> --no-skills`) and give each
   bot its SOUL from `agents/<role>.md` + the skills listed there.
6. Talk to CEO. Delegate. Watch it manage the fleet.

## Structure

```
├── AGENTS.md              # Map for any AI agent (progressive disclosure)
├── CHECKPOINTS.md         # "Correct final state" criteria per domain
├── README.md              # this file
├── LICENSE                # MIT
├── agents/                # SOUL templates per role (the fleet's identity)
│   ├── ceo.md             #   orchestrator + single deliver agent
│   ├── finanzas.md        #   personal finance
│   ├── carrera.md         #   career & job hunting
│   ├── salud.md           #   health / exercise / diet
│   └── research.md        #   deep research (house, skills, business)
├── profiles/              # per-bot: config + skill manifest (which skills, which tools)
├── skills/                # portable procedural skills (shared by the fleet)
├── scripts/               # bridge relay, no_agent crons, verify.sh
├── docs/
│   ├── architecture.md    # the full diagram + delivery model
│   ├── conventions.md     # vault rules, model posture, naming
│   └── verification.md    # how to prove the system works
├── templates/             # new-agent bootstrap (SOUL + skills + routine)
└── progress/              # current.md (live state) + history.md (append-only log)
```

## Replicating for someone else

This repo is designed to be forked per person: replace the placeholders, adjust the fleet to
their life (add a `kids` bot, drop `research`), and keep the plumbing identical. The plumbing —
CEO delivery protocol, peer bridge, verification, vault rules — is the part worth keeping.
