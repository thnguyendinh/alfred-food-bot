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
from telegram import Update, Bot
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

# Validate token
async def validate_token():
    try:
        bot = Bot(TOKEN)
        bot_info = await bot.get_me()
        logger.info(f"Bot token is valid: {bot_info}")
        return True
    except TelegramError as te:
        logger.error(f"Invalid bot token: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
        return False
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        return False

# Database
class Database:
    # Trong class Database, sửa phương thức _init_sqlite
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
        # Tạo thư mục nếu cần
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
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /start from user {user_id} in chat {chat_id}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
        response = (
            "Xin chào! Mình là Alfred Food Bot.\n"
            "- /suggest: Gợi ý món ăn ngẫu nhiên.\n"
            "- /region [tên vùng]: Gợi ý món theo vùng (ví dụ: /region Hà Nội).\n"
            "- /ingredient [nguyên liệu1, nguyên liệu2]: Gợi ý món từ nguyên liệu.\n"
            "- /location: Chia sẻ vị trí để gợi ý món địa phương.\n"
            "- Gửi tên món: Tra thông tin chi tiết."
        )
        async with httpx.AsyncClient() as client:
            http_response = await client.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": response}
            )
            logger.info(f"HTTP response for /start to user {user_id}: status={http_response.status_code}, body={http_response.text}")
            http_response.raise_for_status()
        sent_message = await update.message.reply_text(response)
        logger.info(f"Sent /start response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in /start for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in /start for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send /start response to user {user_id}: {e}")

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /suggest from user {user_id} in chat {chat_id}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
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
        async with httpx.AsyncClient() as client:
            http_response = await client.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": response, "parse_mode": "Markdown"}
            )
            logger.info(f"HTTP response for /suggest to user {user_id}: status={http_response.status_code}, body={http_response.text}")
            http_response.raise_for_status()
        sent_message = await update.message.reply_text(response, parse_mode="Markdown")
        logger.info(f"Sent /suggest response to user {user_id}: {choice}, message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in /suggest for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in /suggest for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send /suggest response to user {user_id}: {e}")

