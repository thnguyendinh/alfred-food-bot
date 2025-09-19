import os
import logging
import random
import asyncio
import urllib.parse
import pg8000.native
import sqlite3
import time
import httpx
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from telegram.error import TelegramError
from foods_data import VIETNAMESE_FOODS, REGIONAL_FOODS

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Env variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
PORT = int(os.getenv("PORT", 8443))

# Log environment variables
logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")
logger.info(f"DATABASE_URL: {'Set' if DATABASE_URL else 'Not set'}")
logger.info(f"PORT: {PORT}")
logger.info(f"TOKEN: {'Set' if TOKEN else 'Not set'}")

# Database
class Database:
    def __init__(self):
        self.use_postgres = False
        self.pg_conn = None
        self.sqlite_conn = None
        if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
            try:
                parsed = urllib.parse.urlparse(DATABASE_URL)
                db_params = {
                    "user": parsed.username,
                    "password": parsed.password,
                    "host": parsed.hostname,
                    "port": parsed.port,
                    "database": parsed.path.lstrip('/')
                }
                self.pg_conn = pg8000.native.Connection(**db_params)
                self.use_postgres = True
                self.pg_conn.run("CREATE TABLE IF NOT EXISTS eaten_foods (user_id TEXT, food TEXT, timestamp INTEGER)")
                logger.info("Connected to PostgreSQL")
            except Exception as e:
                logger.error(f"Postgres init failed: {e}. Falling back to SQLite.")
                self._init_sqlite()
        else:
            self._init_sqlite()

    def _init_sqlite(self):
        try:
            self.sqlite_conn = sqlite3.connect("alfred.db", check_same_thread=False)
            self.sqlite_conn.execute("""
                CREATE TABLE IF NOT EXISTS eaten_foods (
                    user_id TEXT, 
                    food TEXT, 
                    timestamp INTEGER
                )
            """)
            self.sqlite_conn.commit()
            logger.info("Connected to SQLite successfully")
        except sqlite3.Error as e:
            logger.error(f"SQLite connection error: {e}")
            os.makedirs(os.path.dirname("alfred.db"), exist_ok=True)
            try:
                self.sqlite_conn = sqlite3.connect("alfred.db", check_same_thread=False)
                self.sqlite_conn.execute("""
                    CREATE TABLE IF NOT EXISTS eaten_foods (
                        user_id TEXT, 
                        food TEXT, 
                        timestamp INTEGER
                    )
                """)
                self.sqlite_conn.commit()
                logger.info("SQLite connection established after retry")
            except sqlite3.Error as e2:
                logger.error(f"SQLite retry failed: {e2}")
                raise

    def get_conn(self):
        return self.pg_conn if self.use_postgres else self.sqlite_conn

    def add_eaten(self, user_id, food):
        conn = self.get_conn()
        try:
            timestamp = int(time.time())
            if self.use_postgres:
                conn.run("INSERT INTO eaten_foods (user_id, food, timestamp) VALUES (:u, :f, :t)", u=user_id, f=food, t=timestamp)
            else:
                conn.execute("INSERT INTO eaten_foods (user_id, food, timestamp) VALUES (?, ?, ?)", (user_id, food, timestamp))
                conn.commit()
            logger.info(f"Added food {food} for user {user_id} at {timestamp}")
        except Exception as e:
            logger.error(f"DB add error: {e}")

    def get_eaten(self, user_id):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                rows = conn.run("SELECT food FROM eaten_foods WHERE user_id=:u ORDER BY timestamp DESC LIMIT 10", u=user_id)
                return [r[0] for r in rows]
            else:
                rows = conn.execute("SELECT food FROM eaten_foods WHERE user_id=? ORDER BY timestamp DESC LIMIT 10", (user_id,))
                return [r[0] for r in rows.fetchall()]
        except Exception as e:
            logger.error(f"DB fetch error: {e}")
            return []

db = Database()

