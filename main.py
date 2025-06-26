# bot/main.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from bot.analyzer import analyze_chart

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Gunakan .env atau langsung ganti di sini

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_path = "received_chart.jpg"
    await photo_file.download_to_drive(image_path)

    result = analyze_chart(image_path)
    await update.message.reply_text(result)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
