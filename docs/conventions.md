# Conventions

## Language & tone
- Owner is a native Spanish speaker (Galicia) writing in English — match his language.
- Direct, practical, concise. Working artifacts over descriptions.
- End finished tasks with "✅ Done" (no TTS/audio).

## Models & cost (standing rules)
- The owner configures models directly. Agents NEVER auto-switch models or tiers.
- Default: free/open-source models. Escalate only when a task genuinely needs it — and report cost.
- Deterministic work → `no_agent` scripts (zero tokens): watchdogs, digests, syncs.
- Watchdogs stay silent when healthy (empty stdout = no delivery).

## Vault (memory layer)
- Plain markdown, `[[wikilinks]]`, YAML frontmatter on new notes (`type/date/tags/ai-first`).
- New note → also update `index.md` + append `Logs/YYYY-MM-DD.md`.
- Facts change over time → append `timeline:` entries; never delete the old value.
- Secrets never in the vault — refer by name; they live in `.env`.
- After any meaningful change: git add/commit/push.

## Delivery
- CEO is the only agent that posts to the owner. All reports flow through CEO.
- `[SILENT]` / `NO_REPLY` = valid reply when nothing needs attention.
- One digest; never repeat the same data twice.

## Fleet lifecycle
- Prefer skill > cron > new bot.
- New bot = minimal profile + 1-3 targeted skills + SOUL + 1 routine max.
- Decide in the vault (Decisions Log) before creating; archive before deleting.

## Naming
- Profiles: lowercase single words (`ceo`, `finance`, `career`, `health`, `research`).
- Scripts: `snake_case.sh` / `snake_case.py`; agentic cron prompts self-contained.
- Bot Chat prefix: `Message from 🤖 <bot> (@<bot>):`.
