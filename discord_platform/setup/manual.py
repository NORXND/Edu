from discord import Embed
from storage import add_class


# Funkcja sprawdza nazwy roli lub kanału. Nikt raczej nie nazywa kanału tak samo, jak roli. Chyba.
async def check_names(name, ctx, t='r'):
    if t == 'r':
        for role in ctx.guild.roles:
            if role.name == name:
                return role.id
    elif t == 'c':
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id
    else:
        return ""


# Wysyła pytanie, do nauczyciela, po czym czeka na odp.
async def ask(q, ctx, bot, t='r'):
    await ctx.send(q)

    async def wait_for():
        def check(message):
            return message.channel == ctx.channel and message.author.id is not bot.user.id

        message = await bot.wait_for("message", check=check)
        if message.author.id is not bot.user.id:
            ret = await check_names(ctx=ctx, name=message.content, t=t)
            return ret
        else:
            await wait_for()

    obj = await wait_for()
    return obj


async def manual_setup(ctx, bot):
    setup_data = {}

    # Wysyła wiadomość
    embed = Embed(title="Manualna konfiguracja serwera",
                  description="Na początku, co jest wymagane do działania Edu:", color=0xff8000)
    embed.add_field(name="Rola dla ucznia", value="Domyślne uprawnienia - Nie musisz nic zmieniać.", inline=False)
    embed.add_field(name="Rola dla nauczyciela", value="Rola z uprawnieniami domyślnymi lub własnymi.", inline=False)
    embed.add_field(name="Rola dla wychowawcy", value="Rola z uprawnieniami administracyjnymi. (Nie jest obowiązkowa "
                                                      "lecz jest rekomendowana)", inline=False)
    embed.add_field(name="Rola dla niezweryfikowanych",
                    value="Wszystkie uprawnienia muszą być ustawione na NIE, by utrzymać serwer bezpiecznym.",
                    inline=False)
    embed.add_field(name="Kanał dla nauczyciela", value="Kanał dostępny tylko dla roli nauczyciela.", inline=False)
    embed.add_field(name="Kanał i kategoria dla niezweryfikowanych",
                    value="Kategoria niedostępna do odczytu dla wszystkich ról oprócz niezweryfikowanych. Nikt nie "
                          "może w nim pisać. Zalecane jest by uczeń i nauczyciel nie mieli uprawnień do wyświetlania "
                          "kanału, tylko ze względów estetycznych. (Nie jest obowiązkowa lecz jest rekomendowana).",
                    inline=False)
    embed.set_footer(text="Gdy serwer będzie gotowy, naciśnij przycisk ▶️.")
    message = await ctx.send(embed=embed)
    await message.add_reaction("▶️")

    # Tutaj czeka, aż nauczyciel, doda reakcję ▶.
    async def wait_for():
        def check(payload):
            return payload.message_id == message.id and str(payload.emoji) in '▶️'

        payload = await bot.wait_for("raw_reaction_add", check=check)

        if payload.member is bot.user:
            await wait_for()

    await wait_for()

    # Zadaje pytania i zapisuje odp.
    setup_data["DiscordStudentRole"] = await ask("Na początku, podaj nazwę roli dla ucznia:", ctx, bot)
    setup_data["DiscordTeacherRole"] = await ask("Teraz, podaj nazwę roli dla nauczyciela:", ctx, bot)
    setup_data["DiscordAdminRole"] = await ask("Jeśli masz rolę wychowawcy, "
                                               "wpisz nazwę lub jeśli jej nie masz, "
                                               "napisz cokolwiek innego (np. abc):", ctx, bot)
    setup_data["DiscordUnverifiedRole"] = await ask("Jeszcze, podaj nazwę roli dla osób niezweryfikowanych:", ctx, bot)
    setup_data["DiscordTeacherChannel"] = await ask("I to już ostatnie, kanał dla nauczycieli:", ctx, bot, 'c')

    # Wpisuje dane do bazy danych
    add_class(DiscordGuild=ctx.guild.id,
              DiscordTeacherChannel=setup_data['DiscordTeacherChannel'],
              DiscordUnverifiedRole=setup_data['DiscordUnverifiedRole'],
              DiscordStudentRole=setup_data['DiscordStudentRole'],
              DiscordTeacherRole=setup_data['DiscordTeacherRole'],
              DiscordAdminRole=setup_data['DiscordAdminRole'])

    await ctx.send('UWAGA: Pamiętaj by ustawić uprawnienia roli @everyone na NIE by utrzymać serwer bezpiecznym!')
    # Wysyła wiadomość nr.2
    embed = Embed(title="Gratulacje!", description="Ten serwer jest już gotowy do użycia!", color=0xff8000)
    embed.add_field(name="Zobacz dostępne polecenia!", value="edu:pomoc uczeń", inline=False)
    embed.set_footer(text="Edu został skonfigurowany na tym serwerze!")
    channel = bot.get_channel(setup_data['DiscordTeacherChannel'])
    await channel.send(embed=embed, delete_after=10)
