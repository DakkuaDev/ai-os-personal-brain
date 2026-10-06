#!/usr/bin/env python3
"""agent-first-life-os — interactive installer.

Asks the owner what they want (deployment profile, agents, nicknames, handles,
model, personality, chat platform, memory vault, integrations) and renders the fleet:

  lifeos.config.json            # all answers (gitignored — personal)
  generated/agents/<handle>.md  # one rendered SOUL per selected agent
  generated/SETUP-NEXT-STEPS.md # platform-specific commands (Hermes) + generic notes

AI-agnostic by design: templates are plain markdown with {{PLACEHOLDERS}}; the
installer only renders text. Works with Hermes, Claude Code, Codex, OpenCode, etc.

Usage:  python3 scripts/setup.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"
OUT_DIR = ROOT / "generated"
OUT_AGENTS = OUT_DIR / "agents"
CONFIG_PATH = ROOT / "lifeos.config.json"

DOMAINS = ["ceo", "finances", "career", "health", "research", "studies"]
DEFAULT_HANDLES = {d: f"{d}-bot" for d in DOMAINS}
DEFAULT_NICKNAMES = {
    "ceo": "Aegis",       # the right hand — shields you from the noise
    "finances": "Midas",  # everything it touches turns to numbers
    "career": "Compass",  # points you toward the next step
    "health": "Vital",    # keeps the engine running
    "research": "Sage",   # wisdom with sources
    "studies": "Scholar", # the study secretary — UNED master
}
ROLES = {
    "ceo": "orchestrator + single deliver agent",
    "finances": "personal finance specialist",
    "career": "career & job-hunting specialist",
    "health": "health / exercise / diet specialist",
    "research": "deep-research specialist",
    "studies": "academic study assistant (UNED master)",
}

# Deployment profiles — same plumbing, different machine/always-on posture.
#   local  → laptop/desktop, open-source models (Ollama), desktop app, no gateway
#   cloud  → hosted VPS / portal instance, always-on, chat gateway (Discord/WhatsApp)
#   hybrid → cloud CEO as 24/7 front door + local workers for heavy lifting
PROFILES = ["local", "cloud", "hybrid"]
PROFILE_HINTS = {
    "local": "laptop/desktop, Ollama models, desktop app, no always-on gateway",
    "cloud": "hosted VPS / portal instance, always-on, chat gateway (Discord/WhatsApp)",
    "hybrid": "cloud CEO as 24/7 front door + local workers for heavy lifting",
}
DEFAULT_MODEL = {
    "local": "ollama/qwen3:8b",
    "cloud": "deepseek/deepseek-v4-flash",
    "hybrid": "deepseek/deepseek-v4-flash",
}
DEFAULT_PROVIDER = {"local": "ollama", "cloud": "nous", "hybrid": "nous"}
DEFAULT_PLATFORM = {"local": "none", "cloud": "discord", "hybrid": "discord"}

PERSONALITY = {
    "technical": "- Tone: terse, precise, technical. Numbers, specs and sources over prose.",
    "practical": "- Tone: direct, practical, concise. Outcomes and actions over theory.",
    "friendly": "- Tone: warm, plain language, encouraging. Explain simply, never condescend.",
}

BANNER = r"""
  ╔══════════════════════════════════════════════════════════╗
  ║   Agent-First Life OS — interactive installer            ║
  ║   Your fleet of AI agents, your modules, your deployment ║
  ╚══════════════════════════════════════════════════════════╝
