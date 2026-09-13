# New agent bootstrap checklist

Use this when CEO (or the owner) decides a new bot is justified. **Prefer skill > cron > new bot.**

## 1. Justify (write to Decisions Log first)
- [ ] What recurring, distinct workload does this bot own?
- [ ] Why can't a skill or cron cover it?
- [ ] What's the minimum viable scope? (One domain. No feature creep.)

## 2. Create (Hermes example)
```bash
hermes profile create <name> --no-skills \
  --description "<one-liner role + 'Reports to ceo.'>"
cp .env ~/.hermes/profiles/<name>/.env      # shared tokens
hermes -p <name> config set model.default <model>
hermes -p <name> config set model.provider <provider>
hermes -p <name> config set platforms.discord.enabled false   # only ceo owns chat
```

## 3. SOUL
- [ ] Copy `agents/_template.md` → `agents/<name>.md` (this repo), fill role/domain rules.
- [ ] Install as `<profile>/SOUL.md`.
- [ ] Include: identity, model posture, domain rules (load skills first!), reporting-to-CEO protocol,
      safety, messaging protocol, roadmap context.

## 4. Skills (1-3, targeted)
- [ ] Copy only the skills the bot needs (from `skills/` or the shared catalog).
- [ ] No bundled skill dump. Empty profile + curated skills.

## 5. Routine (max 1 to start)
- [ ] One cron that proves the bot's value weekly (e.g. weekly review → CEO).
- [ ] `no_agent` script if deterministic; agentic only if judgment needed.

## 6. Test
- [ ] Ping the bot (`hermes -p <name> chat -Q -q "ping"`).
- [ ] Delegate a real task from CEO; verify it reports back to CEO (not the owner).

## 7. Document
- [ ] Add to `profiles/<name>.md` manifest + vault `Personal Automation` + fleet table in AGENTS.md.
