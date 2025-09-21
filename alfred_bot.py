import os
import logging
import random
import asyncio
import urllib.parse
import pg8000.native
import sqlite3
import time
import math
from datetime import datetime
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.error import TelegramError
from foods_data import VIETNAMESE_FOODS, REGIONAL_FOODS, HOLIDAYS
import unicodedata
from geopy.geocoders import Nominatim

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

logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")
logger.info(f"DATABASE_URL: {'Set' if DATABASE_URL else 'Not set'}")
logger.info(f"PORT: {PORT}")
logger.info(f"TOKEN: {'Set (hidden for security)' if TOKEN else 'Not set'}")
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables")

# Hàm chuẩn hóa không dấu
def normalize_no_diacritics(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower()

# Hàm Levenshtein
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

# Hàm Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Ánh xạ tọa độ thành vùng bằng geopy
geolocator = Nominatim(user_agent="alfred_bot_v1")
def get_region_from_coordinates(latitude, longitude):
    try:
        location = geolocator.reverse((latitude, longitude), language='vi', timeout=10)
        if location:
            address = location.address.split(',')
            region = address[-3].strip() if len(address) > 3 else address[-2].strip()
            return normalize_no_diacritics(region)
        return "Unknown"
    except Exception as e:
        logger.error(f"Geopy error: {e}")
        return "Unknown"

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
                self.pg_conn.run("CREATE TABLE IF NOT EXISTS favorite_foods (user_id TEXT, food TEXT, timestamp INTEGER)")
                self.pg_conn.run("CREATE TABLE IF NOT EXISTS restaurants (user_id TEXT, name TEXT, latitude REAL, longitude REAL, review TEXT, rating INTEGER, timestamp INTEGER)")
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
            self.sqlite_conn.execute("CREATE TABLE IF NOT EXISTS favorite_foods (user_id TEXT, food TEXT, timestamp INTEGER)")
            self.sqlite_conn.execute("CREATE TABLE IF NOT EXISTS restaurants (user_id TEXT, name TEXT, latitude REAL, longitude REAL, review TEXT, rating INTEGER, timestamp INTEGER)")
            self.sqlite_conn.commit()
            logger.info("Connected to SQLite successfully")
        except sqlite3.Error as e:
            logger.error(f"SQLite connection error: {e}")
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
            logger.info(f"Added food {food} to eaten_foods for user {user_id}")
        except Exception as e:
            logger.error(f"DB add eaten error: {e}")

    def get_eaten(self, user_id):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                rows = conn.run("SELECT food FROM eaten_foods WHERE user_id=:u ORDER BY timestamp DESC LIMIT 10", u=user_id)
                return [r[0] for r in rows]
            else:
                cursor = conn.execute("SELECT food FROM eaten_foods WHERE user_id=? ORDER BY timestamp DESC LIMIT 10", (user_id,))
                return [r[0] for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"DB get eaten error: {e}")
            return []

    def add_favorite(self, user_id, food):
        conn = self.get_conn()
        try:
            timestamp = int(time.time())
            if self.use_postgres:
                conn.run("INSERT INTO favorite_foods (user_id, food, timestamp) VALUES (:u, :f, :t)", u=user_id, f=food, t=timestamp)
            else:
                conn.execute("INSERT INTO favorite_foods (user_id, food, timestamp) VALUES (?, ?, ?)", (user_id, food, timestamp))
                conn.commit()
            logger.info(f"Added food {food} to favorite_foods for user {user_id}")
        except Exception as e:
            logger.error(f"DB add favorite error: {e}")

    def get_favorites(self, user_id):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                rows = conn.run("SELECT food FROM favorite_foods WHERE user_id=:u ORDER BY timestamp DESC LIMIT 10", u=user_id)
                return [r[0] for r in rows]
            else:
                cursor = conn.execute("SELECT food FROM favorite_foods WHERE user_id=? ORDER BY timestamp DESC LIMIT 10", (user_id,))
                return [r[0] for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"DB get favorites error: {e}")
            return []

    def delete_favorite(self, user_id, food):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                conn.run("DELETE FROM favorite_foods WHERE user_id=:u AND food=:f", u=user_id, f=food)
            else:
                conn.execute("DELETE FROM favorite_foods WHERE user_id=? AND food=?", (user_id, food))
                conn.commit()
            logger.info(f"Deleted food {food} from favorite_foods for user {user_id}")
        except Exception as e:
            logger.error(f"DB delete favorite error: {e}")

    def add_restaurant(self, user_id, name, latitude, longitude, review, rating):
        conn = self.get_conn()
        try:
            timestamp = int(time.time())
            if self.use_postgres:
                conn.run(
                    "INSERT INTO restaurants (user_id, name, latitude, longitude, review, rating, timestamp) "
                    "VALUES (:u, :n, :lat, :lon, :r, :rat, :t)",
                    u=user_id, n=name, lat=latitude, lon=longitude, r=review, rat=rating, t=timestamp
                )
            else:
                conn.execute(
                    "INSERT INTO restaurants (user_id, name, latitude, longitude, review, rating, timestamp) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, name, latitude, longitude, review, rating, timestamp)
                )
                conn.commit()
            logger.info(f"Added restaurant {name} for user {user_id}")
        except Exception as e:
            logger.error(f"DB add restaurant error: {e}")

    def get_user_restaurants(self, user_id):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                rows = conn.run("SELECT name, latitude, longitude, review, rating FROM restaurants WHERE user_id=:u ORDER BY timestamp DESC", u=user_id)
                return [dict(name=r[0], latitude=r[1], longitude=r[2], review=r[3], rating=r[4]) for r in rows]
            else:
                cursor = conn.execute("SELECT name, latitude, longitude, review, rating FROM restaurants WHERE user_id=? ORDER BY timestamp DESC", (user_id,))
                return [dict(name=r[0], latitude=r[1], longitude=r[2], review=r[3], rating=r[4]) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"DB get user restaurants error: {e}")
            return []

    def get_all_restaurants(self):
        conn = self.get_conn()
        try:
            if self.use_postgres:
                rows = conn.run("SELECT user_id, name, latitude, longitude, review, rating FROM restaurants ORDER BY timestamp DESC")
                return [dict(user_id=r[0], name=r[1], latitude=r[2], longitude=r[3], review=r[4], rating=r[5]) for r in rows]
            else:
                cursor = conn.execute("SELECT user_id, name, latitude, longitude, review, rating FROM restaurants ORDER BY timestamp DESC")
                return [dict(user_id=r[0], name=r[1], latitude=r[2], longitude=r[3], review=r[4], rating=r[5]) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"DB get all restaurants error: {e}")
            return []

db = Database()

# States cho ConversationHandler
NAME, REVIEW, RATING = range(3)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 START HANDLER for user {user_id} in chat {chat_id}")
    try:
        response = (
            "Xin chào! Tôi là quản gia *Alfred Vị Việt* 🇻🇳\n"
            "Tôi sẽ giúp bạn khám phá món ăn ngon và quán ăn tuyệt vời!\n\n"
            "📖 *Danh sách lệnh:*\n"
            "- /suggest [khô/nước]: Gợi ý món ăn ngẫu nhiên.\n"
            "- /region [tên vùng]: Gợi ý món theo vùng (VD: Hà Nội).\n"
            "- /ingredient [nguyên liệu]: Tìm món từ nguyên liệu (VD: thịt bò).\n"
            "- /location: Gợi ý món theo vị trí GPS.\n"
            "- /holiday [dịp lễ]: Gợi ý món theo dịp (VD: Tết Nguyên Đán).\n"
            "- /save [món]: Lưu món yêu thích.\n"
            "- /favorites: Xem món yêu thích.\n"
            "- /restaurant: Xem quán ăn bạn và người khác đã lưu.\n"
            "- /myrestaurants: Xem quán ăn bạn đã lưu.\n"
            "- /donate: Ủng hộ bot.\n"
            "- Gửi tên món: Tra chi tiết món (hỗ trợ không dấu, VD: pho)."
        )
        keyboard = [
            [InlineKeyboardButton("Gợi ý món ngay! 🍲", callback_data="suggest")],
            [InlineKeyboardButton("Ủng hộ bot ❤️", url="https://viettelmoney.go.link/fuCfu")],
            #[InlineKeyboardButton("Donate qua Viettel Money", url="https://viettelmoney.go.link/fuCfu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
            timeout=30.0
        )
        logger.info(f"✅ Sent /start response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT sending /start to user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /start for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send /start response to user {user_id}: {e}")

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 SUGGEST HANDLER for user {user_id} with args: {context.args}")
    try:
        food_type = None
        if context.args:
            food_type = normalize_no_diacritics(' '.join(context.args))
            if food_type not in ['kho', 'nuoc']:
                food_type = None
                response = "Vui lòng chọn 'khô' hoặc 'nước'. Ví dụ: /suggest khô"
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response),
                    timeout=30.0
                )
                logger.info(f"✅ Sent suggest type error response to user {user_id}: message_id={sent_message.message_id}")
                return
        
        eaten_foods = db.get_eaten(user_id)
        available_foods = [
            food for food, info in VIETNAMESE_FOODS.items()
            if food not in eaten_foods and (not food_type or info['type'] == ('Khô' if food_type == 'kho' else 'Nước'))
        ]
        
        if available_foods:
            food = random.choice(available_foods)
            food_info = VIETNAMESE_FOODS[food]
            db.add_eaten(user_id, food)
            response = (
                f"🍲 *Đề xuất món: {food}*\n"
                f"- Loại: {food_info['type']}\n"
                f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
                f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
                f"- Dịp: {', '.join(food_info['holidays'])}\n"
                f"- Calo ước tính: {food_info['calories']}"
            )
            keyboard = [
                [InlineKeyboardButton("📖 Xem cách làm", callback_data=f"recipe_{food}")],
                [InlineKeyboardButton("💾 Lưu món này", callback_data=f"save_{food}")],
                [InlineKeyboardButton("🔄 Gợi ý món khác", callback_data="suggest")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                timeout=30.0
            )
            logger.info(f"✅ Sent suggest response to user {user_id}: {food}, message_id={sent_message.message_id}")
        else:
            response = "😔 Không còn món mới để gợi ý! Thử /favorites hoặc gửi tên món để xem chi tiết."
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent no foods response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /suggest for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /suggest for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send suggest response to user {user_id}: {e}")

async def region_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 REGION HANDLER for user {user_id} with args: {context.args}")
    try:
        if context.args:
            user_input = normalize_no_diacritics(' '.join(context.args))
            normalized_regions = {normalize_no_diacritics(r): r for r in REGIONAL_FOODS.keys()}
            best_match = min(normalized_regions.keys(), key=lambda k: levenshtein_distance(user_input, k))
            distance = levenshtein_distance(user_input, best_match)
            if distance <= 3:
                region = normalized_regions[best_match]
                foods = REGIONAL_FOODS.get(region, [])
                if foods:
                    response = f"🌏 Món ăn phổ biến tại *{region}*: {', '.join(foods)}"
                    keyboard = [[InlineKeyboardButton(food, callback_data=f"recipe_{food}")] for food in foods[:5]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                else:
                    response = f"😔 Không tìm thấy món ăn cho vùng *{region}*."
                    reply_markup = None
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                    timeout=30.0
                )
                logger.info(f"✅ Sent region response to user {user_id}: {region}, message_id={sent_message.message_id}")
            else:
                response = f"😔 Không tìm thấy vùng '{ ' '.join(context.args) }'. Thử 'Hà Nội', 'Sài Gòn', 'Huế' (hỗ trợ không dấu)."
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent region not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /region [tên vùng], ví dụ: /region Hà Nội hoặc ha noi"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent region usage response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /region for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /region for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send region response to user {user_id}: {e}")

