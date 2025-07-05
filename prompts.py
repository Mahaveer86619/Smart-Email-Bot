class Prompts:
    @staticmethod
    def generate_email_prompt(username: str, prompt: str) -> str:
        """
        Generates a prompt for email generation.

        Args:
            prompt (str): The user's description and/or previous email.
        Returns:
            str: A formatted prompt for generating an email.
        """
        return f"Generate an email with the following details: '{prompt}'. Please ensure the email is professional and concise. The user's name is {username}. Make sure to include a clear subject line and a polite closing. The email should be suitable for sending to a professional contact if the tone is not specified. make the email in paragraphs well spaced and easy to read."
