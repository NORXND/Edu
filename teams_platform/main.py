from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
)

import teams_platform.commands.wiki as cmd_wiki
from storage import SECRET

# Potrzebna zmienna
ADAPTER = BotFrameworkAdapter(BotFrameworkAdapterSettings(SECRET['TEAMS_APPID'], SECRET['TEAMS_PASSWORD']))


# Funkcja początkowa.
async def api_handler(context):
    if context.activity.type == "message":
        await message_handler(context)


# Rozprowadza event do odpowiedniej funkcji.
async def message_handler(context):
    cmd = " ".join(list(context.activity.text.split(" "))[1])
    ctx = context
    arg = " ".join(list(context.activity.text.split(" "))[2:])
    # Szuka komendy, niestety nie da się chyba inaczej tego zrobić...
    if 'wpw' == cmd.lower():
        await cmd_wiki.wpw(ctx, arg)
    elif 'wps' == cmd.lower():
        await cmd_wiki.wps(ctx, arg)
