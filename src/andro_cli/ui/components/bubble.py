from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Static, Markdown


class Bubble(Widget):
    DEFAULT_CSS = """
    Bubble {
        height: auto;
        margin: 0 1 1 1;
    }

    Bubble.user {
        align: right top;
    }

    Bubble.bot {
        align: left top;
    }

    Bubble > Markdown {
        width: auto;
        max-width: 80%;
        padding: 0 1;
    }

    Bubble.user > Markdown {
        background: $primary 20%;
        border: tall $primary;
    }

    Bubble.bot > Markdown {
        background: $surface-darken-1;
        border: tall $success;
    }
    """

    def __init__(self, message: str, role: str = "bot", **kwargs) -> None:
        super().__init__(**kwargs, classes=role)
        self._message = message
        self._role = role
        self._header: Static | None = None
        self._content: Markdown | None = None

    def compose(self) -> ComposeResult:
        self._header = Static(self._prefix_text())
        self._content = Markdown(self._message)

        yield self._header
        yield self._content

    def _prefix_text(self) -> str:
        if self._role == "user":
            return "[bold cyan]👤 You[/bold cyan]"
        return "[bold green]🤖 Andro[/bold green]"

    def update_message(self, message: str) -> None:
        self._message = message
        if self._content:
            self._content.update(self._message)