import logging
import os
from dotenv import load_dotenv  # Import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import asyncio
import threading
import nest_asyncio
import time  # Import time untuk menghitung uptime
import json
nest_asyncio.apply()
from bot.utilities.http_server import run_http_server  # Hanya mengimpor run_http_server

# Muat variabel lingkungan dari .env
load_dotenv()

# Aktifkan logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Token bot Anda
TOKEN = os.getenv('API_TOKEN')  # Ambil dari .env

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bot siap menerima pesan!')

# Fungsi untuk menangani pesan yang diterima
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Mengambil teks dari pesan
    text = update.message.text
    # Mengirim ulang pesan yang diterima dengan caption yang diubah
    await update.message.reply_text(f"Caption yang diubah: {text}")

# Fungsi untuk menangani media (foto dan video)
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Mengambil caption asli jika ada
    original_caption = update.message.caption if update.message.caption else ""
    
    # Membuat caption baru dengan beberapa link yang bisa diklik
    clickable_text = (
        '✨ Upload by <a href="http://t.me/Zerozerozoro">Mimin</a> | '
        '<a href="https://sociabuzz.com/firnandaszz/tribe">Donasi</a> | '
        '<a href="http://t.me/Anime_Bahasa_Indonesia">List Anime</a>'
    )
    new_caption = f"{clickable_text}\n{original_caption}"  # Gabungkan caption baru dengan caption asli
    
    if update.message.photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=update.message.photo[-1].file_id, caption=new_caption, parse_mode='HTML')
    elif update.message.video:
        await context.bot.send_video(chat_id=update.effective_chat.id, video=update.message.video.file_id, caption=new_caption, parse_mode='HTML')

# Fungsi untuk menangani perintah /ping
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Pastikan hanya dapat diakses di chat pribadi
    if update.effective_chat.type == 'private':
        await update.message.reply_text("Pong!")

async def main() -> None:
    # Mulai server HTTP di thread terpisah
    threading.Thread(target=run_http_server).start()  # Menjalankan server HTTP di thread terpisah

    # Inisialisasi Application
    application = ApplicationBuilder().token(TOKEN).build()

    # Daftarkan handler untuk perintah
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Menambahkan filter untuk pesan teks
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))  # Menambahkan handler untuk media

    # Mulai bot
    application.run_polling()  # Menjalankan bot Telegram

if __name__ == '__main__':
    asyncio.run(main())  # Menggunakan asyncio.run untuk menjalankan coroutine