async def ingredient_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 INGREDIENT HANDLER for user {user_id} with args: {context.args}")
    try:
        if context.args:
            raw_input = ' '.join(context.args)
            if ',' in raw_input:
                raw_ingredients = raw_input.split(',')
            else:
                raw_ingredients = [raw_input]
            ingredients = [normalize_no_diacritics(ing.strip()) for ing in raw_ingredients]
            matching_foods = []
            for food, info in VIETNAMESE_FOODS.items():
                food_ingredients_str = ' '.join([normalize_no_diacritics(i) for i in info['ingredients']])
                if all(ing in food_ingredients_str for ing in ingredients):
                    matching_foods.append(food)
            if matching_foods:
                display_ingredients = raw_input
                response = f"🥗 Món ăn với nguyên liệu *{display_ingredients}*: {', '.join(matching_foods)}"
                keyboard = [[InlineKeyboardButton(food, callback_data=f"recipe_{food}")] for food in matching_foods[:5]]
                reply_markup = InlineKeyboardMarkup(keyboard)
            else:
                response = f"😔 Không tìm thấy món ăn với nguyên liệu: *{raw_input}*."
                reply_markup = None
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                timeout=30.0
            )
            logger.info(f"✅ Sent ingredient response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /ingredient [nguyên liệu], ví dụ: /ingredient thịt bò, rau thơm hoặc thit bo"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent ingredient usage response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /ingredient for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /ingredient for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send ingredient response to user {user_id}: {e}")

async def location_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 LOCATION HANDLER for user {user_id} with args: {context.args}")
    try:
        response = "📍 Vui lòng chia sẻ vị trí GPS bằng nút 'Location' hoặc gửi tọa độ (VD: 10.7769,106.7009)."
        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
            timeout=30.0
        )
        logger.info(f"✅ Sent location prompt response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /location for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /location for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send location prompt response to user {user_id}: {e}")

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 SAVE HANDLER for user {user_id} with args: {context.args}")
    try:
        if context.args:
            user_input = normalize_no_diacritics(' '.join(context.args))
            normalized_foods = {normalize_no_diacritics(food): food for food in VIETNAMESE_FOODS.keys()}
            best_match = min(normalized_foods.keys(), key=lambda k: levenshtein_distance(user_input, k))
            distance = levenshtein_distance(user_input, best_match)
            if distance <= 3:
                food = normalized_foods[best_match]
                db.add_favorite(user_id, food)
                response = f"💾 Đã lưu *{food}* vào danh sách yêu thích!"
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent save response to user {user_id}: {food}, message_id={sent_message.message_id}")
            else:
                response = f"😔 Món '{ ' '.join(context.args) }' không tìm thấy. Thử /suggest hoặc gửi tên món khác (hỗ trợ không dấu)."
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent save not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /save [tên món], ví dụ: /save Phở hoặc pho"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent save usage response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /save for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /save for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send save response to user {user_id}: {e}")

