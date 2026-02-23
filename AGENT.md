# andro-cli Development Guide

## Project Overview

**andro-cli** is a Python TUI agent powered by Google's Gemini API. It provides an interactive terminal UI (using Textual) where users can chat with AI and execute file/system operations.

## Tech Stack

- **Language**: Python 3.10+
- **Package Manager**: uv
- **Build System**: setuptools (via `src/pyproject.toml`)
- **Key Dependencies**:
  - `openai` — Gemini API client (OpenAI-compatible)
  - `textual` — TUI framework (main UI)
  - `rich` — Terminal formatting & logs
  - `python-dotenv` — Environment variable management
  - `agents` — Agent framework

## Project Structure

```
cli-agent/                  # Git root
├── .gitignore
├── AGENT.md                # This file - developer guide
├── LICENSE
├── README.md               # User documentation
├── memory-bank/            # Cline memory bank
│   ├── activeContext.md
│   ├── productContext.md
│   ├── progress.md
│   ├── projectbrief.md
│   ├── systemPatterns.md
│   └── techContext.md
└── src/                    # Package root (uv project)
    ├── .python-version
    ├── .venv/              # Virtual environment
    ├── pyproject.toml      # Package config & dependencies
    ├── uv.lock             # Locked dependencies
    ├── README.md           # Dev docs (this dir)
    ├── main.py             # Entry point
    ├── agent/              # Agent logic
    │   ├── __init__.py
    │   ├── config.py       # API key + config management
    │   ├── setup.py        # Gemini client setup
    │   ├── models/         # Data models
    │   └── tools/          # Agent tools
    │       ├── files.py
    │       ├── network.py
    │       └── system.py
    └── ui/                 # TUI
        ├── __init__.py
        ├── app.py          # AgentApp (main Textual app)
        └── components/     # Reusable UI widgets
            ├── __init__.py
            ├── bubble.py   # Chat message bubble
            └── input_bar.py # Input field + send button
```

## Startup Flow

```
andro-cli
  ↓
main.py:main()
  ↓
get_api_key()  ←  ~/.cli_agent/config.json or GEMINI_API_KEY env
  ↓ (if missing)
Prompt: "Enter your GEMINI_API_KEY:"
  ↓ (key entered)
save_api_key()  →  ~/.cli_agent/config.json
  ↓
AgentApp.run()  →  Textual TUI launches
```

## Config Directory

| Path | Purpose |
|------|---------|
| `~/.cli_agent/config.json` | API key + settings |
| `~/.cli_agent/AGENT.md` | Custom agent instructions |
| `~/.cli_agent/mcp/` | MCP server configs |

## Development Commands

### Setup
```bash
cd src
uv venv
source .venv/Scripts/activate  # Git Bash / macOS/Linux
uv sync
```

### Run
```bash
uv --directory src run python main.py
```

### Add a dependency
```bash
uv --directory src add <package>
```

### Build & Publish
```bash
uv --directory src build
uv --directory src publish
```

## TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Ctrl+X` | Quit |
| `Ctrl+L` | Clear chat |
| `Escape` | Focus input |

## Available Tools

| Tool | File | Description |
|------|------|-------------|
| `read_file` | tools/files.py | Read file contents |
| `write_file` | tools/files.py | Write to file |
| `delete_file` | tools/files.py | Delete file |
| `list_directory` | tools/files.py | List dir contents |
| `create_directory` | tools/files.py | Create directory |
| `delete_directory` | tools/files.py | Delete directory |
| `get_current_directory` | tools/files.py | Get cwd |
| `ping` | tools/network.py | Ping a host |
| `check_dns` | tools/network.py | DNS lookup |
| `get_local_ip` | tools/network.py | Get local IP |
| `check_port` | tools/network.py | Check if port open |
| `traceroute` | tools/network.py | Network traceroute |
| `get_system_info` | tools/system.py | OS/CPU info |
| `check_disk` | tools/system.py | Disk usage |
| `check_processes` | tools/system.py | Running processes |
| `check_network` | tools/system.py | Network stats |
| `run_command` | tools/system.py | Run shell command |
