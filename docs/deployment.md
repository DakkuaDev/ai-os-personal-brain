# Deployment — hosting & architecture options

> How the Life OS fleet runs, where it lives, and how to deploy it for yourself or someone else.

## Option A: Cloud VPS (current — described setup)

Hermes Agent hosted on a Nous Research VPS (the "DAKKUA S0" setup):
- **OS:** Linux (container, overlay root — `/opt/data` survives restarts)
- **Persistence:** All state on `/opt/data/` (profiles, vault, cron, sessions)
- **Network:** Outbound works; inbound = **only** the Hermes dashboard (HTTPS on port 9119)
  No public IP, no inbound port forwarding.
- **Limit:** Can't expose custom ports — a started web server is container-only.
- **Dashboard:** `HERMES_DASHBOARD_PUBLIC_URL` env var — the entry point.

### Pros
- Always-on (24/7)
- No electricity/bandwidth cost on your laptop
- 2FA/security managed by platform

### Cons
- No inbound connections (WhatsApp webhook, webhook receivers don't work)
- Subscription cost (~$17/mo for Tier 1+, free Tier 0 available)
- Cannot run long-running services beyond the agent

## Option B: Local laptop/desktop (future — migration target)

Run Hermes on your local machine with open-source models (Ollama):
- **Full inbound access** — can use WhatsApp webhooks, expose APIs via Tailscale
- **€0 inference** — local models are free
- **Backups** are yours

### Setup sketch
```bash
# Install Ollama + pull models
ollama pull qwen3:8b
# Install Hermes (local build or release)
git clone https://github.com/org/hermes
cd hermes && make install
# Same clone fleet + setup flow from docs/setup.md
```

### Connecting phone
- **Tailscale** (free VPN mesh) tunnels your local machine to your phone
- WhatsApp bot → local webhook receiver → CEO
- No cloud subscription needed

## Option C: Hybrid (best of both — recommended)

| Tier | Component | Model | Cost |
|---|---|---|---|
| **Always-on cloud** (VPS) | CEO + cron + Discord gateway + rescue | Free/cheap (default), frontier on demand | ~$0–17/mo |
| **Local** (laptop) | Fleet workers (research, finance heavy work) | Local (Ollama) | €0 |
| **Phone** (future) | WhatsApp DM → CEO → fleet | — | Carrier data |

The CEO lives on the cloud (always on). Heavy work delegates to the local machine via
peer bridge (Tailscale tunnel + API server key). The vault syncs both ways via git.

## Backup & restore

### Native full backup (Hermes)
```bash
hermes backup
# Creates /opt/data/backups/hermes-full-<date>.zip + .sha256
# Contains: config, skills, sessions, cron, memory, plugins, vault clone
```

### Restore on new instance
```bash
# Copy the .zip to the new machine
hermes import <zip>
# That's it — exact clone. Then run verify.sh.
```

### Selective restore
- Vault alone: `git clone git@github.com:YOUR_USER/hermes-vault.git`
- Brain repo alone: `git clone git@github.com:DakkuaDev/ai-os-personal-brain.git`

## Secrets

- **Never** put tokens, API keys, or credentials in any repo — they belong in `.env`
  files that are gitignored.
- On Hermes VPS: `/opt/data/.env` is the canonical env file.
- Per-profile: `~/.hermes/profiles/<name>/.env` (the profile can inherit or override).
- The vault `Decisions Log.md` once leaked a key — redacted immediately. Use `grep -rn "ck_\|sk-\|AKIA" .` before committing.
