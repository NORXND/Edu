from .events import on_message
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
