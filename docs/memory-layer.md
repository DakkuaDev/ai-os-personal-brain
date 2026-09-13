# Memory Layer — the vault (and how it relates to this harness)

> The single most important decoupling decision in this system:
> **the harness repo and the memory layer are TWO separate repos.**
> Neither depends on the other to exist; they meet at a documented **contract**.

## The two repos

| | Harness (this repo) | Memory layer (the vault) |
|---|---|---|
| Repo | `DakkuaDev/ai-so-personal-brain` | `DakkuaDev/hermes-vault` |
| Visibility | **Public** (sanitized blueprint, safe to share) | **Private** (contains personal data — never make it public) |
| Role | *How the system works* (rules, templates, verification) | *What is true right now* (facts, decisions, goals, logs) |
| Changes | On rule/SOUL/template change | On any meaningful event/decision |
| Audience | Any replicator (other people, future AI) | Any agent + the owner (Obsidian) |

## The contract (what each side promises)

**The harness promises:**
- Explains the memory layer's role and location (`OBSIDIAN_VAULT_PATH` on each machine).
- Never *requires* the vault's content to be understood — a reader of this repo alone knows the
  system's shape, even with no vault present.

**The vault promises:**
- Works standalone as a second brain for ANY AI: it has its own `AGENTS.md` with read/write rules.
- Never requires the harness to be understood — an agent pointed at the vault alone can operate.

## How agents use the memory layer (the protocol)

1. **Read order:** `index.md` → `CRITICAL_FACTS.md` → relevant note (per vault `AGENTS.md`).
2. **Write rules:** plain markdown; YAML frontmatter (`type/date/tags/ai-first`) + `## For future agent`
   preamble on new notes; `[[wikilinks]]`; append `timeline:` when facts change (never overwrite);
   update `index.md` + `Logs/YYYY-MM-DD.md`; no secrets in the vault.
3. **Where it lives:** one clone per machine that runs agents, referenced by `OBSIDIAN_VAULT_PATH`
   (e.g. `/opt/data/vault` on the cloud host, `C:\Users\<user>\vault` on the local PC).
4. **Ownership:** the owner edits it in Obsidian; agents write through it as guests.

## Why they must NOT merge

- The vault is private; the harness is public/shareable. Merging would leak personal data.
- The harness changes rarely (rule changes); the vault changes constantly (life happens).
  One repo would bury the blueprint under noise — and one clone would drag personal data into
  every replication.
- The harness is *AI-agnostic* (Claude Code, Codex, Gemini… all read it); the vault is also
  AI-agnostic — but they serve different read patterns (blueprint vs living state).

## Replication checklist (for a new person)

1. Fork the **harness** (public) → replace `{{OWNER_NAME}}`/`{{OWNER_EMAIL}}` placeholders.
2. Create a **private vault** repo (or plain folder) → copy the vault's `AGENTS.md` + structure.
3. Clone both to the machine; point `OBSIDIAN_VAULT_PATH` at the vault.
4. Create the fleet from `agents/` templates; run `scripts/verify.sh`.
