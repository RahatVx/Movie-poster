import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext
from flask import Flask

TOKEN = "8059561681:AAFQ0CpRiP-DPB5ZM6XU1YrwIp5-dfPKesY"
LOGS_CHANNEL = "-1002316472437"  # লগ সংরক্ষণের চ্যানেল
SCRAP_CHANNEL = "-1002457337623"  # পোস্টার সংরক্ষণের চ্যানেল

app = Flask(__name__)

@app.route('/')
def health_check():
    return "✅ Bot is Running!"

# 🔹 IMDb থেকে মুভির লিস্ট সংগ্রহ
def search_movies(movie_name):
    search_url = f"https://www.imdb.com/find?q={movie_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    search_page = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(search_page.text, "html.parser")
    
    movies = []
    results = soup.find_all("td", class_="result_text")
    
    for result in results[:5]:  # প্রথম ৫টি রেজাল্ট দেখাবে
        title = result.a.text
        url = "https://www.imdb.com" + result.a["href"]
        movies.append((title, url))
    
    return movies

# 🔹 IMDb থেকে নির্দিষ্ট মুভির তথ্য সংগ্রহ
def get_movie_info(movie_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    movie_page = requests.get(movie_url, headers=headers)
    movie_soup = BeautifulSoup(movie_page.text, "html.parser")
    
    rating = movie_soup.find("span", itemprop="ratingValue")
    genre = movie_soup.find("span", class_="ipc-chip__text")
    
    return (
        rating.text if rating else "N/A",
        genre.text if genre else "Unknown"
    )

# 🔹 ইমেজ তৈরি ফাংশন
def create_image(title, rating, language, genre):
    bg_image = Image.open("background.jpg")
    draw = ImageDraw.Draw(bg_image)
    font = ImageFont.truetype("arial.ttf", 40)

    draw.text((50, 50), f"🎬 {title}", font=font, fill="white")
    draw.text((50, 120), f"⭐ IMDb: {rating}", font=font, fill="yellow")
    draw.text((50, 180), f"🌍 Language: {language}", font=font, fill="white")
    draw.text((50, 240), f"🎭 Genre: {genre}", font=font, fill="white")

    output_path = "output.jpg"
    bg_image.save(output_path)
    return output_path

# 🔹 মুভি নির্বাচন করা হলে
def movie_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    movie_url = query.data
    title = query.message.text.split("\n")[0]  # প্রথম লাইনেই মুভির নাম

    rating, genre = get_movie_info(movie_url)
    
    # 🔹 ইউজারকে ভাষা সেট করার জন্য কীবোর্ড
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data=f"{movie_url}|English")],
        [InlineKeyboardButton("🇧🇩 বাংলা", callback_data=f"{movie_url}|বাংলা")],
        [InlineKeyboardButton("🌎 Other", callback_data=f"{movie_url}|Other")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text(
        f"🎬 **{title}**\n\n⭐ **IMDb:** {rating}\n🎭 **Genre:** {genre}\n\n➡️ ভাষা সিলেক্ট করুন:",
        reply_markup=reply_markup
    )

# 🔹 ভাষা নির্বাচন করা হলে
def language_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    movie_url, language = query.data.split("|")
    title = query.message.text.split("\n")[0]
    
    rating, genre = get_movie_info(movie_url)
    output_path = create_image(title, rating, language, genre)
    
    with open(output_path, "rb") as img:
        query.message.reply_photo(photo=InputFile(img))
    
    # 🔹 Scrap Channel-এ সংরক্ষণ
    context.bot.send_photo(chat_id=SCRAP_CHANNEL, photo=open(output_path, "rb"), caption=f"🎬 {title}\n⭐ IMDb: {rating}\n🌍 Language: {language}\n🎭 Genre: {genre}")
    
    os.remove(output_path)

# 🔹 মুভি খোঁজার হ্যান্ডলার
def search_movie(update: Update, context: CallbackContext):
    movie_name = update.message.text.strip()
    movies = search_movies(movie_name)
    
    if not movies:
        update.message.reply_text("⚠️ কোনো মুভি পাওয়া যায়নি!")
        return
    
    keyboard = [[InlineKeyboardButton(title, callback_data=url)] for title, url in movies]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("📌 নিচের তালিকা থেকে মুভি সিলেক্ট করুন:", reply_markup=reply_markup)

# 🔹 স্টার্ট হ্যান্ডলার
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📢 Main Channel", url="https://t.me/RM_Movie_Flix")],
        [InlineKeyboardButton("📀 Backup Channel", url="https://t.me/RM_Movi")],
        [InlineKeyboardButton("📩 Request Group", url="https://t.me/Movies_Rm")],
        [InlineKeyboardButton("🛠 Admins", url="https://t.me/RahatMx")],
        [InlineKeyboardButton("💬 Support Group", url="https://t.me/Movies_Supports")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("🎥 মুভির নাম লিখুন, আমি পোস্টার তৈরি করবো!", reply_markup=reply_markup)
    
    # 🔹 লগ চ্যানেলে মেসেজ পাঠানো
    context.bot.send_message(chat_id=LOGS_CHANNEL, text=f"🟢 User Started: @{update.message.from_user.username}")

# 🔹 মেইন ফাংশন
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_movie))
    dp.add_handler(CallbackQueryHandler(movie_selected, pattern="https://www.imdb.com"))
    dp.add_handler(CallbackQueryHandler(language_selected, pattern="https://www.imdb.com.*"))

    updater.start_polling()
    app.run(host="0.0.0.0", port=8080)
    updater.idle()

if __name__ == "__main__":
    main()
