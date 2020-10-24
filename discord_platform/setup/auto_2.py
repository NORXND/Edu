from discord import Embed
"""
    By zajrzeć w kod main.py, auto_1.py i auto_2.py musisz naprawdę wiedzieć co się dzieje i znać się 
    na discord.py, by to zrozumieć. Nie zamierzam na razie próbować wytłumaczyć co tam się dzieje.
    Spodziewam się, że jest tam dużo różnego syfu.

    Tutaj mamy tworzenie kanałów (tekstowych i głosowych), dane są pozyskiwane z reakcji i wiadomości.
"""

async def auto_setup_2(bot, ctx):
    # Wysyła wiadomość.
    embed = Embed(title="Automatyczna konfiguracja serwera",
                  description="Czy chcesz dodać kanały przedmiotowe?", color=0xff8000)
    embed.add_field(name="Wyślij wiadomość z odpowiednim formatem:",
                    value="PRZEDMIOT 1=PRZEDMIOT 2=PRZEDMIOT 3=PRZEDMIOT4=PRZEDMIOT5=PRZEDMIOT6", inline=False)
    embed.add_field(name="Jeśli nie chesz dodawać kanałów przedmiotowych wpisz:", value="nie", inline=True)
    embed.set_footer(
        text="UWAGA: Jeśli wiadomość będzie miała zły format, może doprowadzić to do błędów lub złego ułożenia/nazwy "
             "kanałów! Upewnij się że wiadomość zawiera poprawny format!")
    embed_message = await ctx.send(embed=embed)

    # Funkcja służy do stworzenia kanałów.
    async def create_channel(guild, names):
        cat = await guild.create_category(name="Przedmioty", position=2)
        if '=' in names:
            names = list(names.split("="))

            for channel in names:
                await guild.create_text_channel(name=f"{channel}", category=cat)
        else:
            await guild.create_text_channel(name=f"{names}", category=cat)
        await ctx.send("Czy wszystkie kanały się zgadzają? Jeśli nie, ponów konfigurację!")

        # Second part
        await ctx.send("Ile klas (Kanałów głosowych) potrzebujesz? Wpisz liczbę lub 0\n"
                       "UWAGA: Wpisanie innej wiadomośći niż liczba spowoduje błąd! "
                       "Upewnij się że wpisujesz poprawną liczbe!!!")

        async def wait_for():
            def check(message):
                return message.channel == embed_message.channel

            message = await bot.wait_for("message", check=check)
            if message.content != '0':
                name = 1
                for x in range(int(message.content)):
                    await guild.create_voice_channel(name=f"Sala lekcyjna {name}", category=cat)
                    name = + 1

        await wait_for()

    async def wait_for():
        def check(message):
            return message.channel == embed_message.channel

        message = await bot.wait_for("message", check=check)
        if 'nie' not in message.content.lower():
            await create_channel(ctx.guild, message.content)

    await wait_for()