# Handlers
def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /start from user {user_id} in chat {chat_id}")
    try:
        response = (
            "Xin chào! Mình là Alfred Food Bot.\n"
            "- /suggest: Gợi ý món ăn ngẫu nhiên.\n"
            "- /region [tên vùng]: Gợi ý món theo vùng (ví dụ: /region Hà Nội).\n"
            "- /ingredient [nguyên liệu1, nguyên liệu2]: Gợi ý món từ nguyên liệu.\n"
            "- /location: Chia sẻ vị trí để gợi ý món địa phương.\n"
            "- Gửi tên món: Tra thông tin chi tiết."
        )
        update.message.reply_text(response)
        logger.info(f"Sent /start response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /start response to user {user_id}: {e}")

def suggest(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /suggest from user {user_id} in chat {chat_id}")
    try:
        eaten = db.get_eaten(user_id)
        options = [f for f in VIETNAMESE_FOODS.keys() if f not in eaten]
        if not options:
            options = list(VIETNAMESE_FOODS.keys())
        choice = random.choice(options)
        db.add_eaten(user_id, choice)
        food_info = VIETNAMESE_FOODS[choice]
        response = (
            f"Hôm nay bạn thử món: *{choice}*\n"
            f"- Loại: {food_info['type']}\n"
            f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
            f"- Cách làm: {food_info['recipe']}\n"
            f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
            f"- Dịp: {', '.join(food_info['holidays'])}\n"
            f"- Calo ước tính: {food_info['calories']}"
        )
        update.message.reply_text(response, parse_mode="Markdown")
        logger.info(f"Sent /suggest response to user {user_id}: {choice}")
    except Exception as e:
        logger.error(f"Failed to send /suggest response to user {user_id}: {e}")

def region_suggest(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /region from user {user_id} with args: {context.args}")
    try:
        if context.args:
            user_input = ' '.join(context.args)
            def normalize_string(s):
                import unicodedata
                return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8').lower()

            normalized_input = normalize_string(user_input)
            normalized_regions = {normalize_string(key): key for key in REGIONAL_FOODS.keys()}

            def levenshtein_distance(s1, s2):
                if len(s1) < len(s2):
                    return levenshtein_distance(s2, s1)
                if len(s2) == 0:
                    return len(s1)
                previous_row = range(len(s2) + 1)
                for i, c1 in enumerate(s1):
                    current_row = [i + 1]
                    for j, c2 in enumerate(s2):
                        insertions = previous_row[j + 1] + 1
                        deletions = current_row[j] + 1
                        substitutions = previous_row[j] + (c1 != c2)
                        current_row.append(min(insertions, deletions, substitutions))
                    previous_row = current_row
                return previous_row[-1]

            best_match = min(normalized_regions.keys(), key=lambda k: levenshtein_distance(normalized_input, k))
            distance = levenshtein_distance(normalized_input, best_match)
            if distance <= 3:
                region = normalized_regions[best_match]
                foods = REGIONAL_FOODS[region]
                response = f"Món ăn phổ biến tại *{region}*: {', '.join(foods)}"
                update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /region response to user {user_id}: {region}")
            else:
                response = f"Không tìm thấy vùng '{user_input}'. Thử 'Hà Nội', 'Sài Gòn', v.v."
                update.message.reply_text(response)
                logger.info(f"Sent /region not found response to user {user_id}")
        else:
            response = "Sử dụng: /region [tên vùng], ví dụ: /region Hà Nội"
            update.message.reply_text(response)
            logger.info(f"Sent /region usage response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /region response to user {user_id}: {e}")

def ingredient_suggest(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /ingredient from user {user_id} with args: {context.args}")
    try:
        if context.args:
            user_ingredients = [ing.lower() for ing in ' '.join(context.args).split(',')]
            matching_foods = []
            for food, info in VIETNAMESE_FOODS.items():
                if any(ing in [i.lower() for i in info['ingredients']] for ing in user_ingredients):
                    matching_foods.append(food)
            if matching_foods:
                choice = random.choice(matching_foods)
                food_info = VIETNAMESE_FOODS[choice]
                response = (
                    f"Món gợi ý từ nguyên liệu: *{choice}*\n"
                    f"- Loại: {food_info['type']}\n"
                    f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
                    f"- Cách làm: {food_info['recipe']}\n"
                    f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
                    f"- Dịp: {', '.join(food_info['holidays'])}\n"
                    f"- Calo ước tính: {food_info['calories']}"
                )
                update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /ingredient response to user {user_id}: {choice}")
            else:
                response = "Không tìm thấy món phù hợp với nguyên liệu. Thử lại!"
                update.message.reply_text(response)
                logger.info(f"Sent /ingredient not found response to user {user_id}")
        else:
            response = "Sử dụng: /ingredient [nguyên liệu1, nguyên liệu2], ví dụ: /ingredient thịt bò, rau thơm"
            update.message.reply_text(response)
            logger.info(f"Sent /ingredient usage response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /ingredient response to user {user_id}: {e}")

def location_suggest(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /location from user {user_id}")
    try:
        response = "Chia sẻ vị trí của bạn để tôi gợi ý món địa phương (chỉ dùng để gợi ý, không lưu)."
        update.message.reply_text(response)
        logger.info(f"Sent /location response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /location response to user {user_id}: {e}")

def handle_location(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    location = update.message.location
    logger.info(f"Received location from user {user_id}: {location.latitude if location else None}, {location.longitude if location else None}")
    try:
        if location:
            region = "Sài Gòn"  # Giả lập, cần API geocode để thực tế
            foods = REGIONAL_FOODS.get(region, [])
            if foods:
                response = f"Dựa trên vị trí, vùng gần: *{region}*. Món gợi ý: {', '.join(foods)}"
                update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent location-based response to user {user_id}: {region}")
            else:
                response = "Không tìm thấy vùng gần vị trí của bạn."
                update.message.reply_text(response)
                logger.info(f"Sent location not found response to user {user_id}")
        else:
            response = "Vui lòng chia sẻ position."
            update.message.reply_text(response)
            logger.info(f"Sent location request response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send location response to user {user_id}: {e}")

def echo(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    text = update.message.text.lower()
    logger.info(f"Received text '{text}' from user {user_id}")
    try:
        if text in VIETNAMESE_FOODS:
            food_info = VIETNAMESE_FOODS[text]
            response = (
                f"{text} là món ăn nổi tiếng!\n"
                f"- Loại: {food_info['type']}\n"
                f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
                f"- Cách làm: {food_info['recipe']}\n"
                f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
                f"- Dịp: {', '.join(food_info['holidays'])}\n"
                f"- Calo ước tính: {food_info['calories']}"
            )
            update.message.reply_text(response)
            logger.info(f"Sent echo response to user {user_id}: {text}")
        else:
            response = "Mình chưa có thông tin món này. Thử /suggest để gợi ý mới!"
            update.message.reply_text(response)
            logger.info(f"Sent echo not found response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send echo response to user {user_id}: {e}")

# Build Application
try:
    logger.info("Building Telegram application...")
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logger.info("Application built successfully")
except Exception as e:
    logger.error(f"Failed to build application: {e}")
    raise

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("suggest", suggest))
dispatcher.add_handler(CommandHandler("region", region_suggest))
dispatcher.add_handler(CommandHandler("ingredient", ingredient_suggest))
dispatcher.add_handler(CommandHandler("location", location_suggest))
dispatcher.add_handler(MessageHandler(Filters.location, handle_location))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Flask app for Render webhook
flask_app = Flask(__name__)

@flask_app.post("/webhook")
def webhook():
    try:
        update = Update.de_json(request.get_json(), updater.bot)
        dispatcher.process_update(update)
        return "ok", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "Error", 500

@flask_app.get("/")
def index():
    return "Alfred Food Bot is running!", 200

# Set webhook on startup
def set_webhook():
    try:
        updater.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        logger.info(f"Webhook set to {WEBHOOK_URL}/webhook")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")

# Main
if __name__ == "__main__":
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL is not set")
        raise ValueError("WEBHOOK_URL is not set")
    
    set_webhook()
    logger.info("Bot started successfully")
