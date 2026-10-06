# Principles — the "why" behind the Life OS

> Research-backed best practices that shape this architecture. Read this to understand
> **why** things are done a certain way, not just how.

## 1. One deliver agent
**Rule:** Only the CEO talks to the owner. All bot outputs and cron reports flow to CEO,
which synthesizes and delivers ONE digest.

**Why:** The CEO has full context of everything that's happening. Without this, the owner gets
raw output from every direction — noise, repetition, and no single point of accountability.
> *"If everyone is responsible, no one is."*

## 2. Memory layer = separate repo (decoupled from the blueprint)
**Rule:** The vault (what is true) and the harness (how the system works) are **two independent repos**.
Neither depends on the other.

**Why:** The vault needs to be private (personal data) and AI-agnostic. The harness needs to be
public (shareable blueprint). If they were the same repo, you couldn't share the pattern without
sharing your life. Also: lock the vault, still deploy the fleet, and vice versa.
> *"Separate what is true from how the system works."*

## 3. Minimum viable bot
**Rule:** Prefer skill > cron > new bot. A bot should own a domain that has recurring, distinct
workload. Never create a bot for a one-off task.

**Why:** Each bot adds overhead — profile config, SOUL maintenance, gateway management,
memory/cron duplication. A skill loads only when needed; a cron is a stateless script.
A bot is a lasting commitment. Start with the cheapest solution and escalate only when justified.
> *"A new bot is infrastructure. Infrastructure you don't maintain becomes decay."*

## 4. Cost discipline — free/open-source first
**Rule:** Default to free/open-source models. Paid/frontier model only when a task genuinely
needs it and the owner (or CEO) explicitly approves. Report the cost impact.

**Why:** AI model costs add up fast ($0.50–5.00/day × 30 = $15–150+/month just on generation).
Free models (DeepSeek V3/4, Qwen 3, StepFun) handle 90%+ of daily work. Deterministic work
(zero tokens) in `no_agent` scripts.
> *"Pay only for what a cheap model can't do."*

## 5. Verification-driven
**Rule:** A task is done when its CHECKPOINTS.md criteria pass — executable where possible.
Never rely on self-report.

**Why:** AI agents confidently hallucinate. A script that validates a condition (profile exists,
variable is set, file content matches schema) beats an agent's word every time. `verify.sh`
checks the system holistically; domain checkpoints check individual work.
> *"Trust but verify — executable."*

## 6. AI-agnostic
**Rule:** The vault, the docs, and the SOUL templates are plain markdown with `{{PLACEHOLDERS}}`.
No runtime-specific code. Works with Hermes, Claude Code, Codex, OpenCode, Gemini CLI, or any
agent that reads markdown.

**Why:** AI tools evolve quickly. A hermetic format (TOML/YAML/custom) ties you to one vendor.
Plain markdown outlives them all. `AGENTS.md` files provide operating instructions for any AI.
> *"What is written in a dead language can still be read. What is written in a proprietary one
> can't."*

## 7. Second-brain patterns
- **YAML frontmatter** (`type/date/tags/ai-first`) on every note — enables filtering/relevance checks.
- **`## For future agent`** preamble — any AI can decide relevance in seconds without reading the whole note.
- **Bi-temporal facts** — never delete old values; append `timeline:` entries. History is not rewritten.
- **`index.md` + `Logs/`** — navigation catalog + operation log. Always update both on changes.
- **`CRITICAL_FACTS.md`** — a ~120-token snapshot of facts true right now. One-file catchup.
> *"A note without a date, a source, and a 'who is this for' is a note without a future."*

## 8. State on disk, not in chat
**Rule:** The vault, the repo, the cron scripts — all state lives on disk. Chat is ephemeral.
Session history is searchable but the source of truth is the repository.

**Why:** Chat context is limited, irreversible, and AI-specific. Disk is durable, checkable,
and AI-agnostic. `git log` is your audit trail; `verify.sh` is your health check.
Session search supplements, not replaces.
> *"Don't tell me — show me the file."*

## 9. Naming conventions matter
- Handles: `kebab-case-bot` (searchable, taggable)
- Nicknames: human name (personality, but not functional)
- Scripts: `snake_case.sh` / `snake_case.py`
- Bot Chat prefix: `Message from 🤖 <handle> (@<handle>):`
- Profile handle = bot handle. One profile per bot.
> *"Names are how the system reasons about itself. Make them predictable."*
