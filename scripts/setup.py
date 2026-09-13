#!/usr/bin/env python3
"""agent-first-life-os — interactive installer.

Asks the owner what they want (agents, nicknames, handles, model, personality,
chat platform, vault path) and renders the fleet:

  lifeos.config.json            # all answers (gitignored — personal)
  generated/agents/<handle>.md  # one rendered SOUL per selected agent
  generated/SETUP-NEXT-STEPS.md # platform-specific commands (Hermes) + generic notes

AI-agnostic by design: templates are plain markdown with {{PLACEHOLDERS}}; the
installer only renders text. Works with Hermes, Claude Code, Codex, OpenCode, etc.

Usage:  python3 scripts/setup.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"
OUT_DIR = ROOT / "generated"
OUT_AGENTS = OUT_DIR / "agents"
CONFIG_PATH = ROOT / "lifeos.config.json"

DOMAINS = ["ceo", "finances", "career", "health", "research"]
DEFAULT_HANDLES = {d: f"{d}-bot" for d in DOMAINS}
DEFAULT_NICKNAMES = {
    "ceo": "Aegis",       # the right hand — shields you from the noise
    "finances": "Midas",  # everything it touches turns to numbers
    "career": "Compass",  # points you toward the next step
    "health": "Vital",    # keeps the engine running
    "research": "Sage",   # wisdom with sources
}

PERSONALITY = {
    "technical": "- Tone: terse, precise, technical. Numbers, specs and sources over prose.",
    "practical": "- Tone: direct, practical, concise. Outcomes and actions over theory.",
    "friendly": "- Tone: warm, plain language, encouraging. Explain simply, never condescend.",
}

BANNER = r"""
  ╔══════════════════════════════════════════════════════════╗
  ║   Agent-First Life OS — interactive installer            ║
  ║   Your fleet of AI agents, one CEO, your rules.          ║
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


def ask_choice(prompt: str, choices: list[str], default: int = 1) -> str:
    print(f"  {prompt}")
    for i, choice in enumerate(choices, 1):
        mark = " (default)" if i == default else ""
        print(f"    {i}. {choice}{mark}")
    raw = input("  Choose 1-{} [{}]: ".format(len(choices), default)).strip()
    try:
        return choices[int(raw) - 1]
    except (ValueError, IndexError):
        return choices[default - 1]


def multi_select(prompt: str, choices: list[str], default_all: bool = True) -> list[str]:
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


def hermes_steps(cfg: dict) -> str:
    lines = [
        "# Next steps — Hermes Agent",
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
    lines += ["```", "", "## 4. Chat platform (only the CEO uses it)", "```bash"]
    if cfg["platform"] != "none":
        lines += [
            f"hermes -p {cfg['agents'][0]['handle']} config set platforms.{cfg['platform']}.enabled true",
            f"# add the token to ~/.hermes/profiles/{cfg['agents'][0]['handle']}/.env "
            f"(e.g. {cfg['platform'].upper()}_BOT_TOKEN)",
        ]
    lines += [
        "```",
        "",
        "## 5. Verify",
        "```bash",
        "bash scripts/verify.sh",
        f"hermes -p {cfg['agents'][0]['handle']} chat -Q -q 'ping'",
        "```",
        "",
        "> Not on Hermes? The rendered SOULs are plain markdown — install them as your",
        "> runtime's agent persona files and adapt the commands.",
    ]
    return "\n".join(lines)


def main() -> None:
    print(BANNER)
    print("  Tell me about you and your fleet. Defaults are in [brackets] — press Enter to accept.\n")

    owner_name = ask("Your name", "Daniel")
    owner_email = ask("Your email", "you@example.com")
    personality_key = ask_choice("AI personality?", ["technical", "practical", "friendly"], default=2)
    model = ask("Default model", "ollama/qwen3:8b")
    provider = ask("Model provider (ollama, openai, nous, openrouter...)", "ollama")
    selected = multi_select("Which agents do you want?", DOMAINS)
    platform = ask_choice("Chat platform for the CEO (the only bot that talks to you)?",
                          ["discord", "whatsapp", "telegram", "none"], default=1)
    vault_path = ask("Memory layer / vault path (optional, leave empty to skip)", "")

    agents = []
    for domain in selected:
        nick = ask(f"Nickname for the {domain} bot", DEFAULT_NICKNAMES[domain])
        handle = ask(f"  Handle for the {domain} bot (searchable name)", DEFAULT_HANDLES[domain])
        agents.append({"domain": domain, "nickname": nick, "handle": handle,
                       "role": {"ceo": "orchestrator + single deliver agent",
                                "finances": "personal finance specialist",
                                "career": "career & job-hunting specialist",
                                "health": "health / exercise / diet specialist",
                                "research": "deep-research specialist"}[domain]})

    cfg = {
        "owner": {"name": owner_name, "email": owner_email},
        "personality": personality_key,
        "model": model,
        "provider": provider,
        "platform": platform,
        "vault_path": vault_path,
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
        rendered = render(src.read_text(encoding="utf-8"),
                          {**common, "NICKNAME": agent["nickname"], "BOT_HANDLE": agent["handle"]})
        (OUT_AGENTS / f"{agent['handle']}.md").write_text(rendered, encoding="utf-8")
        print(f"  ✅ rendered agents/{agent['handle']}.md")

    (OUT_DIR / "SETUP-NEXT-STEPS.md").write_text(hermes_steps(cfg), encoding="utf-8")
    print(f"\n  ✅ wrote {CONFIG_PATH.name}")
    print(f"  ✅ wrote generated/SETUP-NEXT-STEPS.md")
    print("\n  Done! Follow generated/SETUP-NEXT-STEPS.md to create the fleet.")
    print("  (Fleet nicknames are display names; @handles stay functional.)")


if __name__ == "__main__":
    main()
