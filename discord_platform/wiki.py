from discord import Embed
from discord.ext.commands import Cog, command

import commands.wikipedia as wikipedia


# Klasa Cog'u
class Wiki(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='wps')
    async def wps(self, ctx, key: str, limit=10):
        search = wikipedia.search(key, limit)
        embed = Embed(title="Wynik wyszukiwania z Wikipedii", description=f"Hasło: {key}", color=0xff8000)
        for x in search:
            embed.add_field(name=x["Tytuł"], value=x["Opis"], inline=False)

        await ctx.send(embed=embed)

    @command(name='wpw')
    async def wpw(self, ctx, key: str):
        page = wikipedia.show(key)

        if page["Obrazek"] is None:
            page["Obrazek"] = Embed.Empty

        embed = Embed(title="Artykuł na Wikipedii", url=page['URL'], description="", color=0xff8000)
        embed.set_image(url=page["Obrazek"])
        embed.add_field(name=page["Tytuł"], value=page['Opis'], inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))
