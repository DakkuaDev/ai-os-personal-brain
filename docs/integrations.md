# Integrations & tool connections

> How tools are connected in the Life OS, and how to replicate it.
> **Composio MCP is the default for most apps** — fall back to direct APIs only when Composio
> doesn't support the specific action.

## Composio MCP (default tool bridge — since 2026-10-05)

- **Endpoint:** `https://connect.composio.dev/mcp`
- **Headers:** `Content-Type: application/json`, `Accept: application/json, text/event-stream`,
  `x-consumer-api-key: <COMPOSIO_API_KEY>`
- **API key:** `COMPOSIO_API_KEY` in `.env` (obtain from composio dashboard / CLI)
- **Install:** `pip install composio-core` → `composio login` → `composio add <app>...`

### Workflow
```
1. COMPOSIO_SEARCH_TOOLS    — discover the right tool + get an execution plan
2. COMPOSIO_GET_TOOL_SCHEMAS — load exact input schemas for the tools
3. COMPOSIO_MULTI_EXECUTE_TOOL — execute (up to 50 tools in parallel)
```

### Connected apps (growing list)
| App | Added | Notes |
|---|---|---|
| `github` | 2026-10-05 | Issues, repos, PRs (no noreply — uses personal account) |
| `gmail` | 2026-10-05 | Send/search email |
| `googlecalendar` | 2026-10-05 | Read/create events |
| `googledocs` | 2026-10-05 | Read/write docs |
| `googledrive` | 2026-10-05 | File management |
| `googlesheets` | 2026-10-05 | Read/write spreadsheet data (es_ES locale) |
| `linkedin` | 2026-10-05 | Profile, posts, search |
| `notion` | 2026-10-05 | Pages, databases (NOT DB schema creation — see below) |
| *(add yours)* | — | `composio add <app>` via dashboard |

> To check currently connected: `composio list --json | jq '.connectedAccounts[] | {app}'`

### Composio CLI (alternative to MCP for one-off operations)
```bash
composio search "send an email"
composio execute GITHUB_CREATE_AN_ISSUE -d '{owner: "DakkuaDev", repo: "...", title: "..."}'
```

## Discord (chat platform — CEO only)

- **Single-owner rule:** Exactly one profile owns the Discord gateway — the CEO.
- All other profiles must have their Discord gateway disabled (`platforms.discord.enabled: false`)
  and their `.env` must NOT contain `DISCORD_BOT_TOKEN`.
- **Token conflict:** If two profiles share a Discord token, the gateway multiplexer parks one
  and refuses to run. `hermes gateway` detects this. Fix by removing the token from the
  non-CEO profiles.

### Setup
```bash
hermes -p ceo-bot config set platforms.discord.enabled true
# Add to ~/.hermes/profiles/ceo-bot/.env:
#   DISCORD_BOT_TOKEN=your_bot_token
#   DISCORD_ALLOWED_USERS=your_discord_user_id
#   DISCORD_HOME_CHANNEL=channel_id
```

## Google Workspace (legacy — migrating to Composio)

Some scripts still use direct OAuth (Google Sheets, Gmail, Calendar):

```bash
# Required files
google_client_secret.json    # from Google Cloud Console (OAuth desktop app)
google_token.json            # generated on first auth; refresh_token included
```

- **Verify with:** `gws setup --check`
- **Migration:** All Google tools will move to Composio MCP as scripts are updated.
  Next candidate: `portfolio_snapshot.py` → Composio `GOOGLESHEETS_*` tools.

## Notion (special cases)

- **API key:** `NOTION_API_KEY` in `.env` (from notion.com/my-integrations)
- **Parent page:** `Hermes Agent` (used as root for Agents Matrix, trip pages, master DBs)
- **DB schema creation:** Notion API (as of 2025-09) **cannot** create database schemas
  programmatically. Workaround: build matrices as pages with markdown tables, recreated daily.
  Or use pre-created DB templates (trip planner uses 3 pre-made DBs: Calendario/Todo's/Itinerario).
- **Trip planner:** `scripts/hermes_build_trip.py` creates a Notion trip page + links to existing DBs.

## GitHub (identity conventions)

- **Public repos** (bot-horizon, hermes-plugins): noreply email
  `DakkuaDev@users.noreply.github.com` — no personal data.
- **Private repos** (hermes-vault): personal email.
- **Website** (`dakkuadev.github.io`): NEVER commit to `master`; use `hermes-ai` branch.
  Merges to master require explicit owner OK.
- **Forks/clones:** Check `git remote -v` before pushing. Do not push public changes under
  the personal account if the repo has personal data.

## Environment variables (see `.env.example` for full list)

| Variable | Where | Secret? |
|---|---|---|
| `COMPOSIO_API_KEY` | `.env` | ✅ |
| `DISCORD_BOT_TOKEN` | `.env` (CEO profile only) | ✅ |
| `DISCORD_ALLOWED_USERS` | `.env` | ⚠️ (user ID, non-secret but private) |
| `DISCORD_HOME_CHANNEL` | `.env` | ⚠️ (channel ID) |
| `NOTION_API_KEY` | `.env` | ✅ |
| `GOOGLE_CLIENT_SECRET` + `GOOGLE_TOKEN` | files on disk | ✅ |
| `OBSIDIAN_VAULT_PATH` | `.env` | ❌ (file path) |
| `HERMES_PEER_CLOUD_KEY` | `.env` | ✅ (local↔cloud bridge) |
