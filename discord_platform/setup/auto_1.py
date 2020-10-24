from discord import Colour, Permissions, PermissionOverwrite

"""
    By zajrzeć w kod main.py, auto_1.py i auto_2.py musisz naprawdę wiedzieć co się dzieje i znać się 
    na discord.py, by to zrozumieć. Nie zamierzam na razie próbować wytłumaczyć co tam się dzieje.
    Spodziewam się, że jest tam dużo różnego syfu.

    Tutaj głównie tworzone są role, kategorię i kanały. Tyle. Ostrzegałem.
"""

# Część 1
async def auto_setup_1(guild):
    # Ustawia uprawnienia @everyone.
    await guild.default_role.edit(permissions=Permissions.none())

    # Tworzy role ucznia.
    pupil_perms = Permissions.none()
    pupil_perms.add_reactions = True
    pupil_perms.read_messages = True
    pupil_perms.send_messages = True
    pupil_perms.send_tts_messages = True
    pupil_perms.embed_links = True
    pupil_perms.attach_files = True
    pupil_perms.read_message_history = True
    pupil_perms.external_emojis = True
    pupil_perms.connect = True
    pupil_perms.speak = True
    pupil_perms.use_voice_activation = True

    pupil_role = await guild.create_role(name="Uczeń", colour=Colour.green(), permissions=pupil_perms, hoist=True)

    # Tworzy role „niezweryfikowany".
    unveryfied_role = await guild.create_role(name="Nie Zweryfikowany", permissions=Permissions.none())

    # Tworzy rolę "Nauczyciel".
    teacher_perms = Permissions.all()
    teacher_perms.administrator = False
    teacher_perms.view_audit_log = False
    teacher_perms.manage_channels = False
    teacher_perms.manage_emojis = False
    teacher_perms.manage_guild = False
    teacher_perms.manage_permissions = False
    teacher_perms.manage_roles = False
    teacher_perms.manage_webhooks = False

    teacher_role = await guild.create_role(name="Nauczyciel", colour=Colour.blue(), permissions=teacher_perms,
                                           hoist=True)

    # Tworzy rolę "Wychowawca"
    admin_perms = Permissions.general()
    admin_perms.administrator = True
    admin_role = await guild.create_role(name="Wychowawca", colour=Colour.red(), permissions=admin_perms, hoist=True)

    # Ustawia role w kolejności.
    positions = {
        unveryfied_role: 1,  # penultimate role
        pupil_role: 2,
        teacher_role: 3,
        admin_role: 4,
        guild.me: 5
    }
    await guild.edit_role_positions(positions=positions)

    # Tworzy kategorię i kanał "Weryfikacja"
    veryfi_overwrite = {
        unveryfied_role: PermissionOverwrite(read_message_history=True, read_messages=True),
        teacher_role: PermissionOverwrite(view_channel=False),
        pupil_role: PermissionOverwrite(view_channel=False),
        admin_role: PermissionOverwrite(view_channel=False)}
    veryfi_cat = await guild.create_category(name="Weryfikacja", overwrites=veryfi_overwrite, position=3)
    veryfi_channel = await guild.create_text_channel(name="Witaj", category=veryfi_cat)
    await veryfi_channel.send("Witaj! Ten serwer jest chroniony przez Edu! By uzyskać do niego dostęp będzie wymagana "
                              "weryfikacja nauczyciela.")

    # Tworzy kategorie główny i kanały
    main_cat = await guild.create_category(name="Główny", position=1)
    await guild.create_text_channel(name="Główny", category=main_cat)
    await guild.create_voice_channel(name="Główny", category=main_cat)
    teacher_channel = await guild.create_text_channel(name="Pokój Nauczycielski",
                                                      overwrites={pupil_role: PermissionOverwrite(view_channel=False)},
                                                      category=main_cat)
    # Zachowuje stworzone dane
    setup_data = {'DiscordGuild': guild.id,
                  'DiscordTeacherChannel': teacher_channel.id,
                  'DiscordUnverifiedRole': unveryfied_role.id,
                  'DiscordStudentRole': pupil_role.id,
                  'DiscordAdminRole': admin_role.id,
                  'DiscordTeacherRole': teacher_role.id}

    return setup_data
