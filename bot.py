import logging
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

from configs import TELEGRAM_BOT_TOKEN, check_config
from gemini_service import generate_email
from email_smtp import send_email_smtp

# --- Configuration ---
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Bot Command Handlers ---


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the /help command is issued."""

    user = update.message.from_user
    logger.info("User %s requested help.", user.first_name)

    await update.message.reply_text(
        f"Hello {user.first_name}, 👋\n\n"
        "Welcome to Smart Mail Bot — your assistant for composing and sending professional emails directly from Telegram.\n\n"
        "Here's how to use me:\n"
        "1️⃣  Use /setup to securely provide your sender email and app password (required only once).\n"
        "2️⃣  Use /compose to start a new email. I'll ask for the subject or a brief description.\n"
        "3️⃣  I'll generate a draft for you. You can modify it by simply sending a new prompt, or proceed to send.\n"
        "4️⃣  When you're ready, use /confirm. I'll ask for recipient email addresses (comma-separated for multiple recipients).\n"
        "5️⃣  Once you provide the recipients, I'll send your email and confirm delivery.\n\n"
        "You can restart the process anytime with /compose or get help with /help.\n\n"
        "If you have any questions or encounter issues, please contact the administrator.\n\n"
        "Thank you for using Smart Mail Bot! 🚀"
    )


async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiate setup to collect sender email and SMTP password from the user."""
    user = update.message.from_user
    logger.info("User %s started setup.", user.first_name)
    context.user_data.clear()
    context.user_data["awaiting_setup_email"] = True
    await update.message.reply_text(
        "Please enter your sender email address (the email you want to send from):",
        reply_markup=ForceReply(selective=True),
    )


async def handle_setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Handle setup steps for collecting sender email and SMTP password."""
    user = update.message.from_user
    message = update.message.text

    if context.user_data.get("awaiting_setup_email"):
        context.user_data["setup_sender_email"] = message.strip()
        context.user_data["awaiting_setup_email"] = False
        context.user_data["awaiting_setup_password"] = True
        await update.message.reply_text(
            "Now enter your app password (SMTP password) for this email:",
            reply_markup=ForceReply(selective=True),
        )
        return True

    if context.user_data.get("awaiting_setup_password"):
        context.user_data["setup_smtp_password"] = message.strip()
        context.user_data["awaiting_setup_password"] = False
        await update.message.reply_text(
            "✅ Setup complete! You can now use /compose to start writing your email."
        )
        logger.info("User %s completed setup.", user.first_name)
        return True

    return False


async def compose_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiates the email composition process by asking for subject."""
    user = update.message.from_user
    # Check if setup is done
    if not context.user_data.get("setup_sender_email") or not context.user_data.get(
        "setup_smtp_password"
    ):
        await update.message.reply_text(
            "Please run /setup first to provide your sender email and app password."
        )
        return
    logger.info("User %s started composing an email.", user.first_name)
    context.user_data["awaiting_email_content"] = True
    context.user_data["awaiting_email_modification"] = False
    context.user_data["awaiting_recipients"] = False
    await update.message.reply_text(
        f"Great, {user.first_name}! Please provide the subject or a brief description of the email you'd like to send in any tone."
    )