async def favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 FAVORITES HANDLER for user {user_id}")
    try:
        favorite_foods = db.get_favorites(user_id)
        if favorite_foods:
            response = "❤️ Món ăn yêu thích của bạn:\n" + "\n".join(f"- {food}" for food in favorite_foods)
            keyboard = []
            for food in favorite_foods:
                keyboard.append([
                    InlineKeyboardButton(f"📖 {food}", callback_data=f"recipe_{food}"),
                    InlineKeyboardButton(f"🗑 Xoá", callback_data=f"delete_favorite_{food}")
                ])
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            response = "😔 Bạn chưa có món ăn yêu thích nào. Thử /save [tên món] để lưu!"
            reply_markup = None
        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
            timeout=30.0
        )
        logger.info(f"✅ Sent favorites response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /favorites for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /favorites for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send favorites response to user {user_id}: {e}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 DONATE HANDLER for user {user_id}")
    try:
        response = (
            "❤️ Cảm ơn bạn đã sử dụng *Alfred Vị Việt*! \n"
            "Nếu bạn thấy bot hữu ích, hãy ủng hộ mình để duy trì và phát triển nhé!\n"
            "Chọn phương thức donate bên dưới:"
        )
        keyboard = [
            #[InlineKeyboardButton("💸 PayPal", url="https://paypal.me/alfredfoodbot")],
            [InlineKeyboardButton("💳 Viettel Money", url="https://viettelmoney.go.link/fuCfu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
            timeout=30.0
        )
        logger.info(f"✅ Sent donate response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /donate for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /donate for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send donate response to user {user_id}: {e}")

async def holiday_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 HOLIDAY HANDLER for user {user_id} with args: {context.args}")
    try:
        if context.args:
            user_input = normalize_no_diacritics(' '.join(context.args))
            normalized_holidays = {normalize_no_diacritics(key): key for key in HOLIDAYS.keys()}
            best_match = min(normalized_holidays.keys(), key=lambda k: levenshtein_distance(user_input, k))
            distance = levenshtein_distance(user_input, best_match)
            if distance <= 3:
                holiday = normalized_holidays[best_match]
                matching_foods = [food for food, info in VIETNAMESE_FOODS.items() if holiday in info['holidays']]
                if matching_foods:
                    response = f"🎉 Món ăn phù hợp cho *{holiday}*: {', '.join(matching_foods)}"
                    keyboard = [[InlineKeyboardButton(food, callback_data=f"recipe_{food}")] for food in matching_foods[:5]]
                    keyboard.append([InlineKeyboardButton("🔄 Gợi ý món khác", callback_data="suggest")])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                else:
                    response = f"😔 Không có món ăn nào đặc trưng cho *{holiday}*."
                    reply_markup = None
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                    timeout=30.0
                )
                logger.info(f"✅ Sent holiday response to user {user_id}: {holiday}, message_id={sent_message.message_id}")
            else:
                response = f"😔 Không tìm thấy ngày lễ '{ ' '.join(context.args) }'. Thử 'Tết Nguyên Đán', 'Trung Thu' (hỗ trợ không dấu)."
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent holiday not found response to user {user_id}: message_id={sent_message.message_id}")
        else:
            response = "Sử dụng: /holiday [tên ngày lễ], ví dụ: /holiday Tết Nguyên Đán hoặc tet nguyen dan"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent holiday usage response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /holiday for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /holiday for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send holiday response to user {user_id}: {e}")

async def restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 RESTAURANT HANDLER for user {user_id}")
    try:
        # Lấy danh sách quán ăn của người dùng hiện tại
        user_restaurants = db.get_user_restaurants(user_id)
        # Lấy tất cả quán ăn từ database
        all_restaurants = db.get_all_restaurants()
        # Lọc danh sách quán ăn của người dùng khác
        other_restaurants = [r for r in all_restaurants if r['user_id'] != user_id]

        response = "🏪 *Danh sách quán ăn*\n\n"
        
        # Hiển thị quán ăn của người dùng
        if user_restaurants:
            response += "🍽 *Quán ăn bạn đã lưu:*\n"
            for r in user_restaurants[:5]:  # Giới hạn 5 quán để tránh quá dài
                map_link = f"https://www.google.com/maps/search/?api=1&query={r['latitude']},{r['longitude']}"
                response += (
                    f"- *{r['name']}* ({r['rating']} ⭐)\n"
                    f"  Đánh giá: {r['review']}\n"
                    f"  Vị trí: **{r['latitude']:.4f}, {r['longitude']:.4f}** ([Bản đồ]({map_link}))\n"
                )
        else:
            response += "😔 Bạn chưa lưu quán ăn nào. Gửi vị trí GPS và chọn 'Lưu quán ăn' để bắt đầu!\n"

        # Hiển thị quán ăn của người dùng khác
        if other_restaurants:
            response += "\n🌐 *Quán ăn từ người dùng khác:*\n"
            for r in other_restaurants[:5]:  # Giới hạn 5 quán để tránh quá dài
                map_link = f"https://www.google.com/maps/search/?api=1&query={r['latitude']},{r['longitude']}"
                response += (
                    f"- *{r['name']}* ({r['rating']} ⭐)\n"
                    f"  Đánh giá: {r['review']}\n"
                    f"  Vị trí: **{r['latitude']:.4f}, {r['longitude']:.4f}** ([Bản đồ]({map_link}))\n"
                )
        else:
            response += "\n🌐 *Quán ăn từ người dùng khác:* Chưa có quán nào được lưu bởi người khác."

        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", disable_web_page_preview=True),
            timeout=30.0
        )
        logger.info(f"✅ Sent restaurant response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /restaurant for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /restaurant for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send restaurant response to user {user_id}: {e}")

