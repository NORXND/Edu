"""
Edu - Zdalna edukacja dla każdego!
----------------------------------------------------------------
Copyright (C) 2020, Chojrak Development. All rights reserved.
ONLY POLISH VERSION AVAILABLE, SOME FUTURES MAY NOT BE SUPPORTED BY ENGLISH EVEN AFTER TRANSLATIONS !!!
----------------------------------------------------------------
Obsługiwane platformy:
- Discord (BETA)

Github: https://github.com/NORXND/Edu

Pomoc i kontakt (Support and Contact):
Email - szymon.piotr.grzegorzewski@gmail.com
Discord - NORXND#6717

Thank you for using Edu! ~Made with ❤ to teachers by NORXND!
"""
from discord_platform.main import init as discord
from server import init as server

# Uruchamia bota discord'a.
discord()

# Uruchamia serwer Flask.
server()
