from .events import on_message
import teams_platform.commands.wiki as cmd_wiki
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
)

# Potrzebna zmienna
ADAPTER = BotFrameworkAdapter(BotFrameworkAdapterSettings("", ""))

# Funkcja początkowa.
async def api_handler(context):
    await event_handler(context)

# Rozprowadza event do odpowiedniej funkcji.
async def event_handler(context):
    if context.activity.type == "message":
        await on_message(context)
        if context.activity.text.startswith('edu:'):
            pass

async def command_handler(context):
    cmd = context.activity.text
    pass