async def my_restaurants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    logger.info(f"🎯 MY_RESTAURANTS HANDLER for user {user_id}")
    try:
        restaurants = db.get_user_restaurants(user_id)
        if restaurants:
            response = "🍽 *Quán ăn bạn đã lưu:*\n"
            for r in restaurants[:5]:
                map_link = f"https://www.google.com/maps/search/?api=1&query={r['latitude']},{r['longitude']}"
                response += (
                    f"- *{r['name']}* ({r['rating']} ⭐)\n"
                    f"  Đánh giá: {r['review']}\n"
                    f"  Vị trí: **{r['latitude']:.4f}, {r['longitude']:.4f}** ([Bản đồ]({map_link}))\n"
                )
        else:
            response = "😔 Bạn chưa lưu quán ăn nào. Gửi vị trí GPS và chọn 'Lưu quán ăn' để bắt đầu!"
        sent_message = await asyncio.wait_for(
            context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", disable_web_page_preview=True),
            timeout=30.0
        )
        logger.info(f"✅ Sent myrestaurants response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in /myrestaurants for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in /myrestaurants for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send myrestaurants response to user {user_id}: {e}")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    location = update.message.location
    logger.info(f"🎯 HANDLE LOCATION for user {user_id}: {location.latitude if location else None}, {location.longitude if location else None}")
    try:
        if location:
            latitude, longitude = location.latitude, location.longitude
            context.user_data['location'] = (latitude, longitude)
            region = get_region_from_coordinates(latitude, longitude)
            foods = REGIONAL_FOODS.get(region, REGIONAL_FOODS.get("Sài Gòn", []))
            response = f"📍 Vị trí ({latitude:.4f}, {longitude:.4f}), vùng gần: *{region}*.\nMón gợi ý: {', '.join(foods[:5])}" if foods else f"📍 Vùng: *{region}*. Không tìm thấy món."
            keyboard = [
                [InlineKeyboardButton("🍲 Giới thiệu món", callback_data="suggest")],
                [InlineKeyboardButton("💾 Lưu quán ăn", callback_data="start_save_restaurant")],
                [InlineKeyboardButton("🏪 Xem quán gần", callback_data="nearby_restaurants")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                timeout=30.0
            )
            logger.info(f"✅ Sent location response to user {user_id}: {region}, message_id={sent_message.message_id}")
        else:
            response = "📍 Vui lòng chia sẻ vị trí GPS bằng nút 'Location'."
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent location request response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in handle_location for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in handle_location for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send location response to user {user_id}: {e}")

async def start_save_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if 'location' not in context.user_data:
        await query.edit_message_text("📍 Gửi vị trí GPS trước để lưu quán.")
        return ConversationHandler.END
    await query.edit_message_text("🏪 Nhập tên quán ăn:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['restaurant_name'] = update.message.text
    await update.message.reply_text("📝 Nhập đánh giá về quán ăn:")
    return REVIEW

async def get_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['restaurant_review'] = update.message.text
    await update.message.reply_text("⭐ Nhập số sao (1-5):")
    return RATING

async def get_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        rating = int(update.message.text)
        if 1 <= rating <= 5:
            user_id = str(update.effective_user.id)
            name = context.user_data['restaurant_name']
            review = context.user_data['restaurant_review']
            latitude, longitude = context.user_data['location']
            db.add_restaurant(user_id, name, latitude, longitude, review, rating)
            await update.message.reply_text(f"✅ Đã lưu quán *{name}* với đánh giá {rating} sao!", parse_mode="Markdown")
            context.user_data.clear()
            return ConversationHandler.END
        else:
            await update.message.reply_text("⭐ Số sao phải từ 1 đến 5. Vui lòng nhập lại.")
            return RATING
    except ValueError:
        await update.message.reply_text("🔢 Vui lòng nhập số từ 1 đến 5.")
        return RATING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Hủy lưu quán ăn.")
    context.user_data.clear()
    return ConversationHandler.END

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"🎯 ECHO HANDLER for user {user_id}: {text}")
    try:
        normalized_input = normalize_no_diacritics(text)
        normalized_foods = {normalize_no_diacritics(food): food for food in VIETNAMESE_FOODS.keys()}
        best_match = min(normalized_foods.keys(), key=lambda k: levenshtein_distance(normalized_input, k))
        distance = levenshtein_distance(normalized_input, best_match)
        if distance <= 3:
            food = normalized_foods[best_match]
            food_info = VIETNAMESE_FOODS[food]
            response = (
                f"🍲 *{food}* là món ăn nổi tiếng!\n"
                f"- Loại: {food_info['type']}\n"
                f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
                f"- Cách làm: {food_info['recipe']}\n"
                f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
                f"- Dịp: {', '.join(food_info['holidays'])}\n"
                f"- Calo ước tính: {food_info['calories']}"
            )
            keyboard = [
                [InlineKeyboardButton("💾 Lưu món này", callback_data=f"save_{food}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                timeout=30.0
            )
            logger.info(f"✅ Sent echo response to user {user_id}: {food}, message_id={sent_message.message_id}")
        else:
            response = f"😔 Món '{text}' chưa có trong danh sách. Thử /suggest để gợi ý mới! (Hỗ trợ không dấu, ví dụ: 'pho')"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent echo not found response to user {user_id}: message_id={sent_message.message_id}")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in echo for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in echo for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to send echo response to user {user_id}: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    chat_id = query.message.chat_id
    data = query.data
    logger.info(f"🎯 BUTTON CALLBACK for user {user_id}: {data}")
    try:
        await query.answer()
        if data.startswith("recipe_"):
            food = data.replace("recipe_", "")
            if food in VIETNAMESE_FOODS:
                food_info = VIETNAMESE_FOODS[food]
                response = f"📖 Cách làm *{food}*: {food_info['recipe']}"
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent recipe response to user {user_id}: {food}, message_id={sent_message.message_id}")
        elif data.startswith("save_"):
            food = data.replace("save_", "")
            if food in VIETNAMESE_FOODS:
                db.add_favorite(user_id, food)
                response = f"💾 Đã lưu *{food}* vào danh sách yêu thích!"
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent save response to user {user_id}: {food}, message_id={sent_message.message_id}")
        elif data.startswith("delete_favorite_"):
            food = data.replace("delete_favorite_", "")
            db.delete_favorite(user_id, food)
            response = f"🗑 Đã xoá *{food}* khỏi danh sách yêu thích!"
            sent_message = await asyncio.wait_for(
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                timeout=30.0
            )
            logger.info(f"✅ Sent delete favorite response to user {user_id}: {food}, message_id={sent_message.message_id}")
            await favorites(update, context)
        elif data == "suggest":
            eaten_foods = db.get_eaten(user_id)
            available_foods = [food for food in VIETNAMESE_FOODS.keys() if food not in eaten_foods]
            if available_foods:
                food = random.choice(available_foods)
                food_info = VIETNAMESE_FOODS[food]
                db.add_eaten(user_id, food)
                response = (
                    f"🍲 Đề xuất món: *{food}*\n"
                    f"- Loại: {food_info['type']}\n"
                    f"- Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
                    f"- Phổ biến tại: {', '.join(food_info['popular_regions'])}\n"
                    f"- Dịp: {', '.join(food_info['holidays'])}\n"
                    f"- Calo ước tính: {food_info['calories']}"
                )
                keyboard = [
                    [InlineKeyboardButton("📖 Xem cách làm", callback_data=f"recipe_{food}")],
                    [InlineKeyboardButton("💾 Lưu món này", callback_data=f"save_{food}")],
                    [InlineKeyboardButton("🔄 Gợi ý món khác", callback_data="suggest")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown", reply_markup=reply_markup),
                    timeout=30.0
                )
                logger.info(f"✅ Sent button suggest response to user {user_id}: {food}, message_id={sent_message.message_id}")
            else:
                response = "😔 Không còn món mới để gợi ý! Thử /favorites hoặc gửi tên món."
                sent_message = await asyncio.wait_for(
                    context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown"),
                    timeout=30.0
                )
                logger.info(f"✅ Sent no foods response to user {user_id}: message_id={sent_message.message_id}")
        elif data == "start_save_restaurant":
            return await start_save_restaurant(update, context)
        elif data == "nearby_restaurants":
            if 'location' in context.user_data:
                latitude, longitude = context.user_data['location']
                all_rest = db.get_all_restaurants()
                nearby = []
                for r in all_rest:
                    dist = haversine(latitude, longitude, r['latitude'], r['longitude'])
                    if dist <= 1:
                        nearby.append((r, dist))
                nearby.sort(key=lambda x: x[1])
                if nearby:
                    response = "🏪 Quán gần (<1km):\n" + "\n".join(
                        f"- *{r['name']}* ({round(dist, 2)}km, {r['rating']} ⭐)\n"
                        f"  Đánh giá: {r['review']}\n"
                        f"  Vị trí: **{r['latitude']:.4f}, {r['longitude']:.4f}** ([Bản đồ](https://www.google.com/maps/search/?api=1&query={r['latitude']},{r['longitude']}))"
                        for r, dist in nearby[:5]
                    )
                else:
                    response = "😔 Không có quán nào trong 1km."
                await query.edit_message_text(response, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                await query.edit_message_text("📍 Gửi vị trí GPS trước.")
    except asyncio.TimeoutError:
        logger.error(f"❌ TIMEOUT in button_callback for user {user_id}")
    except TelegramError as te:
        logger.error(f"❌ Telegram error in button_callback for user {user_id}: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
    except Exception as e:
        logger.error(f"❌ Failed to handle button_callback for user {user_id}: {e}")

# ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_save_restaurant, pattern="^start_save_restaurant$")],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_review)],
        RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rating)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=False
)

# Build Application
try:
    logger.info("Building Telegram application...")
    application = ApplicationBuilder().token(TOKEN).http_version("1.1").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("suggest", suggest))
    application.add_handler(CommandHandler("region", region_suggest))
    application.add_handler(CommandHandler("ingredient", ingredient_suggest))
    application.add_handler(CommandHandler("location", location_suggest))
    application.add_handler(CommandHandler("save", save))
    application.add_handler(CommandHandler("favorites", favorites))
    application.add_handler(CommandHandler("donate", donate))
    application.add_handler(CommandHandler("holiday", holiday_suggest))
    application.add_handler(CommandHandler("restaurant", restaurant))
    application.add_handler(CommandHandler("myrestaurants", my_restaurants))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button_callback))
    logger.info("Application built successfully with handlers: start, suggest, region, ingredient, location, save, favorites, donate, holiday, restaurant, myrestaurants, location_message, echo, button_callback")
except Exception as e:
    logger.error(f"Failed to build application: {e}")
    raise

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
            logger.info(f"Parsed update: update_id={update.update_id}, message={update.message.text if update.message else None}")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(application.process_update(update))
            logger.info(f"Processed update: {update.update_id}")
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
    return "Alfred Vị Việt running!", 200

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
        except TelegramError as te:
            logger.error(f"Failed to set webhook: {te.message} (code={getattr(te, 'status_code', 'unknown')})")
            raise
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            raise
    
    logger.info("Starting bot and setting webhook...")
    asyncio.get_event_loop().run_until_complete(set_webhook())
    logger.info("Starting Flask server...")
    flask_app.run(host="0.0.0.0", port=PORT)
