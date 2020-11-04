from botbuilder.schema import Mention
from botbuilder.core import MessageFactory

BAD_WORDS = ['kurwa', 'pierdol', 'suka', 'suko', 'kutas', 'cipa', 'idiota', 'idioto', 'debil', 'chuj', 'gruby', 'gruba',
             'huj', 'spierdalaj', 'odwal', 'zjeb']

async def bad_word_check(context):
    content = context.activity.text
    # Formatuję wiadomość (Małe litery, bez białych znaków)
    content = content.lower()
    content = content.strip()

    for word in BAD_WORDS:
        if word in content:
            # Usuwa wiadomość i wysyła informację do ucznia (na czat publiczny)
            mention = Mention(
                mentioned=context.activity.from_property,
                text=f"{context.activity.from_property.name}",
                type="mention"
            )
            reply_activity = MessageFactory.text(f"{mention.text}, nie używaj niepoprawnego słownictwa!")
            reply_activity.entities = [Mention().deserialize(mention.serialize())]
            await context.send_activity(reply_activity)

# Event dla wiadomości.
async def on_message(context):
    await bad_word_check(context)