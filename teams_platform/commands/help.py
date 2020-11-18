from botbuilder.schema import Activity, Attachment


async def helpcmd(ctx):
    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
            {
                "type": "Container",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "Dostępne komendy",
                        "weight": "bolder",
                        "size": "medium"
                    }
                ]
            },
            {"type": "TextBlock", "text": "Chcesz coś zaproponować? Pisz do nas śmiało! ;)", "wrap": True},
            {
                "type": "Container",
                "items": [
                    {
                        "type": "FactSet",
                        "facts": [
                            {
                                "title": "pomoc",
                                "value": "Wyświetla pomoc"
                            },
                            {"title": "wps", "value": "Szuka artykulow na Wikipedii"},
                            {"title": "wpw", "value": "Wyświetla artykuł z Wikipedii"}
                        ]
                    }
                ]
            }
        ]
    }

    reply_content = Attachment(content_type='application/vnd.microsoft.card.adaptive',
                               content=card)
    await ctx.send_activity(Activity(type='message', attachments=[reply_content]))
