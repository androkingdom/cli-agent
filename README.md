# andro-cli

[![PyPI version](https://img.shields.io/pypi/v/androincli.svg)](https://pypi.org/project/androincli/)

An AI-powered CLI agent built on **Google's Gemini API** with a beautiful **Textual TUI**.  
Chat with an AI assistant directly from your terminal — with file operations, command execution, and more.

---
> **DANGER:** This tool executes shell commands and file operations based are done on local machine. Use with caution and only check the source code.


## ⚠️ Requirements

- Python 3.10+
- A valid **`GEMINI_API_KEY`** — get one free at [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

## 📦 Installation

```bash
pip install androincli
```

Or with `uv`:

```bash
uv tool install androincli
```

---

## 🚀 Usage

```bash
andro
```

## Config is stored in `~/.cli_agent/config.json`:

```json
{
  "GEMINI_API_KEY": "your_api_key_here"
}
```

### First Run

If no API key is found, you'll be prompted in the terminal:

```
⚠️  No Gemini API key found.
Get your key at: https://aistudio.google.com/app/apikey

Enter your GEMINI_API_KEY: ••••••••••••••••
✅ API key saved!

Using API key: AIza****
```

The key is saved to `~/.cli_agent/config.json` for future runs.

### Alternatively, set via environment variable:

**Linux / macOS:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

---

## 🖥️ TUI Interface

Once launched, you'll see a full-screen chat interface:

```
┌─ andro-cli ─ AI-powered CLI assistant ──────────────────────────────┐
│                                                                       │
│  🤖 Andro                                                             │
│  Welcome! How can I help you today?                                   │
│                                                                       │
│  👤 You                                                               │
│  Create a file called hello.txt                                       │
│                                                                       │
│  🤖 Andro                                                             │
│  Creating hello.txt...                                                │
│                                                                       │
├───────────────────────────────────────────────────────────────────────┤
│ Type a message... (Enter to send, Ctrl+q to quit)      [Send ↵]      │
└──────────[Ctrl+q] Quit  [Ctrl+L] Clear  [Esc] Focus Input────────────┘
```

### Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Ctrl+q` | Quit |
| `Ctrl+L` | Clear chat |
| `Escape` | Focus input |

---

## 🛠️ Features

- 🤖 **Gemini AI** — powered by `gemini-2.0-flash`
- 🖥️ **Textual TUI** — beautiful full-screen terminal UI
- 💬 **Chat bubbles** — distinct user/bot message styling
- 🔧 **Tools** — file ops, shell commands, network checks
- 🔑 **API key management** — prompt on first run, saved locally
- 🎨 **Rich formatting** — styled output with Rich

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.
