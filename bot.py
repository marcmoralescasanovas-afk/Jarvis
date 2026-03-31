import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from voice import transcribe_audio
from agent import ask_agent
from tts import speak

load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Jarvis, tu asistente personal 🤖\n\nPuedes escribirme o enviarme un mensaje de voz 🎙️"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = await ask_agent(user_message)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Escuchando...")

    voice_file = await update.message.voice.get_file()
    file_path = f"voice_{update.message.message_id}.ogg"
    await voice_file.download_to_drive(file_path)

    text = transcribe_audio(file_path)
    os.remove(file_path)

    await update.message.reply_text(f"📝 Entendido: _{text}_", parse_mode="Markdown")

    response = await ask_agent(text)
    await update.message.reply_text(response)

    audio_path = speak(response)
    if audio_path:
        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(audio)
        os.remove(audio_path)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("✅ Jarvis está activo...")
    app.run_polling()
