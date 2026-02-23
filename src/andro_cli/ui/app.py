from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widgets import Header, Footer, Input, Button

from andro_cli.ui.components import InputBar, Bubble
from andro_cli.agent.runner import AgentService

CHAT_AREA_ID = "chat-area"
MESSAGE_INPUT_ID = "message-input"
THINKING_TEXT = "⏳ Thinking..."


class AgentApp(App):
    CSS = """
    Screen {
        background: $surface;
    }

    #chat-area {
        height: 1fr;
        padding: 1;
    }

    InputBar {
        height: auto;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "clear_chat", "Clear chat"),
        ("escape", "focus_input", "Focus input"),
    ]

    def __init__(self):
        super().__init__()
        self._busy = False  # prevents concurrent requests
        self.agent_service = AgentService()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield ScrollableContainer(id=CHAT_AREA_ID)
            yield InputBar()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "andro-cli"
        self.sub_title = "AI-powered CLI assistant"
        self._add_bubble("Welcome! How can I help you today?", role="bot")
        self.query_one(f"#{MESSAGE_INPUT_ID}", Input).focus()

    def action_clear_chat(self) -> None:
        chat_area = self.query_one(f"#{CHAT_AREA_ID}", ScrollableContainer)
        chat_area.remove_children()
        self._add_bubble("Chat cleared. How can I help you?", role="bot")

    def action_focus_input(self) -> None:
        self.query_one(f"#{MESSAGE_INPUT_ID}", Input).focus()

    def on_button_pressed(self, event) -> None:
        if event.button.id == "send-btn":
            self._handle_send()

    def on_input_submitted(self, event) -> None:
        self._handle_send()

    def _handle_send(self) -> None:
        if self._busy:
            return

        input_widget = self.query_one(f"#{MESSAGE_INPUT_ID}", Input)
        send_button = self.query_one("#send-btn", Button)

        message = input_widget.value.strip()

        if not message:
            return

        self._busy = True
        input_widget.disabled = True
        send_button.disabled = True

        self._add_bubble(message, role="user")
        input_widget.value = ""

        thinking = self._add_bubble(THINKING_TEXT, role="bot")

        self.call_after_refresh(
            lambda: self.run_worker(self._call_agent(message, thinking))
        )


    async def _call_agent(self, message: str, thinking_bubble: Bubble) -> None:
        try:
            response = await self.agent_service.ask(message)
        except Exception as e:
            response = f"⚠️ Error: {e}"

        thinking_bubble.update_message(response)

        self._busy = False

        input_widget = self.query_one(f"#{MESSAGE_INPUT_ID}", Input)
        input_widget.disabled = False
        input_widget.focus()


    def _add_bubble(self, message: str, role: str = "bot") -> Bubble:
        chat_area = self.query_one(f"#{CHAT_AREA_ID}", ScrollableContainer)
        bubble = Bubble(message=message, role=role)
        chat_area.mount(bubble)
        return bubble
