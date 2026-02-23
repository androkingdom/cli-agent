"""Configuration management for py-cli-agent"""
import json
import os
from pathlib import Path
from typing import Any

# Default config directory
DEFAULT_CONFIG_DIR = Path.home() / ".cli_agent"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"
DEFAULT_AGENT_FILE = DEFAULT_CONFIG_DIR / "AGENT.md"
DEFAULT_MCP_DIR = DEFAULT_CONFIG_DIR / "mcp"


def get_config_dir() -> Path:
    """Get the config directory path."""
    return DEFAULT_CONFIG_DIR


def ensure_config_dir() -> Path:
    """Ensure the config directory exists."""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_CONFIG_DIR


def get_session_file() -> Path:
    return get_config_dir() / "session.db"


def load_config() -> dict[str, Any]:
    """Load configuration from config.json."""
    if not DEFAULT_CONFIG_FILE.exists():
        return {}
    
    try:
        with open(DEFAULT_CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load config: {e}")
        return {}



def save_config(config: dict[str, Any]) -> None:
    """Save configuration to config.json."""
    ensure_config_dir()
    with open(DEFAULT_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def save_default_instructions() -> None:
    """Save default agent instructions to AGENT.md if it doesn't exist."""
    if not DEFAULT_AGENT_FILE.exists():
        try:
            DEFAULT_AGENT_FILE.write_text(get_default_instructions(), encoding="utf-8")
        except Exception as e:
            print(f"[WARN] Failed to save default instructions: {e}")

def load_agent_instructions() -> str:
    """Load custom agent instructions from AGENT.md."""
    if DEFAULT_AGENT_FILE.exists():
        try:
            return DEFAULT_AGENT_FILE.read_text(encoding="utf-8")
        except Exception:
            pass
    
    # Return default instructions if file doesn't exist and saving default instructions
    
    save_default_instructions()
    return get_default_instructions()


def get_default_instructions() -> str:
    """Get default agent instructions."""
    return """# System Prompt - Tech Support Agent

## Role
You are a patient, friendly tech support assistant helping non-technical users with their computer problems. You explain things in simple terms without jargon.

## Chain of Thought (COT) Process
Before taking any action, follow these steps:
1. UNDERSTAND - What is the user's problem?
2. DIAGNOSE - Ask questions to identify the root cause
3. PLAN - Explain what you'll do before doing it
4. ACT - Execute the fix step by step
5. VERIFY - Confirm the problem is resolved
6. EXPLAIN - Tell the user what you did in simple terms

## Guidelines
- Always ask before making changes to the user's computer
- Warn about potential risks before dangerous operations
- Never assume - verify with the user
- Provide simple, jargon-free explanations
- Be patient with users who aren't tech-savvy
- Think step by step internally.
- Do NOT reveal your reasoning.
- Only provide the final answer to the user.
- You must always respond in English. Do not switch languages.

## Response Format
[Final answer to user's question]
"""


def get_api_key() -> str | None:
    """Get the Gemini API key from config or environment."""
    config = load_config()
    
    # Check config first
    if api_key := config.get("GEMINI_API_KEY"):
        return api_key
    
    # Check environment variable
    if api_key := os.getenv("GEMINI_API_KEY"):
        return api_key
    
    return None


def save_api_key(api_key: str) -> None:
    """Save the API key to config."""
    config = load_config()
    config["GEMINI_API_KEY"] = api_key
    save_config(config)


def get_mcp_config() -> dict[str, Any]:
    """Load MCP configuration from mcp/ folder."""
    if not DEFAULT_MCP_DIR.exists():
        return {}
    
    mcp_config = {}
    for file in DEFAULT_MCP_DIR.glob("*.json"):
        try:
            with open(file, "r") as f:
                mcp_config[file.stem] = json.load(f)
        except Exception:
            pass
    
    return mcp_config
