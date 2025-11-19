from database import create_user, has_used_trial

def start(update, context):
    user = update.effective_user
    user_id = user.id

    create_user(user_id)

    update.message.reply_text(
        "👋 *Welcome to BlockScan AI!*\n\n"
        "Your personal crypto intelligence assistant.\n\n"
        "🔥 Features:\n"
        "• Wallet analysis (/walletscan)\n"
        "• Token inspection (/tokenscan)\n"
        "• Scam detection (/scamcheck)\n"
        "• Market simulation (/marketsim)\n\n"
        "💎 Upgrade to *Premium* for full access.\n"
        "Use /subscribe to get started.\n\n"
        "🎁 You can also use /trial for a free 1-day premium trial "
        "*(only available once)*."
    )
