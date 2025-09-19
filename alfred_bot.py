import os
import logging
import random
import asyncio
import urllib.parse
import pg8000.native
import sqlite3
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Workaround for event loop closed bug
import anyio
anyio._backends._asyncio.TaskGroup.__init__ = lambda self, *args, **kwargs: None

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

# --------------------------------------------------------------------
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
                # Tạo bảng với cột timestamp
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
            # Tạo bảng với cột timestamp
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
            # Lưu món ăn với timestamp hiện tại (Unix timestamp)
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
                # Lấy 10 món gần nhất, sắp xếp theo timestamp giảm dần
                rows = conn.run("SELECT food FROM eaten_foods WHERE user_id=:u ORDER BY timestamp DESC LIMIT 10", u=user_id)
                return [r[0] for r in rows]
            else:
                # Lấy 10 món gần nhất, sắp xếp theo timestamp giảm dần
                rows = conn.execute("SELECT food FROM eaten_foods WHERE user_id=? ORDER BY timestamp DESC LIMIT 10", (user_id,))
                return [r[0] for r in rows.fetchall()]
        except Exception as e:
            logger.error(f"DB fetch error: {e}")
            return []

db = Database()

# --------------------------------------------------------------------
# ===== CƠ SỞ DỮ LIỆU MÓN ĂN ===== (Thêm calo cho tính năng dinh dưỡng)
VIETNAMESE_FOODS = {
    "phở": {
        "type": "nước",
        "category": "phở",
        "ingredients": ["bánh phở", "thịt bò/gà", "xương hầm", "hành", "rau thơm"],
        "recipe": "Hầm xương bò/gà làm nước dùng, thêm gia vị, thả bánh phở và thịt.",
        "popular_regions": ["Hà Nội", "Nam Định"],
        "holidays": ["Tết", "Ngày thường"],
        "calories": "600-800 kcal/phần"
    },
    "bún chả": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "thịt nướng", "nước mắm", "rau sống"],
        "recipe": "Nướng thịt, pha nước mắm chua ngọt, ăn kèm với bún và rau.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Bữa trưa"],
        "calories": "500-700 kcal/phần"
    },
    "bún đậu mắm tôm": {
        "type": "khô",
        "category": "bún",
        "ingredients": ["bún", "đậu phụ", "mắm tôm", "thịt luộc", "rau sống"],
        "recipe": "Chiên đậu, luộc thịt, pha mắm tôm, ăn kèm bún và rau.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Liên hoan", "Ăn chơi"],
        "calories": "700-900 kcal/phần"
    },
    "bánh cuốn": {
        "type": "khô",
        "category": "bánh",
        "ingredients": ["bột gạo", "thịt băm", "mộc nhĩ", "hành phi"],
        "recipe": "Tráng bột gạo mỏng, cuốn nhân thịt mộc nhĩ, ăn với nước mắm.",
        "popular_regions": ["Hà Nội", "Bắc Ninh"],
        "holidays": ["Bữa sáng"],
        "calories": "400-600 kcal/phần"
    },
    "cháo lòng": {
        "type": "nước",
        "category": "cháo",
        "ingredients": ["gạo", "lòng heo", "hành", "gia vị"],
        "recipe": "Nấu cháo từ gạo, thêm lòng heo, nêm gia vị vừa ăn.",
        "popular_regions": ["Bắc Bộ"],
        "holidays": ["Mọi dịp"],
        "calories": "500-700 kcal/phần"
    },
    "bánh đa cua": {
        "type": "nước",
        "category": "bánh đa",
        "ingredients": ["bánh đa", "cua đồng", "rau sống", "gia vị"],
        "recipe": "Nấu nước dùng từ cua đồng, thêm bánh đa và rau.",
        "popular_regions": ["Hải Phòng"],
        "holidays": ["Bữa trưa"],
        "calories": "600-800 kcal/phần"
    },
    "bún bò Huế": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "thịt bò", "giò heo", "mắm ruốc"],
        "recipe": "Hầm xương, nêm mắm ruốc, thêm bún và thịt.",
        "popular_regions": ["Huế"],
        "holidays": ["Tết", "Lễ hội"],
        "calories": "700-900 kcal/phần"
    },
    "cơm hến": {
        "type": "khô",
        "category": "cơm",
        "ingredients": ["cơm", "hến", "rau sống", "mắm ruốc"],
        "recipe": "Xào hến, trộn với cơm và rau, chan nước hến.",
        "popular_regions": ["Huế"],
        "holidays": ["Bữa thường ngày"],
        "calories": "400-600 kcal/phần"
    },
    "bánh bèo": {
        "type": "ăn vặt",
        "category": "bánh",
        "ingredients": ["bột gạo", "tôm khô", "mỡ hành", "nước mắm"],
        "recipe": "Hấp bột gạo trong chén nhỏ, rắc nhân tôm, chan nước mắm.",
        "popular_regions": ["Huế"],
        "holidays": ["Liên hoan"],
        "calories": "200-400 kcal/phần"
    },
    "mì quảng": {
        "type": "khô",
        "category": "mì",
        "ingredients": ["mì quảng", "thịt gà/heo/tôm", "rau sống", "đậu phộng"],
        "recipe": "Nấu nước dùng ít, chan vào mì, thêm rau, đậu phộng.",
        "popular_regions": ["Đà Nẵng", "Quảng Nam"],
        "holidays": ["Mọi dịp"],
        "calories": "600-800 kcal/phần"
    },
    "bánh xèo": {
        "type": "ăn vặt",
        "category": "bánh",
        "ingredients": ["bột gạo", "tôm", "thịt", "giá", "rau sống"],
        "recipe": "Đổ bột tráng mỏng, cho nhân, chiên giòn, ăn kèm rau và nước mắm.",
        "popular_regions": ["Miền Trung", "Miền Nam"],
        "holidays": ["Cuối tuần"],
        "calories": "700-900 kcal/phần"
    },
    "bún chả cá": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "chả cá", "rau", "gia vị"],
        "recipe": "Nấu nước dùng từ cá, thêm bún và chả cá.",
        "popular_regions": ["Đà Nẵng"],
        "holidays": ["Mọi dịp"],
        "calories": "500-700 kcal/phần"
    },
    "cao lầu": {
        "type": "khô",
        "category": "mì",
        "ingredients": ["sợi cao lầu", "thịt xá xíu", "rau sống", "da heo chiên"],
        "recipe": "Nấu sợi mì dai từ nước tro tàu, thêm thịt và rau.",
        "popular_regions": ["Hội An", "Quảng Nam"],
        "holidays": ["Du lịch"],
        "calories": "600-800 kcal/phần"
    },
    "cơm tấm": {
        "type": "khô",
        "category": "cơm",
        "ingredients": ["gạo tấm", "sườn nướng", "bì", "chả trứng"],
        "recipe": "Nấu cơm tấm, nướng sườn, ăn kèm bì chả.",
        "popular_regions": ["Sài Gòn"],
        "holidays": ["Mọi dịp"],
        "calories": "800-1000 kcal/phần"
    },
    "hủ tiếu": {
        "type": "nước",
        "category": "hủ tiếu",
        "ingredients": ["hủ tiếu", "thịt", "tôm", "trứng cút"],
        "recipe": "Nấu nước hầm xương, chan lên hủ tiếu.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Bữa sáng"],
        "calories": "600-800 kcal/phần"
    },
    "bánh mì": {
        "type": "khô",
        "category": "bánh mì",
        "ingredients": ["bánh mì", "pate", "thịt", "rau"],
        "recipe": "Nướng bánh mì, phết pate, thêm thịt và rau.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Bữa sáng"],
        "calories": "400-600 kcal/phần"
    },
    "gỏi cuốn": {
        "type": "ăn vặt",
        "category": "cuốn",
        "ingredients": ["bánh tráng", "tôm", "thịt", "bún", "rau sống"],
        "recipe": "Cuốn tôm thịt, bún và rau trong bánh tráng, chấm mắm nêm.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Ăn nhẹ"],
        "calories": "200-400 kcal/phần"
    },
    "bánh khọt": {
        "type": "ăn vặt",
        "category": "bánh",
        "ingredients": ["bột gạo", "tôm", "mỡ hành", "nước mắm"],
        "recipe": "Đổ bột vào khuôn nhỏ, thêm tôm, chiên giòn, ăn với rau.",
        "popular_regions": ["Vũng Tàu"],
        "holidays": ["Ăn chơi"],
        "calories": "500-700 kcal/phần"
    },
    "lẩu mắm": {
        "type": "nước",
        "category": "lẩu",
        "ingredients": ["mắm cá", "các loại cá", "rau", "bún"],
        "recipe": "Nấu mắm cá làm nước lẩu, ăn kèm bún và rau.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Sum họp"],
        "calories": "800-1000 kcal/phần"
    },
    "cá lóc nướng trui": {
        "type": "khô",
        "category": "cá",
        "ingredients": ["cá lóc", "muối", "rau sống", "nước mắm"],
        "recipe": "Nướng cá lóc bằng rơm, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Tiệc ngoài trời"],
        "calories": "400-600 kcal/phần"
    },
    "bún cá": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "cá", "rau thơm"],
        "recipe": "Nấu nước cá, chan lên bún.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Mọi dịp"],
        "calories": "500-700 kcal/phần"
    },
    "chè ba màu": {
        "type": "tráng miệng",
        "category": "chè",
        "ingredients": ["đậu xanh", "đậu đỏ", "rau câu", "nước cốt dừa"],
        "recipe": "Nấu chè nhiều lớp màu, chan nước cốt dừa, ăn kèm đá.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Mùa hè"],
        "calories": "300-500 kcal/phần"
    },
    "chè trôi nước": {
        "type": "tráng miệng",
        "category": "chè",
        "ingredients": ["bột nếp", "đậu xanh", "gừng", "đường"],
        "recipe": "Vo viên bột nếp nhân đậu xanh, luộc chín, chan nước gừng ngọt.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Tết Hàn Thực", "Ngày thường"],
        "calories": "300-500 kcal/phần"
    },
    "bánh canh": {
        "type": "nước",
        "category": "bánh canh",
        "ingredients": ["bánh canh", "tôm", "cá", "rau thơm"],
        "recipe": "Nấu nước dùng từ xương, thêm bánh canh và topping.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Bữa tối"],
        "calories": "600-800 kcal/phần"
    },
    "bánh chưng": {
        "type": "khô",
        "category": "bánh",
        "ingredients": ["gạo nếp", "đậu xanh", "thịt heo", "lá dong"],
        "recipe": "Gói gạo nếp, đậu xanh, thịt trong lá dong, luộc 10-12 giờ.",
        "popular_regions": ["Bắc Bộ"],
        "holidays": ["Tết"],
        "calories": "600-800 kcal/phần"
    },
    "nem chua": {
        "type": "ăn vặt",
        "category": "nem",
        "ingredients": ["thịt heo", "bì heo", "thính gạo", "tỏi"],
        "recipe": "Trộn thịt, bì, thính, gói lá chuối, ủ lên men 2-3 ngày.",
        "popular_regions": ["Thanh Hóa", "Toàn quốc"],
        "holidays": ["Ăn chơi", "Liên hoan"],
        "calories": "200-400 kcal/phần"
    },
    "chả cá Lã Vọng": {
        "type": "khô",
        "category": "cá",
        "ingredients": ["cá lăng", "thì là", "hành", "nước mắm"],
        "recipe": "Ướp cá với nghệ, nướng sơ, chiên trên chảo tại bàn, ăn với bún và rau.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Tiệc gia đình"],
        "calories": "500-700 kcal/phần"
    },
    "bún riêu": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "cua đồng", "cà chua", "đậu phụ"],
        "recipe": "Nấu nước dùng từ cua đồng, thêm cà chua, đậu phụ, ăn với bún.",
        "popular_regions": ["Bắc Bộ"],
        "holidays": ["Mọi dịp"],
        "calories": "500-700 kcal/phần"
    },
    "bánh hỏi": {
        "type": "khô",
        "category": "bánh",
        "ingredients": ["bánh hỏi", "thịt heo", "rau sống", "nước mắm"],
        "recipe": "Làm bánh hỏi từ bột gạo, ăn với thịt nướng hoặc luộc, chấm nước mắm.",
        "popular_regions": ["Bình Định", "Phú Yên"],
        "holidays": ["Bữa sáng", "Liên hoan"],
        "calories": "400-600 kcal/phần"
    },
    "bún nước lèo": {
        "type": "nước",
        "category": "bún",
        "ingredients": ["bún", "cá lóc", "mắm bò hóc", "rau muống"],
        "recipe": "Nấu nước dùng từ mắm bò hóc, thêm cá lóc, ăn với bún và rau.",
        "popular_regions": ["Sóc Trăng"],
        "holidays": ["Mọi dịp"],
        "calories": "600-800 kcal/phần"
    }
}

