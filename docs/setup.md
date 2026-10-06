# Setup guide — new Hermes instance

> Use this to bootstrap **any** new Hermes Agent instance from this blueprint — yours,
> a partner's, a client's. Same plumbing, different choices. Expected time: **~1 hour**.

## 0. Choose your profile and modules

**Deployment profile** (how/where it runs — full details in `docs/deployment.md`):

| Profile | Where it runs | Best for | Cost |
|---|---|---|---|
| `local` | Laptop/desktop, local models (Ollama) | Client / private / single machine | €0 |
| `cloud` | Hosted VPS / portal instance, always-on | Someone who needs 24/7 access (e.g. a partner) | ~$0–17/mo |
| `hybrid` | Cloud CEO (front door) + local workers | Power user who wants both | €0 + cheap cloud |

**Modules** (each is optional — pick per person):

| Module | Ask | Skip if… |
|---|---|---|
| **Memory vault** (Obsidian) | "Use a second brain vault?" | The person only chats + gets reports; no long-term notes |
| **Composio MCP** | "Use Composio as tool bridge?" | Only a couple of tools used, connected directly |
| **Chat gateway** (Discord/WhatsApp) | "Chat platform for CEO?" | The desktop app is the only front door (local profile) |
| **Custom bots** | "Extra custom bots?" | The default fleet is enough |

Rule of thumb: a non-technical person gets **fewer modules and fewer bots** (simple = reliable);
a power user gets the full stack.

## 1. Clone repos

```bash
# Blueprint repo (public — fleet templates, docs, setup)
git clone git@github.com:DakkuaDev/ai-os-personal-brain.git ~/life-os

# Memory vault (private — only if the vault module is on)
git clone git@github.com:YOUR_USER/hermes-vault.git ~/vault
```

## 2. Environment setup

```bash
cd ~/life-os
cp .env.example .env
# Edit .env: fill only the keys your profile/modules need.
# DISCORD_BOT_TOKEN...        only if chat gateway on
# COMPOSIO_API_KEY...         only if Composio on
# OBSIDIAN_VAULT_PATH=~/vault only if vault module on
```

> **Critical:** never commit `.env`. Tokens live in the machine's protected config.

## 3. Run the installer

```bash
python3 scripts/setup.py
```

It asks, in order: **deployment profile** → owner name/email → personality → model/provider
(defaults follow the profile: local = Ollama, cloud/hybrid = Nous) → **which agents** →
**custom bots** → **vault yes/no** → **Composio yes/no** → **chat platform** → nicknames/handles.

Output:
- `lifeos.config.json` — all answers (gitignored; `verify.sh` reads it)
- `generated/agents/<handle>.md` — one rendered SOUL per agent
- `generated/SETUP-NEXT-STEPS.md` — profile-aware Hermes commands

## 4. Install profiles (Hermes Agent)

```bash
# Follow generated/SETUP-NEXT-STEPS.md — it only includes the steps for YOUR choices.
# Short version:
for agent in <handles from config>; do
  hermes profile create $agent --no-skills --description "Life OS: $agent"
  hermes -p $agent config set model.default <model>
  hermes -p $agent config set model.provider <provider>
  cp generated/agents/$agent.md ~/.hermes/profiles/$agent/SOUL.md
done
```

> **One-owner rule:** only the CEO profile may hold a chat-gateway token. If other profiles
> have one, remove it — the gateway multiplexer will refuse to run otherwise.

## 5. Modules (only the ones you enabled)

- **Vault**: `echo 'OBSIDIAN_VAULT_PATH=~/vault' >> .env` (clone from step 1).
- **Composio**: `pip install composio-core && composio login`, then
  `composio add github gmail googlecalendar googledocs googledrive googlesheets linkedin notion`
  (pick what the person actually needs) and add `COMPOSIO_API_KEY` to `.env`.
  Details: `docs/integrations.md`.
- **Chat gateway**: set `platforms.<p>.enabled true` on CEO only + tokens in the CEO profile `.env`.

## 6. Verify

```bash
bash scripts/verify.sh
```

`verify.sh` auto-adapts: fleet comes from `lifeos.config.json`, vault/composio/platform checks
are skipped when those modules are off. It must end green (exit 0).

## 7. First delivery-loop test

1. `hermes -p <ceo> chat -Q -q "ping"` → CEO replies.
2. Message CEO: "ask <bot> for a status" → CEO delegates, relays the reply back.
3. Confirm the owner sees ONE message (the CEO's) and nothing raw.

## 8. Your own bots (the pattern is the point)

Adding a bot = same steps every time, whatever the domain:

1. **Justify** — recurring, distinct workload that a skill or cron can't cover
   (write the decision to the vault first; prefer skill > cron > new bot).
2. **Template** — copy `agents/<domain>-bot.md` (or `agents/custom-bot.md`) → fill domain rules.
3. **Profile** — minimal (`--no-skills`), 1–3 targeted skills, SOUL installed, one routine max.
4. **Report** — every bot reports to CEO via Bot Chat; CEO is the only deliver agent.
5. **Test + document** — ping it, delegate from CEO, add to the fleet table.

Full checklist: `templates/new-agent.md`.

## Next steps (after first boot)

- Daily heartbeat cron (09:00 UTC) → CEO Bot Chat → one-line relay.
- Weekly Life OS check (Monday) — see `docs/daily-use.md`.
- Review `CHECKPOINTS.md` — meet each domain's acceptance criteria.
- Keep `progress/history.md` appended; re-run `verify.sh` after any system change.
