# Setup guide — new Hermes instance

> Use this to bootstrap a new Hermes Agent instance from scratch using the ai-os-personal-brain blueprint.
> Expected time: **~1 hour** to a working system with CEO + fleet + delivery loop.

## Prerequisites
- A [Hermes Agent](https://portal.nousresearch.com) instance (cloud VPS or local)
- Git installed (`git --version`)
- `uv` installed (for Python scripts)
- A Discord bot token + channel ID (if using Discord as chat platform)

## Step 1 — Clone repos

```bash
# Blueprint repo (public — fleet templates, docs, setup)
git clone git@github.com:DakkuaDev/ai-os-personal-brain.git ~/life-os

# Memory vault (private — clone YOUR copy; this repo is the blueprint)
git clone git@github.com:YOUR_USER/hermes-vault.git ~/vault
```

## Step 2 — Environment setup

```bash
cd ~/life-os
cp .env.example .env
# Edit .env: fill in the tokens (DISCORD, COMPOSIO, GOOGLE, NOTION...)
# Set OBSIDIAN_VAULT_PATH to your vault path (e.g. ~/vault)
```

> **Critical:** Never commit `.env`. Tokens stay in your machine's protected config.
> On Hermes /opt/data, `.env` already has keys — copy the missing ones.

## Step 3 — Composio connect (tool bridge)

```bash
# Install + login to Composio
pip install composio-core
composio login  # browser window opens; authenticate with personal account

# Add the apps you need
composio add github
composio add gmail
composio add googlecalendar
composio add googledocs
composio add googledrive
composio add googlesheets
composio add linkedin
composio add notion

# Verify
composio list --json | jq '.connectedAccounts[] | {app}'
# API key is auto-configured in Composio config; add COMPOSIO_API_KEY to .env
composio logout  # optional (key persists)
```

> **MCP endpoint:** `POST https://connect.composio.dev/mcp` with headers
> `Content-Type: application/json`, `Accept: application/json, text/event-stream`,
> `x-consumer-api-key: <COMPOSIO_API_KEY>`
>
> **Workflow:** `COMPOSIO_SEARCH_TOOLS` → `COMPOSIO_GET_TOOL_SCHEMAS` → `COMPOSIO_MULTI_EXECUTE_TOOL`
>
> Connected apps list grows — add more via `composio add <app>` dashboard.

## Step 4 — Create the fleet

```bash
python3 scripts/setup.py
```

The installer will ask:
- Owner name + email
- Personality (technical / practical / friendly)
- Default model (e.g. `ollama/qwen3:8b` or `deepseek/deepseek-v4-flash`)
- Model provider (ollama, nous, openai, openrouter...)
- Which agents you want (pick all 6 for a full fleet)
- Chat platform for CEO (discord / whatsapp / none)
- Vault path

After answering, you get:
- `lifeos.config.json` — all answers (gitignored)
- `generated/agents/<handle>.md` — one rendered SOUL per agent
- `generated/SETUP-NEXT-STEPS.md` — Hermes-specific commands

## Step 5 — Install profiles (Hermes Agent)

```bash
# Follow generated/SETUP-NEXT-STEPS.md or run:

# 1. Create profiles
for agent in ceo-bot finances-bot career-bot health-bot research-bot studies-bot; do
  hermes profile create $agent --no-skills --description "Life OS: $agent"
done

# 2. Set models
for agent in ceo-bot finances-bot career-bot health-bot research-bot studies-bot; do
  hermes -p $agent config set model.default <model>
  hermes -p $agent config set model.provider <provider>
done

# 3. Install SOULs
for agent in ceo-bot finances-bot career-bot health-bot research-bot studies-bot; do
  cp generated/agents/$agent.md ~/.hermes/profiles/$agent/SOUL.md
done

# 4. Wire Discord (CEO only — no other bot should own the gateway)
hermes -p ceo-bot config set platforms.discord.enabled true
# Add DISCORD_BOT_TOKEN, ALLOWED_USERS, HOME_CHANNEL to ~/.hermes/profiles/ceo-bot/.env
# REMOVE Discord tokens from all other profiles' .env files
```

> **One-owner rule:** Only the CEO profile may have a Discord gateway token.
> If other profiles have Discord credentials, remove them — otherwise the
> gateway multiplexer will refuse to run.

## Step 6 — Verify

```bash
cd ~/life-os
bash scripts/verify.sh
# Must end green (exit 0). If it fails, read the specific check and fix.
```

## Step 7 — First delivery loop test

1. Fire a silent cron: `hermes -p ceo-bot chat -Q -q "ping"` → CEO should reply
2. Test fleet delegation: message CEO "ask finance for a simple portfolio check"
3. CEO should forward to `finances-bot` and relay the reply back

## Step 8 — Restore vault memory

```bash
cd ~/vault
cp -r . ~/vault  # (already from clone step)
# The vault auto-syncs daily; for first run, verify git status is clean
git status
```

> The vault IS the memory layer — CRITICAL_FACTS, Memory/, Control/, Logs/.
> The blueprint repo IS the how-to — keep them separate.

## Next steps (after first boot)
- Set up daily heartbeat cron (09:00 UTC)
- Set up weekly Life OS check (Monday)
- Review CHECKPOINTS.md — ensure each domain's acceptance criteria pass
- Wire additional cron jobs for your specific automations (finance tracking, job hunts, etc.)
