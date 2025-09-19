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
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"START HANDLER: Received /start from user {user_id}")
    
    try:
        response = (
            "Xin chào! Mình là Alfred Food Bot.\n"
            "- /suggest: Gợi ý món ăn ngẫu nhiên.\n"
            "- /region [tên vùng]: Gợi ý món theo vùng (ví dụ: /region Hà Nội).\n"
            "- /ingredient [nguyên liệu1, nguyên liệu2]: Gợi ý món từ nguyên liệu.\n"
            "- /location: Chia sẻ vị trí để gợi ý món địa phương.\n"
            "- Gửi tên món: Tra thông tin chi tiết."
        )
        
        logger.info(f"START HANDLER: Attempting to reply to user {user_id}")
        await update.message.reply_text(response)
        logger.info(f"START HANDLER: Successfully replied to user {user_id}")
        
    except Exception as e:
        logger.error(f"START HANDLER ERROR: {e}", exc_info=True)

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(response, parse_mode="Markdown")
        logger.info(f"Sent /suggest response to user {user_id}: {choice}")
    except Exception as e:
        logger.error(f"Failed to send /suggest response to user {user_id}: {e}")

async def region_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /region response to user {user_id}: {region}")
            else:
                response = f"Không tìm thấy vùng '{user_input}'. Thử 'Hà Nội', 'Sài Gòn', v.v."
                await update.message.reply_text(response)
                logger.info(f"Sent /region not found response to user {user_id}")
        else:
            response = "Sử dụng: /region [tên vùng], ví dụ: /region Hà Nội"
            await update.message.reply_text(response)
            logger.info(f"Sent /region usage response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /region response to user {user_id}: {e}")

async def ingredient_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /ingredient response to user {user_id}: {choice}")
            else:
                response = "Không tìm thấy món phù hợp với nguyên liệu. Thử lại!"
                await update.message.reply_text(response)
                logger.info(f"Sent /ingredient not found response to user {user_id}")
        else:
            response = "Sử dụng: /ingredient [nguyên liệu1, nguyên liệu2], ví dụ: /ingredient thịt bò, rau thơm"
            await update.message.reply_text(response)
            logger.info(f"Sent /ingredient usage response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /ingredient response to user {user_id}: {e}")

async def location_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /location from user {user_id}")
    try:
        response = "Chia sẻ vị trí của bạn để tôi gợi ý món địa phương (chỉ dùng để gợi ý, không lưu)."
        await update.message.reply_text(response)
        logger.info(f"Sent /location response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /location response to user {user_id}: {e}")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    location = update.message.location
    logger.info(f"Received location from user {user_id}: {location.latitude if location else None}, {location.longitude if location else None}")
    try:
        if location:
            region = "Sài Gòn"
            foods = REGIONAL_FOODS.get(region, [])
            if foods:
                response = f"Dựa trên vị trí, vùng gần: *{region}*. Món gợi ý: {', '.join(foods)}"
                await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent location-based response to user {user_id}: {region}")
            else:
                response = "Không tìm thấy vùng gần vị trí của bạn."
                await update.message.reply_text(response)
                logger.info(f"Sent location not found response to user {user_id}")
        else:
            response = "Vui lòng chia sẻ position."
            await update.message.reply_text(response)
            logger.info(f"Sent location request response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send location response to user {user_id}: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await update.message.reply_text(response)
            logger.info(f"Sent echo response to user {user_id}: {text}")
        else:
            response = "Mình chưa có thông tin món này. Thử /suggest để gợi ý mới!"
            await update.message.reply_text(response)
            logger.info(f"Sent echo not found response to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send echo response to user {user_id}: {e}")

# Build Application
# Build Application
try:
    logger.info("Building Telegram application...")
    application = ApplicationBuilder().token(TOKEN).build()
    logger.info("Application built successfully")
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("suggest", suggest))
    application.add_handler(CommandHandler("region", region_suggest))
    application.add_handler(CommandHandler("ingredient", ingredient_suggest))
    application.add_handler(CommandHandler("location", location_suggest))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    logger.info("All handlers registered successfully")
    
except Exception as e:
    logger.error(f"Failed to build application: {e}", exc_info=True)
    raise

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("suggest", suggest))
application.add_handler(CommandHandler("region", region_suggest))
application.add_handler(CommandHandler("ingredient", ingredient_suggest))
application.add_handler(CommandHandler("location", location_suggest))
application.add_handler(MessageHandler(filters.LOCATION, handle_location))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Flask app for Render webhook
flask_app = Flask(__name__)

@flask_app.post("/webhook")
def webhook():
    try:
        # Nhận và parse update
        update_data = request.get_json()
        logger.info(f"Received webhook update: {update_data}")
        
        if not update_data:
            logger.warning("Empty update received")
            return "Empty update", 400
            
        update = Update.de_json(update_data, application.bot)
        
        # Xử lý update
        if update and update.message:
            logger.info(f"Processing update: {update.update_id}, message: {update.message.text}")
            
            # Xử lý update trực tiếp
            asyncio.run_coroutine_threadsafe(
                application.process_update(update),
                asyncio.get_event_loop()
            )
            return "ok", 200
        else:
            logger.warning("Invalid update format")
            return "Invalid update", 400
            
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return "Error", 500
@flask_app.get("/")
def index():
    return "Alfred Food Bot is running!", 200

# Set webhook on startup
async def set_webhook():
    try:
        await application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
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
    
    # Initialize and set webhook
    async def init_bot():
        try:
            # Test bot token
            bot_info = await application.bot.get_me()
            logger.info(f"Bot info: {bot_info}")
            
            # Set webhook
            await set_webhook()
            
            # Check webhook info
            webhook_info = await application.bot.get_webhook_info()
            logger.info(f"Webhook info: {webhook_info}")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}", exc_info=True)
            raise
    
    # Khởi tạo application
    try:
        # Initialize application (phiên bản 20.x không cần await initialize())
        logger.info("Application starting...")
        asyncio.run(init_bot())
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise
