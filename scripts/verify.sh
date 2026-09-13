#!/usr/bin/env bash
# verify.sh — system health check for the Agent-First Life OS.
# Must end green. Exit 1 on any failure.
set -u
FAIL=0

say()  { printf '  %s\n' "$1"; }
ok()   { say "✅ $1"; }
bad()  { say "❌ $1"; FAIL=1; }

say "Agent-First Life OS — verify"

# 1. Fleet profiles exist
for bot in ceo-bot finances-bot career-bot health-bot research-bot; do
  if hermes profile list 2>/dev/null | grep -q " $bot "; then ok "profile $bot exists"; else bad "profile $bot missing"; fi
done

# 2. Exactly one Discord/chat owner (ceo)
CEODISC=$(hermes -p ceo-bot config get platforms.discord.enabled 2>/dev/null || echo false)
if [ "$CEODISC" = "True" ] || [ "$CEODISC" = "true" ]; then ok "ceo owns chat platform"; else bad "ceo does not own chat platform"; fi

# 3. Report crons target ceo's bot chat
BAD_DELIVER=$(grep -l '"deliver": "discord' ~/.hermes/cron/jobs.json 2>/dev/null)
if [ -z "$BAD_DELIVER" ]; then ok "no cron delivers raw to discord"; else bad "cron(s) still deliver raw to discord: $BAD_DELIVER"; fi

# 4. Vault clean
if [ -d "$OBSIDIAN_VAULT_PATH/.git" ]; then
  if [ -z "$(git -C "$OBSIDIAN_VAULT_PATH" status --porcelain 2>/dev/null)" ]; then ok "vault clean"; else bad "vault has uncommitted changes"; fi
else
  bad "OBSIDIAN_VAULT_PATH not a git repo"
fi

# 5. No secrets committed
if grep -rIl -E "(DISCORD_BOT_TOKEN|API_KEY|SECRET)" --exclude-dir=.git . 2>/dev/null | grep -qv ".env"; then
  bad "possible secret committed (see files above)"; else ok "no secrets in repo"; fi

# 6. CEO responds
if timeout 60 hermes -p ceo-bot chat -Q -q "ping" 2>/dev/null | grep -qiE "pong|online|✅"; then
  ok "ceo responds"; else bad "ceo did not respond to ping"; fi

echo
if [ "$FAIL" = "0" ]; then echo "✅ All checks passed."; else echo "❌ $FAIL check(s) failed."; exit 1; fi
