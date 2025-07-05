from google import genai
from google.genai import types
import json

from configs import CONFIG
from models.structured_email import StructuredEmail
from prompts import Prompts

GEMINI_API_KEY = CONFIG.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_email(username: str, prompt: str, previous_email: str = None) -> dict:
    """
    Generate an email using Gemini, optionally appending previous email for context.
    Returns the parsed email as a dict.
    """
    # Append previous email to the prompt if provided
    full_prompt = prompt
    if previous_email:
        full_prompt += f"\n\nPrevious generated email:\n{previous_email}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=Prompts.generate_email_prompt(username, full_prompt),
        config={
            "response_mime_type": "application/json",
            "response_schema": StructuredEmail,
        },
    )
    # Parse the JSON response
    email_json = (
        response.text if hasattr(response, "text") else response
    )  # adjust if needed
    try:
        email_data = json.loads(email_json)
    except Exception:
        email_data = {}

    return email_data
