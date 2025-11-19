from database import is_premium

def premium_required(func):
    """
    Decorator to restrict commands to premium users.
    """
    def wrapper(update, context):
        user_id = update.effective_user.id

        if not is_premium(user_id):
            update.message.reply_text(
                "❌ *Premium Required*\n\n"
                "This command is only available for *BlockScan AI Premium* users.\n"
                "Upgrade now with /subscribe"
            )
            return

        return func(update, context)

    return wrapper
