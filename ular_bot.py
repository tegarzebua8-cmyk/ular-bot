import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Papan kocak
ULARS = {99: 54, 70: 32, 51: 11, 36: 6, 92: 88}
TANGGAS = {4: 25, 13: 46, 33: 85, 42: 63, 62: 81}
KOCAK_EVENT = [
    "😜 Kena gosip tetangga, mundur 3 langkah!",
    "😍 Dapet peluk virtual dari pacar rahasia, maju 4 langkah!",
    "🤣 Kepleset kulit pisang, pingsan 1 giliran!",
    "🔥 Ditagih utang, panik dan lari 5 langkah ke depan!"
]

user_pos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_pos[user_id] = 1
    await update.message.reply_text(
        f"Hai {update.effective_user.first_name}! Selamat datang di Ular Tangga Pacar Rahasia ID 😜\n\n"
        f"Kamu di kotak 1. Ketik /roll buat kocok dadu 🎲\n"
        f"Ketik /posisi buat liat posisi."
    )

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_pos:
        user_pos[user_id] = 1
    
    dadu = random.randint(1, 6)
    pos_lama = user_pos[user_id]
    pos_baru = pos_lama + dadu
    
    if pos_baru > 100:
        await update.message.reply_text(f"🎲 Dadu: {dadu}. Yah kelebihan! Kamu butuh pas 100. Tetap di {pos_lama}")
        return

    pesan = f"🎲 Dadu: {dadu}\nDari {pos_lama} -> {pos_baru}\n"

    if pos_baru in ULARS:
        pesan += f"🐍 YAHA KENA ULAR! Turun dari {pos_baru} ke {ULARS[pos_baru]}!\n"
        pos_baru = ULARS[pos_baru]
    elif pos_baru in TANGGAS:
        pesan += f"🪜 ASIK DAPET TANGGA! Naik dari {pos_baru} ke {TANGGAS[pos_baru]}!\n"
        pos_baru = TANGGAS[pos_baru]
    else:
        if random.random() < 0.3:
            pesan += f"{random.choice(KOCAK_EVENT)}\n"

    user_pos[user_id] = pos_baru

    if pos_baru == 100:
        pesan += "\n🎉🎉 MENANG! Kamu sampe ke pelaminan sama pacar rahasia! Ketik /start buat ulang."
    else:
        pesan += f"\nSekarang kamu di kotak {pos_baru}. Roll lagi!"

    await update.message.reply_text(pesan)

async def posisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pos = user_pos.get(update.effective_user.id, 1)
    await update.message.reply_text(f"Kamu sekarang di kotak {pos} / 100")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("BOT_TOKEN belum di set!")
        exit(1)
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("posisi", posisi))
    
    print("Bot is running...")
    app.run_polling()
