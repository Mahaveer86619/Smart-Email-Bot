from dotenv import load_dotenv, dotenv_values
import os
import sys

# Load environment variables from .env file
load_dotenv()

# Load secrets from environment variables or .env file
CONFIG = dotenv_values(".env")


def get_env(key, default=None, required=False):
    value = os.getenv(key) or CONFIG.get(key) or default
    if required and (value is None or str(value).strip() == ""):
        raise ValueError(f"Missing required environment variable: {key}")
    return value


# --- Required Configs ---
TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN", required=True)
GEMINI_API_KEY = get_env("GEMINI_API_KEY", required=True)

# --- SMTP Configs ---
SMTP_SERVER = get_env("SMTP_SERVER", required=True)
SMTP_PORT = int(get_env("SMTP_PORT", 587))
SMTP_USERNAME = get_env("SMTP_USERNAME", required=True)
SMTP_PASSWORD = get_env("SMTP_PASSWORD", required=True)
SENDER_EMAIL = get_env("SENDER_EMAIL", required=True)


def check_config():
    """Check all required configuration variables and exit if any are missing."""
    errors = []
    required_vars = [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("GEMINI_API_KEY", GEMINI_API_KEY),
        ("SMTP_SERVER", SMTP_SERVER),
        ("SMTP_PORT", SMTP_PORT),
        ("SMTP_USERNAME", SMTP_USERNAME),
        ("SMTP_PASSWORD", SMTP_PASSWORD),
        ("SENDER_EMAIL", SENDER_EMAIL),
    ]
    for key, value in required_vars:
        if value is None or str(value).strip() == "":
            errors.append(key)
    if errors:
        print(
            f"Error: Missing required configuration(s): {', '.join(errors)}",
            file=sys.stderr,
        )
        sys.exit(1)


# Optionally run check_config() here if you want to fail fast on import
# check_config()