REGIONAL_FOODS = {
    "Hà Nội": ["phở", "bún chả", "bún đậu mắm tôm", "bánh cuốn", "cháo lòng", "chả cá Lã Vọng", "bún riêu"],
    "Hải Phòng": ["bánh đa cua", "nem cua bể", "lẩu cua đồng"],
    "Quảng Ninh": ["cháo hà", "sá sùng nướng", "sam biển"],
    "Nam Định": ["phở bò Nam Định", "bánh gai"],
    "Ninh Bình": ["cơm cháy Ninh Bình", "dê núi Ninh Bình"],
    "Thái Bình": ["bánh cáy", "canh cá rô đồng"],
    "Lạng Sơn": ["vịt quay Lạng Sơn", "khâu nhục"],
    "Thanh Hóa": ["nem chua Thanh Hóa", "chè lam Phủ Quảng", "nem chua"],
    "Nghệ An": ["cháo lươn Nghệ An", "mực nhảy Cửa Lò"],
    "Hà Tĩnh": ["ram bánh mướt", "cháo canh Hà Tĩnh"],
    "Huế": ["bún bò Huế", "cơm hến", "bánh bèo", "bánh nậm", "bánh lọc"],
    "Đà Nẵng": ["mì quảng", "bánh xèo", "bún chả cá"],
    "Quảng Nam": ["cao lầu Hội An", "mì Quảng gà", "bánh bao bánh vạc"],
    "Quảng Ngãi": ["don Quảng Ngãi", "ram bắp"],
    "Bình Định": ["bánh hỏi lòng heo", "bún chả cá Quy Nhơn", "bánh hỏi"],
    "Phú Yên": ["bánh hỏi chả nướng", "sò huyết đầm Ô Loan", "bánh hỏi"],
    "Khánh Hòa": ["nem nướng Nha Trang", "bún sứa", "yến sào"],
    "Ninh Thuận": ["nho Ninh Thuận", "thịt cừu nướng"],
    "Bình Thuận": ["bánh canh chả cá Phan Thiết", "dông nướng", "thanh long"],
    "Gia Lai": ["phở khô Gia Lai (phở hai tô)"],
    "Đắk Lắk": ["cà phê Buôn Ma Thuột", "bún đỏ"],
    "Kon Tum": ["gỏi lá Kon Tum"],
    "Lâm Đồng": ["lẩu gà lá é", "dâu tây Đà Lạt"],
    "Sài Gòn": ["cơm tấm", "hủ tiếu", "bánh mì", "gỏi cuốn", "bánh khọt", "bánh canh"],
    "Cần Thơ": ["lẩu mắm", "ốc nướng tiêu xanh", "bánh xèo miền Tây"],
    "An Giang": ["gỏi sầu đâu", "mắm Châu Đốc", "bò bảy món"],
    "Bạc Liêu": ["bún bò cay Bạc Liêu"],
    "Sóc Trăng": ["bún nước lèo Sóc Trăng", "bún nước lèo"],
    "Trà Vinh": ["bún suông Trà Vinh"],
    "Cà Mau": ["ba khía muối", "cua Cà Mau"],
    "Kiên Giang": ["gỏi cá trích Phú Quốc", "nước mắm Phú Quốc"],
    "Vũng Tàu": ["bánh khọt Vũng Tàu", "hải sản Vũng Tàu"],
    "Bắc Giang": ["vải thiều Lục Ngạn", "bánh đúc thịt"],
    "Quảng Bình": ["bánh bột lọc Quảng Bình", "cháo canh cá lóc"],
    "Đồng Nai": ["gỏi cá Đồng Nai", "bánh tráng phơi sương"],
    "Tây Ninh": ["bánh tráng phơi sương", "muối ớt Tây Ninh"],
    "Bến Tre": ["chuối đập Bến Tre", "kẹo dừa"]
}