async def send_email_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handles the /confirm command to start the recipient input process."""
    user = update.message.from_user
    try:
        if not context.user_data.get("last_generated_email"):
            await update.message.reply_text(
                "Please compose and review your email first using /compose."
            )
            return
        if context.user_data.get("awaiting_recipients"):
            await update.message.reply_text(
                "I'm already waiting for recipient email addresses. Please enter them, separated by commas."
            )
            return
        context.user_data["awaiting_recipients"] = True
        await update.message.reply_text(
            "Please enter the recipient email address(es), separated by commas if sending to multiple people."
        )
    except Exception as e:
        logger.error("Error in /confirm: %s", e)
        await update.message.reply_text(
            "An error occurred. Please try again or use /compose to restart."
        )


async def log_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user messages: setup, generates/modifies email, or logs recipient emails."""
    user = update.message.from_user
    message = update.message.text

    # Handle setup workflow
    if await handle_setup(update, context):
        return

    try:
        # Awaiting subject/description for email
        if context.user_data.get("awaiting_email_content"):
            logger.info(
                "User %s provided email subject/description: %s",
                user.first_name,
                message,
            )
            await update.message.reply_text("Generating your email, please wait...")
            previous_email = context.user_data.get("last_generated_email")
            try:
                email_data = generate_email(
                    username=user.first_name,
                    prompt=message,
                    previous_email=previous_email,
                )
            except Exception as e:
                logger.error("Error generating email: %s", e)
                await update.message.reply_text(
                    "Sorry, I couldn't generate your email. Please try again or /compose to restart."
                )
                return
            context.user_data["last_generated_email"] = email_data.get("body", "")
            context.user_data["last_generated_subject"] = email_data.get("subject", "")
            email_preview = f"Subject: {email_data.get('subject', '(No Subject)')}\n\n{email_data.get('body', '(No Body)')}"
            await update.message.reply_text(f"Here is your generated email.")
            await update.message.reply_text(email_preview)
            await update.message.reply_text(
                "If you'd like to modify it, just send a new prompt/description. When you're ready to send, use /confirm."
            )
            context.user_data["awaiting_email_content"] = False
            context.user_data["awaiting_email_modification"] = True
            return

        # Awaiting modification prompt
        if context.user_data.get("awaiting_email_modification"):
            if context.user_data.get("awaiting_recipients"):
                # If user is supposed to enter recipients, don't treat as modification
                pass
            else:
                logger.info(
                    "User %s modifying email with: %s", user.first_name, message
                )
                previous_email = context.user_data.get("last_generated_email")
                try:
                    email_data = generate_email(
                        username=user.first_name,
                        prompt=message,
                        previous_email=previous_email,
                    )
                except Exception as e:
                    logger.error("Error modifying email: %s", e)
                    await update.message.reply_text(
                        "Sorry, I couldn't modify your email. Please try again or /compose to restart."
                    )
                    return
                context.user_data["last_generated_email"] = email_data.get("body", "")
                context.user_data["last_generated_subject"] = email_data.get(
                    "subject", ""
                )
                email_preview = f"Subject: {email_data.get('subject', '(No Subject)')}\n\n{email_data.get('body', '(No Body)')}"
                await update.message.reply_text(
                    f"Here is your revised email:\n\n{email_preview}\n\n"
                    "Send another prompt to modify again, or use /confirm when you're ready."
                )
                return

        # Awaiting recipient emails
        if context.user_data.get("awaiting_recipients"):
            recipients = [
                email.strip() for email in message.split(",") if email.strip()
            ]
            if not recipients:
                await update.message.reply_text(
                    "No valid recipient emails detected. Please enter at least one email address."
                )
                return
            context.user_data["recipients"] = recipients
            logger.info("User %s provided recipients: %s", user.first_name, recipients)
            await update.message.reply_text("Sending email...")
            try:
                # Use user-provided sender email and password
                send_email_smtp(
                    recipients,
                    context.user_data.get("last_generated_subject", "(No Subject)"),
                    context.user_data.get("last_generated_email", "(No Body)"),
                    sender_email=context.user_data.get("setup_sender_email"),
                    smtp_password=context.user_data.get("setup_smtp_password"),
                )
                await update.message.reply_text(
                    f"✅ Email sent to: {', '.join(recipients)}"
                )
                logger.info("Email sent to: %s", recipients)
            except Exception as e:
                logger.error("Error sending email: %s", e)
                await update.message.reply_text(
                    "❌ Failed to send email. Please check the recipient addresses, or verify your SMTP credentials, then try again."
                )
            context.user_data["awaiting_recipients"] = False
            return

        # If user sends a message out of workflow
        await update.message.reply_text(
            "I'm not sure what to do with that message. Use /compose to start a new email or /help for instructions."
        )
        logger.info(
            "User %s sent a message out of workflow: %s", user.first_name, message
        )

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        await update.message.reply_text(
            "An unexpected error occurred. Please use /compose to start over."
        )


def main() -> None:
    """Run the bot."""
    check_config()  # Ensure all configs are valid before starting
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setup", setup_command))
    application.add_handler(CommandHandler("compose", compose_email))
    application.add_handler(CommandHandler("confirm", send_email_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, log_user_message)
    )
    logger.info("Bot started polling. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
