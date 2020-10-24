from discord.ext.commands import Cog, command, has_permissions
from discord import Embed
from storage import get_class, delete_class
from discord_platform.setup.auto_main import auto_setup
from discord_platform.setup.manual import manual_setup
"""
    By zajrzeć w kod main.py, auto_1.py i auto_2.py musisz naprawdę wiedzieć co się dzieje i znać się 
    na discord.py, by to zrozumieć. Nie zamierzam na razie próbować wytłumaczyć co tam się dzieje.
    Spodziewam się, że jest tam dużo różnego syfu.
    
    W skrócie pierwsza funkcja sprawdza, czy dany serwer ma wpis w bazie danych, po czym go usuwa.
    Druga funkcja to komenda. Po pierwsze wysyła wiadomość, po czym czeka na wybór poprzez reakcję między
    automatyczną a manualną.
"""
# Sprawdza czy zostały już zapisane informację o tym serwerze w bazie danych
async def check_if_already_exits(ctx):
    if get_class("DiscordGuild", ctx.guild.id) is not None:
        # Wysyła wiadomość i usuwa wpis w bazie
        await ctx.send("UWAGA: Dane serwera zostały usunięte z bazy danych!")
        delete_class('DiscordGuild', ctx.guild.id)
        return False
    else:
        return False


# Klasa Cog'u
class Setup(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Pozwala na zkonfigurowanie bota do pierwszego użycia
    @command(name="konfiguracja")
    @has_permissions(administrator=True)
    async def configuration(self, ctx):
        await ctx.message.delete()
        if await check_if_already_exits(ctx) is True:
            return

        # Tworzy nowy embed i go wysyła
        embed = Embed(title="Edu", url="https://github.com/NORXND/Edu",
                      description="Witaj! Jestem Edu, twój asystent w zdalnej edukacji! Pomogę ci utrzymać "
                                  "twoje eLekcje bezpiecznie i efektywnie!",
                      color=0xff8000)
        embed.add_field(name="Czy chesz bym automatycznie zkonfigurował twój serwer Discord?",
                        value="Tak (✅) lub Nie (❌) jeśli sam chcesz dodać kanały/role itp.", inline=False)
        embed.set_footer(text="Made with ❤ to teachers by NORXND")
        welcome_message = await ctx.send(embed=embed)

        # Sprawdza odp nauczyciela i wykonuję daną akcje.
        async def wait_for():
            def check(payload):
                return payload.message_id == welcome_message.id and str(payload.emoji) in ('✅', '❌')

            payload = await self.bot.wait_for("raw_reaction_add", check=check)

            if payload.member.id is not self.bot.user.id:
                if str(payload.emoji) == '✅':
                    await auto_setup(ctx.guild, self.bot, ctx)
                elif str(payload.emoji) == '❌':
                    await manual_setup(ctx, self.bot)
            else:
                await wait_for()

        # Dodaje reakcję i czeka na odp.
        await welcome_message.add_reaction("✅")
        await welcome_message.add_reaction("❌")
        await wait_for()


def setup(bot):
    bot.add_cog(Setup(bot))
