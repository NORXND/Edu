from os import getenv, environ

import mysql.connector
from boto.s3.connection import S3Connection

# Jeśli program jest na Heroku, pobiera sekrety
try:
    s3 = S3Connection(environ['S3_KEY'], environ['S3_SECRET'])
except KeyError:
    # Lub po prostu pomija.
    pass

# Przypisuje sekrety.
SECRET = dict()
SECRET['DATABASE_HOST'] = getenv("DATABASE_HOST")
SECRET['DATABASE_LOGIN'] = getenv("DATABASE_LOGIN")
SECRET['DATABASE_PASSWORD'] = getenv("DATABASE_PASSWORD")
SECRET['DATABASE_NAME'] = getenv("DATABASE_NAME")
SECRET['DISCORD_TOKEN'] = getenv("DISCORD_TOKEN")
SECRET['TEAMS_APPID'] = getenv("TEAMS_APPID")
SECRET['TEAMS_PASSWORD'] = getenv("TEAMS_PASSWORD")

# Łączy się z bazą danych.
DB = mysql.connector.connect(
    host=SECRET['DATABASE_HOST'],
    user=SECRET['DATABASE_LOGIN'],
    password=SECRET['DATABASE_PASSWORD'],
    database=SECRET['DATABASE_NAME']
)
DB_CURSOR = DB.cursor(buffered=True)

# Konwertuje tekst na liczbę lub na tekst (?) lub na NoneType.
def convert(v):
    try:
        return int(v)
    except ValueError:
        try:
            return str(v)
        except ValueError:
            return None


# Zbiera dane o klasie
def get_class(key, value):
    DB_CURSOR.execute(f"SELECT * FROM `main` WHERE `{key}` = {value}")
    result = DB_CURSOR.fetchone()
    try:
        return {"DiscordGuild": convert(result[1]),
                "MessengerThread": convert(result[2]),
                "MessengerAdminName": convert(result[3]),
                "DiscordTeacherChannel": convert(result[4]),
                "DiscordUnverifiedRole": convert(result[5]),
                "DiscordStudentRole": convert(result[6]),
                "DiscordTeacherRole": convert(result[7]),
                "DiscordAdminRole": convert(result[8])}
    except TypeError:
        return None

# Tworzy nową klasę.
def add_class(DiscordGuild="", MessengerThread="", MessengerAdminName="", DiscordTeacherChannel="",
              DiscordUnverifiedRole="", DiscordStudentRole="", DiscordTeacherRole="",
              DiscordAdminRole=""):
    DB_CURSOR.execute(f"INSERT INTO `main` (`DiscordGuild`, `MessengerThread`, `MessengerAdminName`, "
                      f"`DiscordTeacherChannel`, `DiscordUnverifiedRole`, "
                      f"`DiscordStudentRole`, `DiscordTeacherRole`, `DiscordAdminRole`) "
                      f"VALUES ('{DiscordGuild}', '{MessengerThread}', '{MessengerAdminName}', "
                      f"'{DiscordTeacherChannel}', '{DiscordUnverifiedRole}', "
                      f"'{DiscordStudentRole}', '{DiscordTeacherRole}', '{DiscordAdminRole}')")
    DB.commit()


# Usuwa dane o klasie.
# Nie ma tam nic co mogło by być wielce stracone, config i gotowe ;).
def delete_class(key, value):
    DB_CURSOR.execute(f"DELETE FROM `main` WHERE `main`.`{key}` = {value}")
    DB.commit()
