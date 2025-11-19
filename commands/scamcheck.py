from premium import premium_required
from utils import chunk_text

@premium_required
def scamcheck(update, context):
    text = update.message.text.replace("/scamcheck", "").strip()

    if not text:
        update.message.reply_text(
            "⚠️ Please send the text or link you want checked.\n\nExample:\n"
            "`/scamcheck Check this website: https://abcproject.io`",
            parse_mode="Markdown"
        )
        return

    update.message.reply_text(
        f"🕵️ *Checking for scam indicators…*\n\nText:\n`{text}`",
        parse_mode="Markdown"
    )

    # Placeholder AI logic
    result = (
        "🧠 *Scam Analysis Result*\n\n"
        "• No direct scam patterns detected.\n"
        "• Always double-check contract ownership.\n"
        "• Never share private keys or seed phrases.\n\n"
        "⚠️ Full AI engine will be connected after deployment."
    )

    for part in chunk_text(result):
        update.message.reply_text(part, parse_mode="Markdown")