# --------------------------------------------------------------------
# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start from user {update.effective_user.id}")
    await update.message.reply_text(
        "Xin chào! Mình là Alfred Food Bot.\n"
        "- /suggest: Gợi ý món ăn ngẫu nhiên.\n"
        "- /region [tên vùng]: Gợi ý món theo vùng (ví dụ: /region Hà Nội).\n"
        "- /ingredient [nguyên liệu1, nguyên liệu2]: Gợi ý món từ nguyên liệu có sẵn.\n"
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

    # Giả lập lệnh fake sau lệnh pass (để khắc phục bug loop)
    await asyncio.sleep(0.1)  # Delay nhỏ
    fake_update = Update.de_json({'update_id': random.randint(1, 1000), 'message': {'text': '/fake', 'chat': {'id': user_id}}}, application.bot)
    await application.process_update(fake_update)  # Xử lý lệnh fake rỗng

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

async def location_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"Received /location from user {user_id}")
    await update.message.reply_text("Chia sẻ vị trí của bạn để tôi gợi ý món địa phương (chỉ dùng để gợi ý, không lưu).")
    # Handler sẽ được thêm cho message với location (dưới)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    location = update.message.location
    if location:
        logger.info(f"Received location from user {user_id}: {location.latitude}, {location.longitude}")
        # Giả lập gợi ý vùng dựa trên location (thực tế cần API geocode, nhưng giả định)
        region = "Sài Gòn"  # Giả định, anh có thể thêm logic geocode thực tế
        foods = REGIONAL_FOODS.get(region, [])
        if foods:
            response = f"Dựa trên vị trí, vùng gần: *{region}*. Món gợi ý: {', '.join(foods)}"
            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text("Không tìm thấy vùng gần vị trí của bạn.")
    else:
        await update.message.reply_text("Vui lòng chia sẻ position.")

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

