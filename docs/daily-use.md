# Daily use — how the system works day to day

> For the owner, the bot fleet, or anyone inheriting this system.
> This is the "what happens when" guide.

## Daily rhythm

### 05:00–10:00 UTC (06:00–11:00 Madrid) — Morning automation window

| Time | Job | What it does | Delivery path |
|---|---|---|---|
| 05:00 UTC | weather-brief | Fetch A Coruña weather (Open-Meteo, free) | → bot-chat:ceo-bot |
| 08:00 UTC | job-scraper | Scrape XR/Unity/game dev jobs (RemoteRocketship, LinkedIn, etc.) | → bot-chat:ceo-bot |
| 09:00 UTC | heartbeat | CEO checks fleet + cron health → one-line digest | → Discord home |
| 10:00 UTC | job-cover-letters | Draft cover letters for high-match jobs → CEO for approval | → bot-chat:ceo-bot |

The CEO receives all these in its Bot Chat and posts a **single synthesized digest** to the
Discord home channel (or whatever chat platform is wired). You see ONE message per time window.

### Weekend / monthly cron window
Some jobs run on specific days:
- **1st of month:** Money briefing + Coast-FIRE history snapshot
- **2nd of month:** Expense digest (reconciles previous month)
- **5th of month:** Portfolio audit + personal advisor note
- **Monday:** Weekly Life OS check (1-line each: finance / career / health / research / automations)
- **Sunday:** Health check nudge (Vital asks for the week's stats)

## How to talk to CEO

- **In Discord:** `@ceo-bot <your message>`
- **In your Hermes desktop chat** (default profile): just type normally — the default profile IS
  the CEO when the desktop session runs as CEO. (Default is the worker backend; CEO owns the delivery.)
  Actually: you chat with **default** profile (Hermes agent); forward to CEO by saying
  "ask CEO to..." or "ceo-bot: ...".

**What you can ask:**
- "What's the latest on <topic>?" — CEO delegates to the relevant bot
- "Ask finance for the portfolio snapshot" — CEO DMs finances-bot, relays reply
- "Add a task: buy climbing chalk" — CEO processes or delegates
- "Run the weekly Life OS check" — CEO triggers fleet check
- "Set a cron for <X>" — CEO creates the cron
- `[SILENT]` reply from CEO = nothing needs attention

**When NOT to ask:**
- To reset/reconfigure the system → use config or `hermes config set`
- To fix a broken Discord gateway → run `hermes gateway` → follow instructions
- Code-level debugging → use the default profile directly (it has full tool access)

## Weekly maintenance

### Monday — Life OS check (CEO)
- CEO runs `scripts/hermes_vault_maintenance.py` → checks index, broken wiki-links,
  cron-drift, stale info, log-consistency
- CEO pings each fleet bot for a one-line status
- CEO posts a consolidated Monday digest (finance balance / career status / health trend /
  research progress / system health)

### As needed — maintenance passes
- **Vault weekly pass** (detects duplicate/stale info — run via `hermes cron run vault-maintenance`)
- **Credits watchdog** (checks free models haven't silently turned paid — runs weekly)
- **`scripts/verify.sh`** — should pass clean before/after any system change

## On-call / rescue

If a task needs a frontier model or a tool the default can't reach:
1. Tell CEO: "This needs a stronger model for X reason"
2. CEO will either: (a) switch to a paid model for that task, or (b) escalate to the cloud rescue
   instance via peer bridge (if wired)
3. The results come back through the same delivery loop

> **Cost rule:** Default = free/open-source models. Paid/frontier is opt-in per task.
> CEO reports when it escalates.
