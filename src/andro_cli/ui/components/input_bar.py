"""InputBar component for andro-cli TUI."""
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Button
from textual.widget import Widget


class InputBar(Widget):
    """A composed input bar with text field and send button."""

    DEFAULT_CSS = """
    InputBar {
        height: auto;
        dock: bottom;
        border-top: solid $primary;
        padding: 0 1;
        layout: horizontal;
    }

    InputBar > #message-input {
        width: 1fr;
    }

    InputBar > #send-btn {
        width: auto;
        min-width: 10;
        margin-left: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Create input bar children."""
        yield Input(placeholder="Type a message... (Enter to send, Ctrl+X to quit)", id="message-input")
        yield Button("Send [bold]↵[/bold]", id="send-btn", variant="primary")