async def region_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /region from user {user_id} with args: {context.args}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
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
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response, "parse_mode": "Markdown"}
                    )
                    logger.info(f"HTTP response for /region to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /region response to user {user_id}: {region}, message_id={sent_message.message_id}")
            else:
                response = f"Không tìm thấy vùng '{user_input}'. Thử 'Hà Nội', 'Sài Gòn', v.v."
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response}
                    )
                    logger.info(f"HTTP response for /region not found to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response)
                logger.info(f"Sent /region not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /region [tên vùng], ví dụ: /region Hà Nội"
            async with httpx.AsyncClient() as client:
                http_response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": response}
                )
                logger.info(f"HTTP response for /region usage to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                http_response.raise_for_status()
            sent_message = await update.message.reply_text(response)
            logger.info(f"Sent /region usage response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in /region for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in /region for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send /region response to user {user_id}: {e}")

async def ingredient_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /ingredient from user {user_id} with args: {context.args}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
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
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response, "parse_mode": "Markdown"}
                    )
                    logger.info(f"HTTP response for /ingredient to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent /ingredient response to user {user_id}: {choice}, message_id={sent_message.message_id}")
            else:
                response = "Không tìm thấy món phù hợp với nguyên liệu. Thử lại!"
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response}
                    )
                    logger.info(f"HTTP response for /ingredient not found to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response)
                logger.info(f"Sent /ingredient not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /ingredient [nguyên liệu1, nguyên liệu2], ví dụ: /ingredient thịt bò, rau thơm"
            async with httpx.AsyncClient() as client:
                http_response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": response}
                )
                logger.info(f"HTTP response for /ingredient usage to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                http_response.raise_for_status()
            sent_message = await update.message.reply_text(response)
            logger.info(f"Sent /ingredient usage response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in /ingredient for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in /ingredient for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send /ingredient response to user {user_id}: {e}")

async def location_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"Received /location from user {user_id}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
        response = "Chia sẻ vị trí của bạn để tôi gợi ý món địa phương (chỉ dùng để gợi ý, không lưu)."
        async with httpx.AsyncClient() as client:
            http_response = await client.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": response}
            )
            logger.info(f"HTTP response for /location to user {user_id}: status={http_response.status_code}, body={http_response.text}")
            http_response.raise_for_status()
        sent_message = await update.message.reply_text(response)
        logger.info(f"Sent /location response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in /location for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in /location for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send /location response to user {user_id}: {e}")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    location = update.message.location
    logger.info(f"Received location from user {user_id}: {location.latitude if location else None}, {location.longitude if location else None}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
        if location:
            region = "Sài Gòn"  # Giả lập, cần API geocode để thực tế
            foods = REGIONAL_FOODS.get(region, [])
            if foods:
                response = f"Dựa trên vị trí, vùng gần: *{region}*. Món gợi ý: {', '.join(foods)}"
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response, "parse_mode": "Markdown"}
                    )
                    logger.info(f"HTTP response for location-based to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response, parse_mode="Markdown")
                logger.info(f"Sent location-based response to user {user_id}: {region}, message_id={sent_message.message_id}")
            else:
                response = "Không tìm thấy vùng gần vị trí của bạn."
                async with httpx.AsyncClient() as client:
                    http_response = await client.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": response}
                    )
                    logger.info(f"HTTP response for location not found to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                    http_response.raise_for_status()
                sent_message = await update.message.reply_text(response)
                logger.info(f"Sent location not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Vui lòng chia sẻ position."
            async with httpx.AsyncClient() as client:
                http_response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": response}
                )
                logger.info(f"HTTP response for location request to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                http_response.raise_for_status()
            sent_message = await update.message.reply_text(response)
            logger.info(f"Sent location request response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in handle_location for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in handle_location for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send location response to user {user_id}: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    text = update.message.text.lower()
    logger.info(f"Received text '{text}' from user {user_id}")
    try:
        # Check chat permissions
        chat = await context.bot.get_chat(chat_id)
        logger.info(f"Chat permissions for user {user_id}: {chat}")
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
            async with httpx.AsyncClient() as client:
                http_response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": response}
                )
                logger.info(f"HTTP response for echo to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                http_response.raise_for_status()
            sent_message = await update.message.reply_text(response)
            logger.info(f"Sent echo response to user {user_id}: {text}, message_id={sent_message.message_id}")
        else:
            response = "Mình chưa có thông tin món này. Thử /suggest để gợi ý mới!"
            async with httpx.AsyncClient() as client:
                http_response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": response}
                )
                logger.info(f"HTTP response for echo not found to user {user_id}: status={http_response.status_code}, body={http_response.text}")
                http_response.raise_for_status()
            sent_message = await update.message.reply_text(response)
            logger.info(f"Sent echo not found response to user {user_id}: message_id={sent_message.message_id}")
    except TelegramError as te:
        logger.error(f"Telegram error in echo for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except httpx.HTTPStatusError as he:
        logger.error(f"HTTP error in echo for user {user_id}: status={he.response.status_code}, body={he.response.text}")
    except Exception as e:
        logger.error(f"Failed to send echo response to user {user_id}: {e}")

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
# Thay thế phần Flask app với cấu hình đúng cho Render
flask_app = Flask(__name__)

@flask_app.post("/webhook")
def webhook():
    try:
        # Nhận update từ Telegram
        update = Update.de_json(request.get_json(), application.bot)
        
        # Xử lý update bất đồng bộ
        asyncio.run_coroutine_threadsafe(
            application.process_update(update), 
            asyncio.get_event_loop()
        )
        return "ok", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "Error", 500

@flask_app.get("/")
def index():
    return "Alfred Food Bot is running!", 200
    
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
    
    # Thay thế hàm set_webhook
async def set_webhook():
    try:
        # Xóa webhook cũ trước
        await application.bot.delete_webhook()
        
        # Đặt webhook mới
        await application.bot.set_webhook(
            url=f"{WEBHOOK_URL}/webhook",
            allowed_updates=["message", "callback_query"]
        )
        logger.info(f"Webhook set to: {WEBHOOK_URL}/webhook")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        raise
    
    logger.info("Starting bot and setting webhook...")
    asyncio.get_event_loop().run_until_complete(set_webhook())
    logger.info("Starting Flask server...")
    flask_app.run(host="0.0.0.0", port=PORT)
