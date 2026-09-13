# Verification

How to prove the system works — executable where possible, observable otherwise. Cross-ref
`CHECKPOINTS.md` for the full acceptance list.

## 1. Health check (`scripts/verify.sh`)
```
./scripts/verify.sh
```
Checks (extend as the system grows):
- All fleet profiles exist (`ceo finance career health research`).
- Exactly one profile owns the chat platform (no token conflict).
- All report crons target `bot-chat:ceo` (grep `cron/jobs.json` for `deliver`).
- Vault is a git repo with no uncommitted changes (after a session).
- `.env` present and no secrets committed.
- CEO responds to a ping (`hermes -p ceo chat -Q -q "ping"` returns quickly).

## 2. Delivery loop test
1. Fire a harmless no_agent cron: `hermes cron run tax-calendar` (or equivalent).
2. Confirm the stdout lands in CEO's Bot Chat (read the CEO session).
3. Confirm CEO posts a synthesized digest to the home channel.
4. Confirm the owner sees exactly ONE message.

## 3. Delegation test
1. Message CEO: "ask finance for the current portfolio snapshot".
2. CEO messages `finance` (Bot Chat), waits, relays the reply.
3. Verify the reply names the bot and contains real numbers or an honest blocker.

## 4. Escalation test (when a cloud rescue exists)
1. Ask CEO a research question that needs a frontier model.
2. Verify CEO requests cloud rescue via peer DM and relays the cited answer back.

## 5. Replication test (the real proof)
On a clean machine: clone repo → fill `.env.example` → `./scripts/verify.sh` → create fleet →
talk to CEO. Target: under 1 hour to a working system. Document deviations here.
