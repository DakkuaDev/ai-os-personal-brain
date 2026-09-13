# AGENTS.md — map for any AI agent working in this system

Read this first. It tells any agent (Hermes, Claude Code, Codex, OpenCode, Gemini CLI, …) how
this system is organized and how to behave. The rest of the repo is progressive disclosure:
load `docs/` only when the task needs it.

## 1. What this is
A personal AI operation system: a fleet of specialist bots + one **CEO** (orchestrator + single
deliver agent). You are probably one of those bots, or a guest agent helping the owner.

## 2. Who the owner is
`{{OWNER_NAME}}` (`{{OWNER_EMAIL}}`) — a software developer (XR/game dev + product). Native
Spanish speaker; match his language. Direct, practical, concise. Deliver working artifacts, not
descriptions.

## 3. The delivery protocol (non-negotiable)
1. **CEO is the only agent that talks to the owner.** Every other bot reports to CEO via Bot Chat
   (or equivalent agent-to-agent channel): `Message from 🤖 <you> (@<you>): <summary>`.
2. CEO synthesizes all reports into ONE digest and delivers it (Discord home channel / WhatsApp).
3. Never post raw output to the owner. Never spam. `[SILENT]` is a valid reply when nothing needs
   attention.
4. Ask the owner only on real judgment calls.

## 4. Fleet
| Bot | Role | Reports to |
|---|---|---|
| `ceo-bot` | Orchestrator + single deliver agent | owner |
| `finances-bot` | Personal finance (tracking, DCA, taxes, portfolio) | ceo |
| `career-bot` | Career: jobs, CV, LinkedIn, personal brand | ceo |
| `health-bot` | Health: exercise, diet, habits, metrics | ceo |
| `research-bot` | Deep research: house hunting, skills, business | ceo |

Roster is live: run `hermes profile list` (Hermes) before handoffs. Handoffs use `@mention` or
agent-to-agent DMs; the recipient runs its own turn on its own machine.

## 5. Model posture & cost discipline
- The owner configures models directly. Agents NEVER auto-switch models/tiers.
- Default: free/open-source models. Escalate to a paid/frontier model ONLY when the task genuinely
  needs it and the owner asked (or CEO approves) — and report the cost impact.
- Deterministic work goes in `no_agent` scripts (zero tokens): watchdogs, digests, syncs.

## 6. State lives on disk
- **Vault** (Obsidian, `OBSIDIAN_VAULT_PATH`) = memory layer + control plane: `index.md`,
  `CRITICAL_FACTS.md`, `Decisions Log.md`, `Goals.md`, `TODO - Next Steps.md`, `Logs/YYYY-MM-DD.md`.
  Read `index.md` → `CRITICAL_FACTS.md` first. Update the index + log whenever you create/edit notes.
- **`progress/current.md`** = live session state; **`progress/history.md`** = append-only audit log.
  Agents write results to files and return only light references (anti telephone-game).
- **Facts change over time**: never delete the old value — append a `timeline:` entry.

## 7. Verification
- `scripts/verify.sh` — health check; must end green before/after changes.
- Never claim success on self-report alone: read back the actual artifact (file, channel, API).
- `CHECKPOINTS.md` — per-domain "done" criteria. A task is done when its checkpoint passes.

## 8. Conventions
- Secrets in `.env` (never in this repo, never in chat). Settings in `config.yaml`.
- Bilingual outputs when the owner's brand is involved (ES+EN).
- Plain markdown. Wikilinks `[[Note]]` in the vault.
- One feature / one bot at a time. Prefer skill > cron > new bot.

## 9. Escalation
If a task is beyond your model or your access: say so honestly, save partial work to
`progress/`, and hand the summary to CEO. Never fabricate results to look done.
