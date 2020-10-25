from discord.ext.commands import Bot
from discord import Activity, ActivityType, Intents
from sys import platform as current_os_platform
from asyncio import get_event_loop, get_child_watcher
from threading import Thread
from storage import SECRET

# Tworzenie klasy bota.
bot = Bot(command_prefix='edu:', intents=Intents().all())


# Kod uruchamia się przy zalogowaniu.
@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.playing, name=f"EDU - edu:pomoc"))
    print(' * Zalogowano pomyślnie!')


"""
Sekwencja uruchamiania bota: 
-> Tworzenie pętli asyncio.
--> Tworzenie zadania dla pętli (funkcja bot_final_start).
---> Tworzenie wątku modułu threading.
-----> Uruchamianie wątku.
"""


async def bot_final_start():
    # Loguje się do klienta bota za pomocą tokenu.
    await bot.start(SECRET['DISCORD_TOKEN'])


def bot_loop_start(event_loop):
    # Uruchamia pętle „na zawsze”.
    event_loop.run_forever()


if current_os_platform != 'win32':
    get_child_watcher()


def init():
    loop = get_event_loop()
    loop.create_task(bot_final_start())
    bot_thread = Thread(target=bot_loop_start, args=(loop,))
    bot_thread.start()


cogs = ['discord_platform.admin', 'discord_platform.events', 'discord_platform.setup.main', 'discord_platform.help']

for extension in cogs:
    bot.load_extension(extension)
