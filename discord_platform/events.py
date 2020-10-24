from discord.ext.commands import Cog
from discord import Embed
import storage

BAD_WORDS = ['kurwa', 'pierdol', 'suka', 'suko', 'kutas', 'cipa', 'idiota', 'idioto', 'debil', 'chuj', 'gruby', 'gruba',
             'huj', 'spierdalaj', 'odwal', 'zjeb']


async def bad_word_check(message):
    content = message.content
    # Formatuję wiadomość (Małe litery, bez białych znaków)
    content = content.lower()
    content = content.strip()

    for word in BAD_WORDS:
        if word in content:
            # Usuwa wiadomość i wysyła informację do ucznia (na czat publiczny)
            await message.delete()
            await message.channel.send(f"{message.author.mention}, nie używaj niepoprawnego słownictwa!",
                                       delete_after=20)


# Klasa Cog'u
class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Funkcja uruchamia się, gdy użytkownik dołączy do serwera.
    @Cog.listener()
    async def on_member_join(self, member):
        data = storage.get_class("DiscordGuild", member.guild.id)
        # Daje użytkownikowi role „nie-zweryfikowany”
        await member.add_roles(member.guild.get_role(data['DiscordUnverifiedRole']))

        # Wysyła informację do nauczyciela.
        channel = member.guild.get_channel(data['DiscordTeacherChannel'])  # Dodaj ID kanału tutaj! (Dla nauczycieli)
        message = await channel.send(
            f"@hare Użytkownik próbował dostać się do klasy! Nazwa użytkownika to {member} Czy chesz go zaakceptować? "
            f"✅ (Tak) / ❌ (Nie)")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        async def wait_for():
            def check(payload):
                return payload.message_id == message.id and str(payload.emoji) in ('✅', '❌')

            payload = await self.bot.wait_for("raw_reaction_add", check=check)

            if payload.member.id is not self.bot.user.id:
                if str(payload.emoji) == '✅':
                    await channel.send("Użytkownik został zatwierdzony! UWAGA: Ma teraz dostęp do klasy jako uczeń!")
                    await member.add_roles(member.guild.get_role(data['DiscordStudentRole']))
                    await member.remove_roles(member.guild.get_role(data['DiscordUnverifiedRole']))
                elif str(payload.emoji) == '❌':
                    await channel.send("Użytkownik został wyrzucony!")
                    await member.kick()
            else:
                await wait_for()
        await wait_for()

    # Funkcja uruchamia się gdy zostanie wysłana nowa wiadomość.
    @Cog.listener()
    async def on_message(self, message):
        await bad_word_check(message)

    # Funkcja uruchamia się gdy zostanie wysłana nowa wiadomość.
    @Cog.listener()
    async def on_guild_join(self, guild):
        embed = Embed(title="Edu", url="https://github.com/NORXND/Edu",
                      description="Witaj! Jestem Edu, twój asystent w zdalnej edukacji! Pomogę ci utrzymać "
                                  "twoje eLekcje bezpiecznie i efektywnie!",
                      color=0xff8000)
        embed.add_field(name="By rozpocząć konfigurację wprowadź poniższą komendę:",
                        value="edu:konfiguracja", inline=False)
        embed.set_footer(text="Made with ❤ to teachers by NORXND")

        if guild.system_channel is not None:
            await guild.system_channel.send(embed=embed, delete_after=600)


def setup(bot):
    bot.add_cog(Events(bot))