"""


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"  {prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n  Setup cancelled.")
        sys.exit(1)
    return value or default


def ask_yesno(prompt: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    raw = input(f"  {prompt} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "true", "1")


def ask_choice(prompt: str, choices: list[str], default: int = 1) -> str:
    print(f"  {prompt}")
    for i, choice in enumerate(choices, 1):
        mark = " (default)" if i == default else ""
        print(f"    {i}. {choice}{mark}")
    raw = input(f"  Choose 1-{len(choices)} [{default}]: ").strip()
    try:
        return choices[int(raw) - 1]
    except (ValueError, IndexError):
        return choices[default - 1]


def multi_select(prompt: str, choices: list[str]) -> list[str]:
    print(f"  {prompt}  (comma-separated numbers, Enter = all)")
    for i, choice in enumerate(choices, 1):
        print(f"    {i}. {choice}")
    raw = input("  Choose (e.g. 1,2,5) [all]: ").strip()
    if not raw:
        return list(choices)
    try:
        return [choices[int(n) - 1] for n in raw.split(",") if 1 <= int(n) <= len(choices)]
    except ValueError:
        return list(choices)


def render(template: str, values: dict) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "custom"


def hermes_steps(cfg: dict) -> str:
    lines = [
        "# Next steps — Hermes Agent",
        "",
        f"## Profile: {cfg['profile']}  ·  modules: vault={'yes' if cfg['vault'] else 'no'},"
        f" composio={'yes' if cfg['composio'] else 'no'}, platform={cfg['platform'] or 'none'}",
        "",
        "## 1. Create the profiles (empty, minimal)",
        "```bash",
    ]
    for agent in cfg["agents"]:
        lines.append(f'hermes profile create {agent["handle"]} --no-skills \\')
        lines.append(f'  --description "{agent["nickname"]}: {agent["role"]}. Reports to CEO."')
    lines += ["```", "", "## 2. Point them at your model", "```bash"]
    for agent in cfg["agents"]:
        lines.append(f"hermes -p {agent['handle']} config set model.default {cfg['model']}")
        lines.append(f"hermes -p {agent['handle']} config set model.provider {cfg['provider']}")
    lines += ["```", "", "## 3. Install the SOULs", "```bash"]
    for agent in cfg["agents"]:
        lines.append(f'cp generated/agents/{agent["handle"]}.md ~/.hermes/profiles/{agent["handle"]}/SOUL.md')
    lines += ["```"]

    step = 4

    if cfg["vault"]:
        lines += ["", f"## {step}. Memory vault (Obsidian)", "```bash",
                  "git clone <your-vault-repo> " + (cfg["vault_path"] or "~/vault"),
                  f"echo 'OBSIDIAN_VAULT_PATH={cfg['vault_path'] or '~/vault'}' >> .env", "```"]
        step += 1

    if cfg["composio"]:
        lines += ["", f"## {step}. Composio MCP (tool bridge)", "```bash",
                  "pip install composio-core && composio login",
                  "composio add github gmail googlecalendar googledocs googledrive googlesheets linkedin notion  # pick what you need",
                  "echo 'COMPOSIO_API_KEY=<from composio dashboard>' >> .env",
                  "```", "",
                  "Workflow: `COMPOSIO_SEARCH_TOOLS` → `COMPOSIO_GET_TOOL_SCHEMAS` → `COMPOSIO_MULTI_EXECUTE_TOOL`.",
                  "See `docs/integrations.md`."]
        step += 1

    if cfg["platform"] != "none":
        lines += ["", f"## {step}. Chat platform (CEO only — never other bots)", "```bash",
                  f"hermes -p {cfg['agents'][0]['handle']} config set platforms.{cfg['platform']}.enabled true",
                  f"# add the token to ~/.hermes/profiles/{cfg['agents'][0]['handle']}/.env "
                  f"(e.g. {cfg['platform'].upper()}_BOT_TOKEN + ALLOWED_USERS + HOME_CHANNEL)",
                  "```"]
        step += 1

    lines += ["", f"## {step}. Verify", "```bash",
              "bash scripts/verify.sh",
              f"hermes -p {cfg['agents'][0]['handle']} chat -Q -q 'ping'", "```", "",
              "> Not on Hermes? The rendered SOULs are plain markdown — install them as your",
              "> runtime's agent persona files and adapt the commands.", ">",
              "> Local-only profile? Skip the chat-gateway step; the desktop app is your front door."]
    return "\n".join(lines)


def main() -> None:
    print(BANNER)
    print("  Tell me about you and your fleet. Defaults are in [brackets] — press Enter to accept.\n")

    profile = ask_choice("Deployment profile?",
                         [f"{p} — {PROFILE_HINTS[p]}" for p in PROFILES],
                         default=PROFILES.index("hybrid") + 1)
    profile = profile.split(" — ")[0].strip()

    owner_name = ask("Your name", "Daniel")
    owner_email = ask("Your email", "you@example.com")
    personality_key = ask_choice("AI personality?", ["technical", "practical", "friendly"], default=2)
    model = ask("Default model", DEFAULT_MODEL[profile])
    provider = ask("Model provider (ollama, openai, nous, openrouter...)", DEFAULT_PROVIDER[profile])

    selected = multi_select("Which agents do you want?", DOMAINS)
    custom = ask("Extra custom bots? (comma-separated domains, e.g. kids, home; empty = none)", "")
    custom_domains = [c.strip().lower() for c in custom.split(",") if c.strip()]

    use_vault = ask_yesno("Use an Obsidian vault as memory layer (second brain)?", default=True)
    vault_path = ask("Vault path (clone of your vault repo)", "~/vault") if use_vault else ""

    use_composio = ask_yesno("Use Composio MCP as tool bridge (GitHub/Gmail/Sheets/Notion/LinkedIn)?", default=True)
    platform = ask_choice("Chat platform for the CEO (the only bot that talks to you)?",
                          ["discord", "whatsapp", "telegram", "none"],
                          default=["discord", "whatsapp", "telegram", "none"].index(DEFAULT_PLATFORM[profile]) + 1)

    agents = []
    for domain in selected + custom_domains:
        nick = ask(f"Nickname for the {domain} bot", DEFAULT_NICKNAMES.get(domain, domain.title()))
        handle = ask(f"  Handle for the {domain} bot (searchable name)", DEFAULT_HANDLES.get(domain, f"{domain}-bot"))
        agents.append({"domain": domain, "nickname": nick, "handle": slugify(handle),
                       "role": ROLES.get(domain, f"{domain} specialist (edit in the rendered SOUL)")})

    cfg = {
        "profile": profile,
        "owner": {"name": owner_name, "email": owner_email},
        "personality": personality_key,
        "model": model,
        "provider": provider,
        "platform": platform,
        "vault": bool(use_vault),
        "vault_path": vault_path,
        "composio": bool(use_composio),
        "agents": agents,
    }
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    OUT_AGENTS.mkdir(parents=True, exist_ok=True)

    common = {
        "OWNER_NAME": owner_name,
        "OWNER_EMAIL": owner_email,
        "PERSONALITY": PERSONALITY[personality_key],
        "MODEL": model,
        "PLATFORM": platform,
        "VAULT_PATH": vault_path or "OBSIDIAN_VAULT_PATH (unset)",
        "JOB_PROFILE": "YOUR ROLE PROFILE — edit this line in the rendered SOUL",
    }
    for agent in agents:
        src = AGENTS_DIR / f"{agent['domain']}-bot.md"
        if not src.exists():
            src = AGENTS_DIR / "custom-bot.md"
        rendered = render(src.read_text(encoding="utf-8"),
                          {**common, "NICKNAME": agent["nickname"], "BOT_HANDLE": agent["handle"],
                           "DOMAIN": agent["domain"]})
        (OUT_AGENTS / f"{agent['handle']}.md").write_text(rendered, encoding="utf-8")
        print(f"  ✅ rendered agents/{agent['handle']}.md")

    (OUT_DIR / "SETUP-NEXT-STEPS.md").write_text(hermes_steps(cfg), encoding="utf-8")
    print(f"\n  ✅ wrote {CONFIG_PATH.name}")
    print(f"  ✅ wrote generated/SETUP-NEXT-STEPS.md")
    print("\n  Done! Follow generated/SETUP-NEXT-STEPS.md to create the fleet.")
    print("  (Fleet nicknames are display names; @handles stay functional.)")


if __name__ == "__main__":
    main()