# --------------------------------------------------------------------
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

# --------------------------------------------------------------------
# Flask app for Render webhook
flask_app = Flask(__name__)

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        json_data = request.get_json(force=True)
        logger.info(f"Received webhook data: {json_data}")
        update = Update.de_json(json_data, application.bot)
        if update:
            logger.info(f"Processing update: {update.update_id}")
            await application.process_update(update)
            logger.info(f"Processed update: {update.update_id}")
            # Giả lập lệnh fake sau lệnh pass (để khắc phục bug loop)
            await asyncio.sleep(0.1)  # Delay nhỏ
            fake_update = Update.de_json({'update_id': random.randint(1, 1000), 'message': {'text': '/fake', 'chat': {'id': update.effective_user.id}}}, application.bot)
            await application.process_update(fake_update)  # Xử lý lệnh fake rỗng để reset loop
            return "ok", 200
        else:
            logger.warning("Received invalid update")
            return "Invalid update", 400
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return "Error", 500

@flask_app.route("/webhook", methods=["GET"])
async def webhook_get():
    logger.warning("Webhook endpoint only accepts POST requests")
    return "Method Not Allowed: Use POST for webhook", 405

@flask_app.route("/")
def index():
    return "Alfred Food Bot running!", 200

# --------------------------------------------------------------------
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
