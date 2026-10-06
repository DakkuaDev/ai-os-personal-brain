#!/usr/bin/env bash
# verify.sh — system health check for the Agent-First Life OS.
# Must end green. Exit 1 on any failure.
#
# Config-driven: reads lifeos.config.json (written by scripts/setup.py) when present.
#   - fleet    → the exact handles you created (default: the standard 6)
#   - vault    → only checked when OBSIDIAN_VAULT_PATH is set
#   - composio → only checked when COMPOSIO_API_KEY is set
#   - platform → skipped when config says "none" or no .env token is found
set -u
FAIL=0

say()  { printf '  %s\n' "$1"; }
ok()   { say "✅ $1"; }
bad()  { say "❌ $1"; FAIL=1; }

say "Agent-First Life OS — verify"

# Fleet from lifeos.config.json if present, else the default roster.
AGENTS="ceo-bot finances-bot career-bot health-bot research-bot studies-bot"
if [ -f "lifeos.config.json" ] && command -v python3 >/dev/null 2>&1; then
  CFG_AGENTS=$(python3 - <<'PY' 2>/dev/null
import json
try:
    d = json.load(open("lifeos.config.json"))
    print(" ".join(a["handle"] for a in d.get("agents", [])))
except Exception:
    pass
PY
)
  if [ -n "$CFG_AGENTS" ]; then AGENTS="$CFG_AGENTS"; fi
fi
CEO=$(printf '%s' "$AGENTS" | awk '{print $1}')

# 1. Fleet profiles exist
for bot in $AGENTS; do
  if hermes profile list 2>/dev/null | grep -q " $bot "; then ok "profile $bot exists"; else bad "profile $bot missing"; fi
done

# 2. Exactly one chat-platform owner (the CEO) — skipped when no platform configured
PLATFORM="discord"
if [ -f "lifeos.config.json" ]; then
  PLATFORM=$(python3 - <<'PY' 2>/dev/null
import json
try:
    print(json.load(open("lifeos.config.json")).get("platform") or "none")
except Exception:
    print("discord")
PY
)
fi
if [ "$PLATFORM" = "none" ]; then
  ok "no chat platform configured (skip owner check)"
else
  CEODISC=$(hermes -p "$CEO" config get "platforms.$PLATFORM.enabled" 2>/dev/null || echo false)
  if [ "$CEODISC" = "True" ] || [ "$CEODISC" = "true" ]; then ok "$CEO owns chat platform ($PLATFORM)"; else bad "$CEO does not own chat platform ($PLATFORM)"; fi
fi

# 3. Report crons target CEO's bot chat (only when a crons file exists)
CRON_JSON="${HERMES_HOME:-$HOME/.hermes}/cron/jobs.json"
if [ -f "$CRON_JSON" ]; then
  BAD_DELIVER=$(grep -l '"deliver": "discord' "$CRON_JSON" 2>/dev/null)
  if [ -z "$BAD_DELIVER" ]; then ok "no cron delivers raw to a chat platform"; else bad "cron(s) still deliver raw: $BAD_DELIVER"; fi
else
  ok "no cron jobs file (skip delivery check)"
fi

# 4. Vault clean — only when a vault is configured
if [ -n "${OBSIDIAN_VAULT_PATH:-}" ] && [ -d "$OBSIDIAN_VAULT_PATH/.git" ]; then
  if [ -z "$(git -C "$OBSIDIAN_VAULT_PATH" status --porcelain 2>/dev/null)" ]; then ok "vault clean"; else bad "vault has uncommitted changes"; fi
elif [ -n "${OBSIDIAN_VAULT_PATH:-}" ]; then
  bad "OBSIDIAN_VAULT_PATH set but not a git repo"
else
  ok "no vault configured (skip vault check)"
fi

# 4b. Composio bridge — only when the key is configured
if [ -n "${COMPOSIO_API_KEY:-}" ]; then
  if command -v composio >/dev/null 2>&1; then
    if timeout 20 composio list >/dev/null 2>&1; then ok "composio reachable"; else bad "composio CLI not logged in"; fi
  else
    ok "COMPOSIO_API_KEY set (composio CLI not installed — fine for agents-only use)"
  fi
else
  ok "no Composio configured (skip bridge check)"
fi

# 5. No secrets committed — flag real secret VALUES (env-var NAMES in docs are fine)
SECRET_ASSIGN='[A-Z_]*(TOKEN|KEY|SECRET|PASSWORD)[A-Z_]*[[:space:]]*=[[:space:]]*[^#[:space:]][^[:space:]]{7,}'
SECRET_SHAPE='(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{30,}|ck_[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[A-Za-z0-9-]{10,})'
if grep -rInE "$SECRET_ASSIGN|$SECRET_SHAPE" --exclude-dir=.git --exclude-dir=generated \
     --exclude="verify.sh" --exclude=".env.example" . 2>/dev/null \
   | grep -vE ':.*(your_|example|REPLACE|xxx|dummy|<|>)' | grep -qv '^\.env:'; then
  bad "possible secret VALUE committed (see files above)"; else ok "no secrets in repo"; fi

# 6. CEO responds
if timeout 60 hermes -p "$CEO" chat -Q -q "ping" 2>/dev/null | grep -qiE "pong|online|✅|session_id"; then
  ok "$CEO responds"; else bad "$CEO did not respond to ping"; fi

echo
if [ "$FAIL" = "0" ]; then echo "✅ All checks passed."; else echo "❌ $FAIL check(s) failed."; exit 1; fi
