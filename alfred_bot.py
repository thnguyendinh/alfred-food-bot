
import os
import logging
import random
import asyncio
import urllib.parse
import pg8000.native
import sqlite3
import time
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
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
PORT = int(os.getenv("PORT", 10000))

# Log environment variables
logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")
logger.info(f"DATABASE_URL: {'Set' if DATABASE_URL else 'Not set'}")
logger.info(f"PORT: {PORT}")
logger.info(f"TOKEN: {'Set' if TOKEN else 'Not set'}")

# Validate token
async def validate_token():
    try:
        bot = Bot(TOKEN)
        await bot.get_me()
        logger.info("Bot token is valid")
        return True
    except Exception as e:
        logger.error(f"Invalid bot token: {e}")
        return False

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
            self.sqlite_conn.execute("CREATE TABLE IF NOT EXISTS eaten_foods (user_id TEXT, food TEXT, timestamp INTEGER)")
            self.sqlite_conn.commit()
            logger.info("Connected to SQLite")
        except Exception as e:
            logger.error(f"SQLite init failed: {e}")

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
    logger.info(f"Received /start from user {update.effective_user.id}")
    await update.message.reply_text(
        "Xin chào! Mình là Alfred Food Bot.\n"
        "- /suggest: Gợi ý món ăn ngẫu nhiên.\n"
        "- /region [tên vùng]: Gợi ý món theo vùng (ví dụ: /region Hà Nội).\n"
        "- /ingredient [nguyên liệu1, nguyên liệu2]: Gợi ý món từ nguyên liệu.\n"
        "- /location: Chia sẻ vị trí để gợi ý món địa phương.\n"
        "- Gửi tên món: Tra thông tin chi tiết."
    )

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"Received /suggest from user {user_id}")
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
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

async def region_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"Received /region from user {user_id} with args: {context.args}")
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
        else:
            await update.message.reply_text(f"Không tìm thấy vùng '{user_input}'. Thử 'Hà Nội', 'Sài Gòn', v.v.")
    else:
        await update.message.reply_text("Sử dụng: /region [tên vùng], ví dụ: /region Hà Nội")
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

async def ingredient_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"Received /ingredient from user {user_id} with args: {context.args}")
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
        else:
            await update.message.reply_text("Không tìm thấy món phù hợp với nguyên liệu. Thử lại!")
    else:
        await update.message.reply_text("Sử dụng: /ingredient [nguyên liệu1, nguyên liệu2], ví dụ: /ingredient thịt bò, rau thơm")
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

async def location_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"Received /location from user {user_id}")
    await update.message.reply_text("Chia sẻ vị trí của bạn để tôi gợi ý món địa phương (chỉ dùng để gợi ý, không lưu).")
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    location = update.message.location
    if location:
        logger.info(f"Received location from user {user_id}: {location.latitude}, {location.longitude}")
        region = "Sài Gòn"  # Giả lập, cần API geocode để thực tế
        foods = REGIONAL_FOODS.get(region, [])
        if foods:
            response = f"Dựa trên vị trí, vùng gần: *{region}*. Món gợi ý: {', '.join(foods)}"
            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text("Không tìm thấy vùng gần vị trí của bạn.")
    else:
        await update.message.reply_text("Vui lòng chia sẻ position.")
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.lower()
    logger.info(f"Received text '{text}' from user {user_id}")
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
    else:
        await update.message.reply_text("Mình chưa có thông tin món này. Thử /suggest để gợi ý mới!")
    # Lệnh giả
    await asyncio.sleep(0.1)
    fake_update = Update.de_json(
        {
            'update_id': random.randint(1, 1000),
            'message': {
                'text': '/fake',
                'chat': {'id': user_id, 'type': 'private'},
                'date': int(time.time())
            }
        }, application.bot
    )
    await application.process_update(fake_update)

# Build Application
try:
    logger.info("Building Telegram application...")
    application = ApplicationBuilder().token(TOKEN).http_version("1.1").build()
    logger.info("Application built successfully")
except Exception as e:
    logger.error(f"Failed to build application: {e}")
    raise

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("suggest", suggest))
application.add_handler(CommandHandler("region", region_suggest))
application.add_handler(CommandHandler("ingredient", ingredient_suggest))
application.add_handler(CommandHandler("location", location_suggest))
application.add_handler(MessageHandler(filters.LOCATION, handle_location))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Initialize application
logger.info("Initializing application...")
asyncio.get_event_loop().run_until_complete(application.initialize())
logger.info("Application initialized successfully")

# Flask app for Render webhook
flask_app = Flask(__name__)

@flask_app.post("/webhook")
def webhook():
    try:
        json_data = request.get_json(force=True)
        logger.info(f"Received webhook data: {json_data}")
        update = Update.de_json(json_data, application.bot)
        if update:
            logger.info(f"Processing update: {update.update_id}")
            asyncio.run_coroutine_threadsafe(application.process_update(update), asyncio.get_event_loop())
            logger.info(f"Processed update: {update.update_id}")
            # Lệnh giả trong webhook
            fake_update = Update.de_json(
                {
                    'update_id': random.randint(1, 1000),
                    'message': {
                        'text': '/fake',
                        'chat': {'id': update.effective_user.id, 'type': 'private'},
                        'date': int(time.time())
                    }
                }, application.bot
            )
            asyncio.run_coroutine_threadsafe(application.process_update(fake_update), asyncio.get_event_loop())
            return "ok", 200
        else:
            logger.warning("Received invalid update")
            return "Invalid update", 400
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return "Error", 500

@flask_app.get("/webhook")
def webhook_get():
    logger.warning("Webhook endpoint only accepts POST requests")
    return "Method Not Allowed: Use POST for webhook", 405

@flask_app.route("/")
def index():
    return "Alfred Food Bot running!", 200

# Main
if __name__ == "__main__":
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL is not set")
        raise ValueError("WEBHOOK_URL is not set")
    
    async def set_webhook():
        try:
            webhook_info = await application.bot.get_webhook_info()
            logger.info(f"Current webhook info: {webhook_info}")
            if webhook_info.url != f"{WEBHOOK_URL}/webhook":
                await application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
                logger.info(f"Webhook set to {WEBHOOK_URL}/webhook")
            else:
                logger.info("Webhook already set correctly")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            raise
    
    logger.info("Starting bot and setting webhook...")
    asyncio.get_event_loop().run_until_complete(set_webhook())
    logger.info("Starting Flask server...")
    flask_app.run(host="0.0.0.0", port=PORT)
