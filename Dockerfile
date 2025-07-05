FROM python:alpine

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose no ports (Telegram bot is outbound only)
# EXPOSE 8080

# Set environment variables (override in docker-compose or with .env)
ENV PYTHONUNBUFFERED=1

# Entrypoint
CMD ["python", "bot.py"]
