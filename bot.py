import os
import logging
import asyncio
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from flask import Flask
from pymongo import MongoClient
from handlers import (
    start_handler,
    help_handler,
    search_handler,
    movie_selection_callback,
    trending_handler,
    top_handler,
    rating_handler,
    genres_handler,
    subscribe_handler,
    analytics_handler,
    batch_handler,
    trailer_handler,
    admin_handler,
    admin_callback_handler,
    inline_query_handler
)
from config import BOT_TOKEN, MONGO_URI

# ======================================================================
# Logging Configuration
# ======================================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================================================================
# Flask Health Check App
# ======================================================================
app = Flask(__name__)

@app.route("/")
def health():
    return "✅ Bot is Running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ======================================================================
# Database Initialization (MongoDB)
# ======================================================================
def init_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        logger.info("MongoDB connected successfully.")
        return db
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None

# ======================================================================
# Main function to initialize bot and start polling
# ======================================================================
async def main():
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    logger.info("Flask health-check server started on port 8080.")

    db = init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("trending", trending_handler))
    application.add_handler(CommandHandler("top", top_handler))
    application.add_handler(CommandHandler("rating", rating_handler))
    application.add_handler(CommandHandler("genres", genres_handler))
    application.add_handler(CommandHandler("subscribe", subscribe_handler))
    application.add_handler(CommandHandler("analytics", analytics_handler))
    application.add_handler(CommandHandler("batch", batch_handler))
    application.add_handler(CommandHandler("trailer", trailer_handler))
    application.add_handler(CommandHandler("admin", admin_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
    application.add_handler(CallbackQueryHandler(movie_selection_callback))
    application.add_handler(CallbackQueryHandler(admin_callback_handler, pattern="^admin\\|"))
    application.add_handler(MessageHandler(filters.INLINE_QUERY, inline_query_handler))

    for i in range(20):
        logger.info(f"Initialization step {i+1}/20 completed.")
        await asyncio.sleep(0.1)

    logger.info("Telegram Bot is starting polling.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
