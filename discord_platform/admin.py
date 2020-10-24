from discord.ext.commands import Cog, command, has_permissions
from discord import Member


# Klasa Cog'u
class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Komenda służy do zablokowania użytkownika
    @command(name="zablokuj")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, reason: str = "brak powodu."):
        await ctx.message.delete()
        # Blokuje uzytkownika
        await member.ban(reason=reason)
        # Wysyła potwierdzenie do nauczyciela
        await ctx.send(f"Użytkownik {member.mention} został zablokowany!", delete_after=5)

    # Komenda służy do wyrzucenia użytkownika z serwera
    @command(name="wyrzuć")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, reason: str = "brak powodu."):
        await ctx.message.delete()
        # Wyrzuca uzytkownika
        await member.kick(reason=reason)
        # Wysyła potwierdzenie do nauczyciela
        await ctx.send(f"Użytkownik {member.mention} został zablokowany!", delete_after=5)

    # Komenda służy do usunięcia danej liczby wiadmości
    @command(name="usuń")
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, ammount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=ammount)
        await ctx.send(f"{ammount} wiadomości zostało usnięte!", delete_after=5)


def setup(bot):
    bot.add_cog(Admin(bot))
