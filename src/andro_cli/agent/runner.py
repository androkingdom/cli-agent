import asyncio
import os

from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from agents.extensions.memory import AdvancedSQLiteSession
from andro_cli.agent.config import get_api_key, load_agent_instructions, ensure_config_dir, get_session_file

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = get_api_key() or ""
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or "gemini-2.5-flash-lite"

if not API_KEY:
    raise ValueError(
        "\n\n"
        "  ❌  No Gemini API key found!\n\n"
        "  How to fix:\n"
        "    1. Get a free key at: https://aistudio.google.com/app/apikey\n"
        "    2. Set it as an environment variable:\n"
        "         export GEMINI_API_KEY='your_key_here'   # Linux/macOS\n"
        "         $env:GEMINI_API_KEY='your_key_here'     # Windows PowerShell\n"
        "    3. Or run the app normally — it will prompt you:\n"
        "         uv --directory src run python main.py\n"
    )

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)


class AgentService:
    def __init__(self):
        ensure_config_dir()
        from pathlib import Path
        from .tools import files
        fs = files.SecureFileSystem(root=Path.cwd())
        file_tools = files.build_file_tools(fs)


                
        self.session = AdvancedSQLiteSession(
            session_id="default",
            db_path=str(get_session_file()),
            create_tables=True,
        )

        self.agent = Agent(
            name="Assistant",
            instructions=load_agent_instructions(),
            model=OpenAIChatCompletionsModel(
                model=MODEL_NAME,
                openai_client=client,
            ),
            tools=[*file_tools]
        )

        self._lock = asyncio.Lock()

    async def ask(self, message: str) -> str:
        from typing import cast
        from agents import Session
        
        async with self._lock:
            result = await Runner.run(
                self.agent,
                message,
                session=cast(Session, self.session),
            )

            # Important
            await self.session.store_run_usage(result)

            return result.final_output
