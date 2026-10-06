# History (append-only)

2026-09-13 — Repo scaffolded: README, AGENTS.md, CHECKPOINTS.md, docs/, agents/ (5 role templates),
templates/new-agent.md, scripts/verify.sh, .env.example, LICENSE. Fleet live on cloud: ceo
(deliver agent, owns Discord), finance, career, health, research. 14 crons → bot-chat:ceo-bot.

2026-10-06 — NEW: studies-bot agent template + fleet everywhere (AGENTS, CHECKPOINTS, verify.sh, setup.py). Composio MCP docs (integrations, .env.example, architecture). New docs: setup/step-by-step guide, daily-use (rhythm + how to talk to CEO), deployment (cloud/local/hybrid, backup/restore), principles (9 researched best practices). Fixes: ai-so→ai-os repo typo, progress/current.md stale ref, ceo-bot-bot typo in CHECKPOINTS. README structure tree + 6 agents + new doc pointers.

2026-10-06 — FLEXIBILITY RELEASE: repo is now a per-person template, not a snapshot.
  • 3 deployment profiles (local / cloud / hybrid) — docs/deployment.md + installer asks first.
  • Optional modules per person: Obsidian vault, Composio, chat gateway, custom bots.
  • agents/custom-bot.md — generic template; setup.py accepts extra custom domains (renders kids-bot/home-bot style bots).
  • verify.sh is config-driven: fleet from lifeos.config.json; vault/composio/platform checks skipped when module off (tested with minimal 1-bot config: green).
  • setup.py: profile-aware defaults (local→ollama, cloud/hybrid→nous), vault/composio yes-no, custom-bot prompt, SETUP-NEXT-STEPS only includes enabled modules (tested: local/no-vault/no-composio run renders 8 bots, 0 unresolved placeholders).
  • README: banner (assets/banner.svg + banner.png), deployment table, module matrix, replicable-for-anyone framing.
  • docs: setup.md and deployment.md rewritten profile-first; architecture/integrations/AGENTS/CHECKPOINTS/.env.example marked module-optional.
