"""Main CLI entry point for andro-cli."""
import sys

from rich.console import Console
from rich.prompt import Prompt

from andro_cli.agent.config import get_api_key, save_api_key

console = Console()


def prompt_for_api_key() -> str | None:
    """Prompt the user to enter their Gemini API key via CLI.

    Returns:
        The API key string, or None if user chose to exit.
    """
    console.print()
    console.print("[bold yellow]⚠️  No Gemini API key found.[/bold yellow]")
    console.print("[dim]Get your key at: https://aistudio.google.com/app/apikey[/dim]")
    console.print()

    try:
        api_key = Prompt.ask(
            "[cyan]Enter your GEMINI_API_KEY[/cyan] (or press Ctrl+C to exit)",
            password=True,
        ).strip()
    except (KeyboardInterrupt, EOFError):
        return None

    return api_key or None


def main() -> int:
    """Main entry point.

    1. Check for API key in config/env.
    2. If missing, prompt the user via CLI.
    3. Save the key and launch the TUI.
    """
    api_key = get_api_key()

    if not api_key:
        api_key = prompt_for_api_key()

        if not api_key:
            console.print("\n[red]No API key provided. Exiting.[/red]")
            return 1

        save_api_key(api_key)
        console.print("[green]✅ API key saved![/green]")

    console.print(f"[dim]Using API key: {api_key[:4]}****[/dim]")
    console.print()

    # Launch TUI
    from andro_cli.ui.app import AgentApp
    app = AgentApp()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
