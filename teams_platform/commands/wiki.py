from botbuilder.core.card_factory import CardFactory
from botbuilder.schema import ThumbnailCard, Activity, Attachment
from botframework.connector.models import CardImage, CardAction

import commands.wikipedia as wikipedia


def wps(ctx, key: str, limit=10):
    search = wikipedia.search(key, limit)
    # Nie ma innej metody :(
    card = {"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "type": "Container",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Wyniki wyszukiwania na Wikipedii",
                            "weight": "bolder",
                            "size": "medium"
                        }
                    ]},
                {
                    "type": "TextBlock",
                    "text": f"Hasło: {key}",
                    "wrap": True
                },
                {
                    "type": "Container",
                    "items": [
                        {
                            "type": "FactSet",
                            "facts": []}]}]}
    for x in search:
        fact = {"title": x["Tytuł"], "value": x["Opis"]}
        card['body'][2]['items'][0]["facts"].append(fact)

    reply_content = Attachment(content_type='application/vnd.microsoft.card.thumbnail',
                               content=CardFactory.adaptive_card(card=card))
    await ctx.send_activity(Activity(type='message', attachments=[reply_content]))


def wpw(ctx, key: str):
    page = wikipedia.show(key)

    if page["Obrazek"] is None:
        page["Obrazek"] = "https://norxnd.cal24.pl/edu/asset/inne.png"

    card = ThumbnailCard(title="Artykuł na Wikipedii",
                         subtitle=page['Tytuł'], text=page['Opis'],
                         images=[
                             CardImage(url=page["Obrazek"])
                         ],
                         buttons=[
                             CardAction(
                                 type="openUrl",
                                 title="Zobacz na Wikipedii",
                                 value=page['URL'])
                         ])

    reply_content = Attachment(content_type='application/vnd.microsoft.card.thumbnail',
                               content=card)
    await ctx.send_activity(Activity(type='message', attachments=[reply_content]))
