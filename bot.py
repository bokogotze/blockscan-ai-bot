import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from database import create_user, has_used_trial, set_trial_used, set_premium
from payment_handler import create_invoice
from commands.start import start
from commands.walletscan import walletscan
from commands.tokenscan import tokenscan
from commands.scamcheck import scamcheck
from commands.marketsim import marketsim

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ---------- Commands ---------- #

async def trial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if has_used_trial(user_id):
        await update.message.reply_text("❌ You already used your free 1-day trial.")
        return

    set_premium(user_id, 1)
    set_trial_used(user_id)

    await update.message.reply_text("🎉 Your free *1-day premium trial* is now ACTIVE!")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        "💳 *Creating your subscription invoice...*\n"
        "Please wait 3–5 seconds.",
        parse_mode="Markdown"
    )

    invoice_url, invoice_id = create_invoice(user_id, currency="usdt")

    if not invoice_url:
        await update.message.reply_text("❌ Error creating invoice. Try again.")
        return

    await update.message.reply_text(
        f"💎 *BlockScan AI Premium*\n\n"
        f"Price: *$49 / month*\n"
        f"Invoice ID: `{invoice_id}`\n\n"
        f"👉 Pay here:\n{invoice_url}",
        parse_mode="Markdown"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Unknown command. Try /start")


# ---------- App ---------- #

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Base Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trial", trial))
    app.add_handler(CommandHandler("subscribe", subscribe))

    # Premium AI Tools
    app.add_handler(CommandHandler("walletscan", walletscan))
    app.add_handler(CommandHandler("tokenscan", tokenscan))
    app.add_handler(CommandHandler("scamcheck", scamcheck))
    app.add_handler(CommandHandler("marketsim", marketsim))

    # Unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
