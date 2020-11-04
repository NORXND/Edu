"""
    Czekam aż na jakieś poradniki/dokumentację/przykłady, na razie wszystkie są przestarzałe.
    Jeśli ktoś wie jak tego używać, to proszę o szybki kontakt!
    ----------------------------------------------------------------------------------------
    https://github.com/tulir/fbchat-asyncio
    ----------------------------------------------------------------------------------------
    Poniżej wykonuję testy, więc możesz to ignorować.
"""
import asyncio
import fbchat


async def main():
    # Log the user in
    session = await fbchat.Session.login("edu-pl@teachers.org", "Edu2020Facebook")

    print("Own id: {}".format(session.user.id))

    # Send a message to yourself
    await session.user.send_text("Hi me!")

    # Log the user out
    await session.logout()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()