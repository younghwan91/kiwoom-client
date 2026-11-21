# Using it from AI coding tools

What this repository gives Claude Code, Cursor, Copilot, Codex and other AI coding tools so that they use kiwoom-client
**correctly**. Everything is generated from the code and checked by tests, so method names and the endpoint list never
drift from the real code.

| File | Read by | Contents |
|---|---|---|
| [`llms.txt`](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms.txt) | LLMs reading the web ([llmstxt.org](https://llmstxt.org) format) | one-paragraph summary, rules for writing code, links |
| [`llms-full.txt`](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms-full.txt) | pasting into a context window | every public signature and docstring + the full endpoint list |
| [`AGENTS.md`](https://github.com/younghwan91/kiwoom-client/blob/main/AGENTS.md) | agents that open this repository (Codex, …) | usage rules + rules for working on this repository |
| [`skills/kiwoom-client/`](https://github.com/younghwan91/kiwoom-client/tree/main/skills/kiwoom-client) | Claude Code · Agent Skills | rules, workflow, examples + endpoint list |
| [`.cursor/rules/kiwoom-client.mdc`](https://github.com/younghwan91/kiwoom-client/blob/main/.cursor/rules/kiwoom-client.mdc) | Cursor | the same rules (attached when a Python file is open) |
| [`.github/copilot-instructions.md`](https://github.com/younghwan91/kiwoom-client/blob/main/.github/copilot-instructions.md) | GitHub Copilot | the same rules |
| MCP server (`kiwoom-client-mcp`) | MCP clients | call the endpoints as tools — [README, MCP server](https://github.com/younghwan91/kiwoom-client/blob/main/README_EN.md) |

Every rule set starts the same way: **`is_mock` defaults to `False`, the live server, and `api.order.*` /
`api.credit_order.*` place real orders.** Run AI-written code in paper trading (`is_mock=True`) first.

## Claude Code skill

### Install as a plugin

This repository doubles as a plugin marketplace. Inside Claude Code:

```text
/plugin marketplace add younghwan91/kiwoom-client
/plugin install kiwoom-client@kiwoom-client
```

Once installed, the skill loads by itself when code uses `kiwoom_client` or the conversation is about the Kiwoom REST API;
invoke it directly with `/kiwoom-client:kiwoom-client`.

### Copy into your project

Put the skill folder (two files) in your project's `.claude/skills/`, or in `~/.claude/skills/` for every project.

```bash
mkdir -p .claude/skills/kiwoom-client
for f in SKILL.md endpoints.md; do
  curl -fsSL -o ".claude/skills/kiwoom-client/$f" \
    "https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/skills/kiwoom-client/$f"
done
```

A copied skill is invoked as `/kiwoom-client`. After upgrading the library, run the same command again to refresh the
endpoint list.

## Cursor · GitHub Copilot

They apply as soon as you open this repository. For your own project, download them to the same paths (append to an
existing `copilot-instructions.md`):

```bash
mkdir -p .cursor/rules .github
curl -fsSL -o .cursor/rules/kiwoom-client.mdc \
  https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/.cursor/rules/kiwoom-client.mdc
curl -fsSL https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/.github/copilot-instructions.md \
  >> .github/copilot-instructions.md
```

## Other tools

- **Tools that read `AGENTS.md` (Codex, …)**: opening this repository is enough. To use the rules in your own project,
  copy the "Writing code that uses kiwoom-client" section of
  [`AGENTS.md`](https://github.com/younghwan91/kiwoom-client/blob/main/AGENTS.md) into your own `AGENTS.md`.
- **Tools that read URLs**: point them at `llms.txt`.
