from discord.ext.commands import Cog, command
from discord import Embed
from storage import get_class

"""
Nie ma tu nic do komentowania. 2 funkcje to wysyłanie wiadomośći, 3 sprawdza argument.
"""


async def student_help(ctx):
    embed = Embed(title="Pomoc", description="Lista dostępnych poleceń", color=0xff8000)
    embed.add_field(name="undefined", value="undefined", inline=False)
    embed.set_footer(text="By wyświetlić polecenia dla nauczyciela, pisz edu:pomoc nauczyciel")
    await ctx.send(embed=embed, delete_after=30)


async def teacher_help(ctx):
    if ctx.guild.get_role(get_class('DiscordGuild', ctx.guild.id)['DiscordTeacherRole']) in ctx.author.roles:
        embed = Embed(title="Pomoc", description="Lista dostępnych poleceń dla nauczyciela", color=0xff8000)
        embed.add_field(name="edu:zablokuj @{użytkownik} {Powód}}", value="Blokuje użytkownika.", inline=False)
        embed.add_field(name="edu:wyrzuć @{użytkownik} {Powód}}",
                        value="Wyrzuca użytkownika, może on dołączyć ponownie.", inline=False)
        embed.add_field(name="edu:usuń {Liczba}", value="Usuwa liczbe wiadomości w kanale.", inline=False)
        embed.set_footer(text="By wyświetlić polecenia dla nauczyciela, pisz edu:pomoc uczeń")
        await ctx.send(embed=embed)
    else:
        await ctx.send("To polecenie może być użyte tylko przez nauczyciela!")


# Klasa Cog'u
class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='pomoc')
    async def help(self, ctx, menu='uczeń'):
        if menu == 'nauczyciel':
            await teacher_help(ctx)
        else:
            await student_help(ctx)


def setup(bot):
    bot.add_cog(Help(bot))
