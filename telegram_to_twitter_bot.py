import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import tweepy

# Load environment variables from the .env file
load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Set up Twitter API client
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
twitter_api = tweepy.API(auth)

# Function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the message and media (if any) from Telegram
    chat_id = update.effective_chat.id
    message_text = update.message.text or ""
    media = update.message.photo or update.message.video

    try:
        # If there's media, download and upload it to Twitter
        if media:
            file = media[-1].get_file()
            file_path = await file.download()

            # Upload media to Twitter and post tweet
            media_obj = twitter_api.media_upload(file_path)
            twitter_api.update_status(status=message_text, media_ids=[media_obj.media_id])
        else:
            # Just post the message if there's no media
            twitter_api.update_status(status=message_text)

        await context.bot.send_message(chat_id=chat_id, text="Posted to Twitter successfully!")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error posting to Twitter: {e}")

# Set up the application
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Add message handler
message_handler = MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO, handle_message)
app.add_handler(message_handler)

# Start the bot
if __name__ == "__main__":
    app.run_polling()
