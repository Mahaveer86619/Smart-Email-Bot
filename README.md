# Smart Email Bot

Smart Email Bot is an intelligent tool designed to automate and manage email tasks efficiently. This guide provides easy-to-follow instructions to help you set up and run the project on your local system using two methods:

- **Method 1:** Using Docker Compose (Recommended)
- **Method 2:** Using Python Virtual Environment

---

## Prerequisites

- **Git** installed on your system.
- For Docker methods: **Docker** and **Docker Compose** installed ([Get Docker](https://docs.docker.com/get-docker/)).
- For Python method:
  - **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/)).
  - **pip** (usually comes with Python).

---

## Method 1: Running with Docker Compose (Recommended)

This is the fastest and easiest way to get started. Docker Compose will automatically build and run all necessary services.

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Mahaveer86619/Smart-Email-Bot.git
   cd Smart-Email-Bot
   ```

2. **Run with Docker Compose**
   ```bash
   docker compose up
   ```
   or (for older Docker versions)
   ```bash
   docker-compose up
   ```

   - This will automatically build images (if needed) and start the application.
   - To stop the application, press `Ctrl+C` and/or run `docker compose down`.

   > **Note:** If you need to rebuild after making changes, run:
   > ```bash
   > docker compose up --build
   > ```

---

## Method 2: Running with Python Virtual Environment

If you prefer not to use Docker, you can set up a Python virtual environment manually.

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Mahaveer86619/Smart-Email-Bot.git
   cd Smart-Email-Bot
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **On Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **On Windows:**
     ```cmd
     venv\Scripts\activate
     ```

4. **Install Project Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python bot.py
   ```

---

## Environment Variables Setup

This project requires a `.env` file for configuration. An example file `.env.example` is provided for reference.

### Steps to Set Up `.env`

1. **Copy the Example env File: **
   
   Make a new `.env` file to add your keys and settings as described below.

3. **Fill in the following fields in your `.env` file:**

   ```env
   GEMINI_API_KEY="YOUR-KEY"
   TELEGRAM_BOT_TOKEN="YOUR-KEY"
   SMTP_SERVER="smtp.gmail.com"
   SMTP_PORT=587
   ```

   - `GEMINI_API_KEY`:  
     Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).  
     Create a project, enable the Gemini API, and generate an API key.

   - `TELEGRAM_BOT_TOKEN`:  
     Get your bot token by talking to [@BotFather](https://t.me/botfather) on Telegram.  
     Create a new bot and BotFather will provide you with a token.

   - `SMTP_SERVER` and `SMTP_PORT`:  
     Default values are provided for Gmail. If you use another email provider, update these fields accordingly.

---

## Configuration

- Make sure to set up any required **environment variables** or **configuration files** as described above or in the [docs](./docs) or project documentation.
- For sensitive credentials (API keys, passwords), use the `.env` file or Docker secrets.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).
