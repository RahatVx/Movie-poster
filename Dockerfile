# Dockerfile for Advanced Movie Bot
FROM python:3.9

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask port
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
