from discord_platform.setup.auto_1 import auto_setup_1
from discord_platform.setup.auto_2 import auto_setup_2
from discord import HTTPException, Embed
from storage import add_class


# Funkcja służy do automatycznego stworzenia serwera discord.
async def auto_setup(guild, bot, ctx):
    print(f"Konfiguracja serwera {guild.id}")
    # Zapisuje dane do późniejszego czyszczenia serwera.
    server_cleanup = {'t': guild.text_channels, 'v': guild.voice_channels, 'r': guild.roles, 'c': guild.categories}

    # Rozpoczyna konfigurację
    setup_data = await auto_setup_1(guild)

    # Czyści serwer
    await auto_setup_2(bot, ctx)
    for x in server_cleanup['t']:
        await x.delete()
    for x in server_cleanup['v']:
        await x.delete()
    for x in server_cleanup['r']:
        if x.name != "@everyone" or x.name != "EDU":
            try:
                await x.delete()
            except HTTPException:
                pass
    for x in server_cleanup['c']:
        await x.delete()

    # Wpisuje dane do bazy danych
    add_class(DiscordGuild=setup_data['DiscordGuild'],
              DiscordTeacherChannel=setup_data['DiscordTeacherChannel'],
              DiscordUnverifiedRole=setup_data['DiscordUnverifiedRole'],
              DiscordStudentRole=setup_data['DiscordStudentRole'],
              DiscordTeacherRole=setup_data['DiscordTeacherRole'],
              DiscordAdminRole=setup_data['DiscordAdminRole'])

    # Wysyła wiadomość
    embed = Embed(title="Gratulacje!", description="Ten serwer jest już gotowy do użycia!", color=0xff8000)
    embed.add_field(name="Zobacz dostępne polecenia!", value="edu:pomoc uczeń", inline=False)
    embed.set_footer(text="Edu został skonfigurowany na tym serwerze!")
    channel = bot.get_channel(setup_data['DiscordTeacherChannel'])
    await channel.send(embed=embed, delete_after=10)
