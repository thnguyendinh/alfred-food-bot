import os
import json
import random
import logging
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from flask import Flask, request

# ===== CẤU HÌNH =====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
RENDER = os.getenv("RENDER", False)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
DATABASE_URL = os.getenv("DATABASE_URL")

# Kiểm tra và import database driver
USE_POSTGRES = False
if DATABASE_URL and "postgres" in DATABASE_URL:
    try:
        import pg8000.native
        USE_POSTGRES = True
    except ImportError:
        USE_POSTGRES = False
        logging.warning("pg8000 not available, falling back to SQLite")

# Fallback to SQLite
if not USE_POSTGRES:
    import sqlite3

# Khởi tạo Flask app nếu dùng webhook
if RENDER and WEBHOOK_URL:
    app = Flask(__name__)

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Trạng thái conversation
SELECTING_ACTION, CHOOSING_TYPE, PROVIDING_LOCATION, GETTING_HISTORY = range(4)

# ===== CƠ SỞ DỮ LIỆU MÓN ĂN =====
VIETNAMESE_FOODS = {
    # ===== Miền Bắc =====
    "phở": {
        "type": "nước", "category": "phở",
        "ingredients": ["bánh phở", "thịt bò/gà", "xương hầm", "hành", "rau thơm"],
        "recipe": "Hầm xương bò/gà làm nước dùng, thêm gia vị, thả bánh phở và thịt.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Tết", "Ngày thường"]
    },
    "bún chả": {
        "type": "nước", "category": "bún",
        "ingredients": ["bún", "thịt nướng", "nước mắm", "rau sống"],
        "recipe": "Nướng thịt, pha nước mắm chua ngọt, ăn kèm với bún và rau.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Bữa trưa"]
    },
    "bún đậu mắm tôm": {
        "type": "khô", "category": "bún",
        "ingredients": ["bún", "đậu phụ", "mắm tôm", "thịt luộc", "rau sống"],
        "recipe": "Chiên đậu, luộc thịt, pha mắm tôm, ăn kèm bún và rau.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Liên hoan", "Ăn chơi"]
    },
    "bánh cuốn": {
        "type": "khô", "category": "bánh",
        "ingredients": ["bột gạo", "thịt băm", "mộc nhĩ", "hành phi"],
        "recipe": "Tráng bột gạo mỏng, cuốn nhân thịt mộc nhĩ, ăn với nước mắm.",
        "popular_regions": ["Hà Nội", "Bắc Ninh"],
        "holidays": ["Bữa sáng"]
    },
    "cháo lòng": {
        "type": "nước", "category": "cháo",
        "ingredients": ["gạo", "lòng heo", "hành", "gia vị"],
        "recipe": "Nấu cháo từ gạo, thêm lòng heo, nêm gia vị vừa ăn.",
        "popular_regions": ["Bắc Bộ"],
        "holidays": ["Mọi dịp"]
    },

    # ===== Miền Trung =====
    "bún bò Huế": {
        "type": "nước", "category": "bún",
        "ingredients": ["bún", "thịt bò", "giò heo", "mắm ruốc"],
        "recipe": "Hầm xương, nêm mắm ruốc, thêm bún và thịt.",
        "popular_regions": ["Huế"],
        "holidays": ["Tết", "Lễ hội"]
    },
    "cơm hến": {
        "type": "khô", "category": "cơm",
        "ingredients": ["cơm", "hến", "rau sống", "mắm ruốc"],
        "recipe": "Xào hến, trộn với cơm và rau, chan nước hến.",
        "popular_regions": ["Huế"],
        "holidays": ["Bữa thường ngày"]
    },
    "bánh bèo": {
        "type": "ăn vặt", "category": "bánh",
        "ingredients": ["bột gạo", "tôm khô", "mỡ hành", "nước mắm"],
        "recipe": "Hấp bột gạo trong chén nhỏ, rắc nhân tôm, chan nước mắm.",
        "popular_regions": ["Huế"],
        "holidays": ["Liên hoan"]
    },
    "mì quảng": {
        "type": "khô", "category": "mì",
        "ingredients": ["mì quảng", "thịt gà/heo/tôm", "rau sống", "đậu phộng"],
        "recipe": "Nấu nước dùng ít, chan vào mì, thêm rau, đậu phộng.",
        "popular_regions": ["Đà Nẵng", "Quảng Nam"],
        "holidays": ["Mọi dịp"]
    },
    "bánh xèo": {
        "type": "ăn vặt", "category": "bánh",
        "ingredients": ["bột gạo", "tôm", "thịt", "giá", "rau sống"],
        "recipe": "Đổ bột tráng mỏng, cho nhân, chiên giòn, ăn kèm rau và nước mắm.",
        "popular_regions": ["Miền Trung", "Miền Nam"],
        "holidays": ["Cuối tuần"]
    },
    "bún chả cá": {
        "type": "nước", "category": "bún",
        "ingredients": ["bún", "chả cá", "rau", "gia vị"],
        "recipe": "Nấu nước dùng từ cá, thêm bún và chả cá.",
        "popular_regions": ["Đà Nẵng"],
        "holidays": ["Mọi dịp"]
    },

    # ===== Miền Nam =====
    "cơm tấm": {
        "type": "khô", "category": "cơm",
        "ingredients": ["gạo tấm", "sườn nướng", "bì", "chả trứng"],
        "recipe": "Nấu cơm tấm, nướng sườn, ăn kèm bì chả.",
        "popular_regions": ["Sài Gòn"],
        "holidays": ["Mọi dịp"]
    },
    "hủ tiếu": {
        "type": "nước", "category": "hủ tiếu",
        "ingredients": ["hủ tiếu", "thịt", "tôm", "trứng cút"],
        "recipe": "Nấu nước hầm xương, chan lên h�ủ tiếu.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Bữa sáng"]
    },
    "bánh mì": {
        "type": "khô", "category": "bánh mì",
        "ingredients": ["bánh mì", "pate", "thịt", "rau"],
        "recipe": "Nướng bánh mì, phết pate, thêm thịt và rau.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Bữa sáng"]
    },
    "gỏi cuốn": {
        "type": "ăn vặt", "category": "cuốn",
        "ingredients": ["bánh tráng", "tôm", "thịt", "bún", "rau sống"],
        "recipe": "Cuốn tôm thịt, bún và rau trong bánh tráng, chấm mắm nêm.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Ăn nhẹ"]
    },
    "bánh khọt": {
        "type": "ăn vặt", "category": "bánh",
        "ingredients": ["bột gạo", "tôm", "mỡ hành", "nước mắm"],
        "recipe": "Đổ bột vào khuôn nhỏ, thêm tôm, chiên giòn, ăn với rau.",
        "popular_regions": ["Vũng Tàu"],
        "holidays": ["Ăn chơi"]
    },
    "lẩu mắm": {
        "type": "nước", "category": "lẩu",
        "ingredients": ["mắm cá", "các loại cá", "rau", "bún"],
        "recipe": "Nấu mắm cá làm nước lẩu, ăn kèm bún và rau.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Sum họp"]
    },
    "cá lóc nướng trui": {
        "type": "khô", "category": "cá",
        "ingredients": ["cá lóc", "muối", "rau sống", "nước mắm"],
        "recipe": "Nướng cá lóc bằng rơm, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Tiệc ngoài trời"]
    },
    "bún cá": {
        "type": "nước", "category": "bún",
        "ingredients": ["bún", "cá", "rau thơm"],
        "recipe": "Nấu nước cá, chan lên bún.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Mọi dịp"]
    },
    "chè ba màu": {
        "type": "tráng miệng", "category": "chè",
        "ingredients": ["đậu xanh", "đậu đỏ", "rau câu", "nước cốt dừa"],
        "recipe": "Nấu chè nhiều lớp màu, chan nước cốt dừa, ăn kèm đá.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Mùa hè"]
    },
    "chè trôi nước": {
        "type": "tráng miệng", "category": "chè",
        "ingredients": ["bột nếp", "đậu xanh", "gừng", "đường"],
        "recipe": "Vo viên bột nếp nhân đậu xanh, luộc chín, chan nước gừng ngọt.",
        "popular_regions": ["Nam Bộ"],
        "holidays": ["Tết Hàn Thực", "Ngày thường"]
    }
}

REGIONAL_FOODS = {
    # ===== Bắc Bộ =====
    "Hà Nội": ["phở", "bún chả", "bún đậu mắm tôm", "bánh cuốn", "cháo lòng"],
    "Hải Phòng": ["bánh đa cua", "nem cua bể", "lẩu cua đồng"],
    "Quảng Ninh": ["cháo hà", "sá sùng nướng", "sam biển"],
    "Nam Định": ["phở bò Nam Định", "bánh gai"],
    "Ninh Bình": ["cơm cháy Ninh Bình", "dê núi Ninh Bình"],
    "Thái Bình": ["bánh cáy", "canh cá rô đồng"],
    "Lạng Sơn": ["vịt quay Lạng Sơn", "khâu nhục"],

    # ===== Bắc Trung Bộ =====
    "Thanh Hóa": ["nem chua Thanh Hóa", "chè lam Phủ Quảng"],
    "Nghệ An": ["cháo lươn Nghệ An", "mực nhảy Cửa Lò"],
    "Hà Tĩnh": ["ram bánh mướt", "cháo canh Hà Tĩnh"],
    "Huế": ["bún bò Huế", "cơm hến", "bánh bèo", "bánh nậm", "bánh lọc"],

    # ===== Duyên hải Nam Trung Bộ =====
    "Đà Nẵng": ["mì quảng", "bánh xèo", "bún chả cá"],
    "Quảng Nam": ["cao lầu Hội An", "mì Quảng gà", "bánh bao bánh vạc"],
    "Quảng Ngãi": ["don Quảng Ngãi", "ram bắp"],
    "Bình Định": ["bánh hỏi lòng heo", "bún chả cá Quy Nhơn"],
    "Phú Yên": ["bánh hỏi chả nướng", "sò huyết đầm Ô Loan"],
    "Khánh Hòa": ["nem nướng Nha Trang", "bún sứa", "yến sào"],
    "Ninh Thuận": ["nho Ninh Thuận", "thịt cừu nướng"],
    "Bình Thuận": ["bánh canh chả cá Phan Thiết", "dông nướng", "thanh long"],

    # ===== Tây Nguyên =====
    "Gia Lai": ["phở khô Gia Lai (phở hai tô)"],
    "Đắk Lắk": ["cà phê Buôn Ma Thuột", "bún đỏ"],
    "Kon Tum": ["gỏi lá Kon Tum"],
    "Lâm Đồng": ["lẩu gà lá é", "dâu tây Đà Lạt"],

    # ===== Nam Bộ =====
    "Sài Gòn": ["cơm tấm", "hủ tiếu", "bánh mì", "gỏi cuốn", "bánh khọt"],
    "Cần Thơ": ["lẩu mắm", "ốc nướng tiêu xanh", "bánh xèo miền Tây"],
    "An Giang": ["gỏi sầu đâu", "mắm Châu Đốc", "bò bảy món"],
    "Bạc Liêu": ["bún bò cay Bạc Liêu"],
    "Sóc Trăng": ["bún nước lèo Sóc Trăng"],
    "Trà Vinh": ["bún suông Trà Vinh"],
    "Cà Mau": ["ba khía muối", "cua Cà Mau"],
    "Kiên Giang": ["gỏi cá trích Phú Quốc", "nước mắm Phú Quốc"],
    "Vũng Tàu": ["bánh khọt Vũng Tàu", "hải sản Vũng Tàu"]
}

# ===== LỚP DATABASE =====
class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Kết nối đến database"""
        try:
            if USE_POSTGRES and DATABASE_URL:
                # Parse connection string cho PostgreSQL
                url = urllib.parse.urlparse(DATABASE_URL)
                self.conn = pg8000.native.Connection(
                    user=url.username,
                    password=url.password,
                    host=url.hostname,
                    port=url.port,
                    database=url.path[1:]  # Bỏ dấu / ở đầu
                )
                logger.info("Kết nối PostgreSQL thành công với pg8000")
            else:
                # Fallback to SQLite
                db_path = '/tmp/alfred.db' if RENDER else 'alfred.db'
                self.conn = sqlite3.connect(db_path, check_same_thread=False)
                logger.info("Kết nối SQLite thành công")
        except Exception as e:
            logger.error(f"Lỗi kết nối database: {e}")
            # Tạo SQLite connection như fallback
            try:
                db_path = '/tmp/alfred.db' if RENDER else 'alfred.db'
                self.conn = sqlite3.connect(db_path, check_same_thread=False)
                logger.info("Fallback SQLite connection thành công")
            except Exception as e2:
                logger.error(f"Lỗi fallback SQLite: {e2}")
    
    def create_tables(self):
        """Tạo bảng nếu chưa tồn tại"""
        if self.conn is None:
            logger.error("Không thể tạo bảng: connection is None")
            return
            
        try:
            if USE_POSTGRES:
                # Tạo bảng cho PostgreSQL
                self.conn.run("""
                    CREATE TABLE IF NOT EXISTS user_histories (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        food TEXT NOT NULL,
                        meal_type TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.conn.run("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id BIGINT PRIMARY KEY,
                        preferences JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.conn.run("CREATE INDEX IF NOT EXISTS idx_user_id ON user_histories(user_id)")
            else:
                # Tạo bảng cho SQLite
                cursor = self.conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_histories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        food TEXT NOT NULL,
                        meal_type TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id INTEGER PRIMARY KEY,
                        preferences TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON user_histories(user_id)')
                self.conn.commit()
                
            logger.info("Tạo bảng thành công")
        except Exception as e:
            logger.error(f"Lỗi tạo bảng: {e}")

    def get_user_history(self, user_id: int) -> List[Dict]:
        if self.conn is None:
            return []
            
        try:
            if USE_POSTGRES:
                result = self.conn.run(
                    "SELECT food, meal_type, created_at FROM user_histories WHERE user_id = $1 ORDER BY created_at DESC LIMIT 10",
                    user_id
                )
                return [{"food": row[0], "type": row[1], "date": row[2].isoformat()} for row in result]
            else:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT food, meal_type, created_at FROM user_histories WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
                    (user_id,)
                )
                rows = cursor.fetchall()
                return [{"food": row[0], "type": row[1], "date": row[2]} for row in rows]
        except Exception as e:
            logger.error(f"Lỗi get_user_history: {e}")
            return []

    def add_to_history(self, user_id: int, food: str, meal_type: str = None):
        if self.conn is None:
            return
            
        try:
            if USE_POSTGRES:
                self.conn.run(
                    "INSERT INTO user_histories (user_id, food, meal_type) VALUES ($1, $2, $3)",
                    user_id, food, meal_type
                )
            else:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO user_histories (user_id, food, meal_type) VALUES (?, ?, ?)",
                    (user_id, food, meal_type)
                )
                self.conn.commit()
        except Exception as e:
            logger.error(f"Lỗi add_to_history: {e}")

    def get_user_preferences(self, user_id: int) -> Dict:
        if self.conn is None:
            return {}
            
        try:
            if USE_POSTGRES:
                result = self.conn.run(
                    "SELECT preferences FROM user_preferences WHERE user_id = $1",
                    user_id
                )
                if result and result[0]:
                    return json.loads(result[0][0])
            else:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT preferences FROM user_preferences WHERE user_id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                if row and row[0]:
                    return json.loads(row[0])
            return {}
        except Exception as e:
            logger.error(f"Lỗi get_user_preferences: {e}")
            return {}

    def save_user_preferences(self, user_id: int, preferences: Dict):
        if self.conn is None:
            return
            
        try:
            preferences_json = json.dumps(preferences)
            if USE_POSTGRES:
                self.conn.run(
                    """INSERT INTO user_preferences (user_id, preferences) 
                       VALUES ($1, $2)
                       ON CONFLICT (user_id) 
                       DO UPDATE SET preferences = $2, updated_at = CURRENT_TIMESTAMP""",
                    user_id, preferences_json
                )
            else:
                cursor = self.conn.cursor()
                cursor.execute(
                    """INSERT OR REPLACE INTO user_preferences (user_id, preferences, updated_at) 
                       VALUES (?, ?, CURRENT_TIMESTAMP)""",
                    (user_id, preferences_json)
                )
                self.conn.commit()
        except Exception as e:
            logger.error(f"Lỗi save_user_preferences: {e}")

# ===== LỚP FOOD ASSISTANT =====
class FoodAssistant:
    def __init__(self):
        self.db = Database()
        
    def get_user_history(self, user_id: int) -> List[Dict]:
        return self.db.get_user_history(user_id)
    
    def add_to_history(self, user_id: int, food: str, meal_type: str = None):
        self.db.add_to_history(user_id, food, meal_type)
    
    def get_recent_foods(self, user_id: int, count: int = 3) -> List[str]:
        history = self.get_user_history(user_id)
        recent = history[:count] if len(history) >= count else history
        return [item["food"] for item in recent]
    
    def filter_foods_by_type(self, food_type: str = None) -> List[str]:
        if not food_type:
            return list(VIETNAMESE_FOODS.keys())
        return [food for food, details in VIETNAMESE_FOODS.items() 
                if details["type"] == food_type]
    
    def get_regional_foods(self, region: str) -> List[str]:
        return REGIONAL_FOODS.get(region, [])
    
    def suggest_food(self, user_id: int, preferences: Dict[str, Any]) -> str:
        recent_foods = self.get_recent_foods(user_id, 3)
        available_foods = self.filter_foods_by_type(preferences.get("type"))
        
        if preferences.get("region"):
            regional_foods = self.get_regional_foods(preferences.get("region"))
            available_foods = [f for f in available_foods if f in regional_foods]
        
        available_foods = [f for f in available_foods if f not in recent_foods]
        
        if not available_foods:
            available_foods = list(VIETNAMESE_FOODS.keys())
        
        if available_foods:
            selected_food = random.choice(available_foods)
            self.add_to_history(user_id, selected_food, preferences.get("type"))
            return selected_food
        else:
            return "Xin lỗi, không tìm thấy món ăn phù hợp."
    
    def get_food_info(self, food_name: str) -> Dict:
        if food_name in VIETNAMESE_FOODS:
            info = VIETNAMESE_FOODS[food_name].copy()
            info["name"] = food_name
            return info
        
        return {
            "name": food_name,
            "type": "không xác định",
            "category": "không xác định",
            "ingredients": ["không xác định"],
            "recipe": "Công thức không có sẵn.",
            "popular_regions": ["không xác định"],
            "holidays": ["không xác định"]
        }

# ===== HANDLERS =====
food_bot = FoodAssistant()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"Xin chào {user.first_name}! Tôi là Alfred, trợ lý ẩm thực Việt Nam.\n\n"
        "Gõ /suggest để nhận gợi ý món ăn!",
        reply_markup=ReplyKeyboardRemove()
    )
    return SELECTING_ACTION

async def suggest_food(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    history = food_bot.get_user_history(user_id)
    
    if history:
        recent_foods = food_bot.get_recent_foods(user_id, 3)
        await update.message.reply_text(
            f"Bạn đã ăn: {', '.join(recent_foods)}.\nTôi sẽ tránh gợi ý những món này.\n\n"
            "Bạn muốn ăn món khô hay món nước?",
            reply_markup=ReplyKeyboardMarkup([["Khô", "Nước", "Cả hai"]], one_time_keyboard=True)
        )
    else:
        await update.message.reply_text(
            "Bạn muốn ăn món khô hay món nước?",
            reply_markup=ReplyKeyboardMarkup([["Khô", "Nước", "Cả hai"]], one_time_keyboard=True)
        )
    return CHOOSING_TYPE

async def handle_food_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    food_type = update.message.text.lower()
    
    if user_id not in context.user_data:
        context.user_data[user_id] = {}
    
    if food_type == "khô":
        context.user_data[user_id]["type"] = "khô"
    elif food_type == "nước":
        context.user_data[user_id]["type"] = "nước"
    else:
        context.user_data[user_id]["type"] = None
    
    await update.message.reply_text(
        "Bạn có đang ở địa phương nào không? (ví dụ: Hà Nội, Huế, Sài Gòn...)\n"
        "Nếu không, gõ 'không'.",
        reply_markup=ReplyKeyboardRemove()
    )
    return PROVIDING_LOCATION

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    location = update.message.text
    
    preferences = context.user_data.get(user_id, {})
    if location.lower() != "không":
        preferences["region"] = location
    
    suggested_food = food_bot.suggest_food(user_id, preferences)
    food_info = food_bot.get_food_info(suggested_food)
    
    response = f"Gợi ý: {suggested_food}\n\n"
    response += f"Loại: {food_info['type']}\n"
    response += f"Phân loại: {food_info['category']}\n"
    response += f"Nguyên liệu: {', '.join(food_info['ingredients'][:3])}\n"
    response += f"Vùng miền: {', '.join(food_info['popular_regions'])}\n\n"
    response += "Bạn có muốn xem công thức nấu không? (có/không)"
    
    context.user_data["last_suggestion"] = suggested_food
    await update.message.reply_text(response)
    return GETTING_HISTORY

async def handle_recipe_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_response = update.message.text.lower()
    
    if user_response == "có":
        suggested_food = context.user_data.get("last_suggestion", "")
        food_info = food_bot.get_food_info(suggested_food)
        await update.message.reply_text(f"Công thức {suggested_food}:\n\n{food_info['recipe']}")
    
    await update.message.reply_text(
        "Cảm ơn bạn! Gõ /suggest để nhận gợi ý món ăn khác.",
        reply_markup=ReplyKeyboardRemove()
    )
    return SELECTING_ACTION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Tạm biệt!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def food_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập tên món ăn. Ví dụ: /info phở")
        return
    
    food_name = " ".join(context.args)
    food_info = food_bot.get_food_info(food_name)
    
    response = f"Thông tin {food_info['name']}:\n\n"
    response += f"Loại: {food_info['type']}\n"
    response += f"Phân loại: {food_info['category']}\n"
    response += f"Nguyên liệu: {', '.join(food_info['ingredients'])}\n"
    response += f"Vùng miền: {', '.join(food_info['popular_regions'])}\n\n"
    response += f"Công thức: {food_info['recipe']}"
    
    await update.message.reply_text(response)

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    history = food_bot.get_user_history(user_id)
    
    if not history:
        await update.message.reply_text("Bạn chưa có lịch sử món ăn.")
        return
    
    response = "Lịch sử món ăn gần đây:\n\n"
    for i, item in enumerate(history[:5], 1):
        response += f"{i}. {item['food']} ({item['date'][:10]})\n"
    
    await update.message.reply_text(response)

# ===== MAIN =====
def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN không được thiết lập!")
        return
    
    # Tạo application với các tham số đúng
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [CommandHandler("suggest", suggest_food)],
            CHOOSING_TYPE: [MessageHandler(filters.Regex("^(Khô|Nước|Cả hai)$"), handle_food_type)],
            PROVIDING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)],
            GETTING_HISTORY: [MessageHandler(filters.Regex("^(có|không)$"), handle_recipe_request)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("info", food_info))
    application.add_handler(CommandHandler("history", history))

    if RENDER and WEBHOOK_URL:
        @app.route('/webhook', methods=['POST'])
        def webhook():
            update = Update.de_json(request.get_json(), application.bot)
            application.update_queue.put(update)
            return 'ok'
        
        @app.route('/')
        def index():
            return 'Alfred Food Bot is running!'
        
        # Sửa lỗi run_webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)),
            webhook_url=WEBHOOK_URL,
            secret_token='WEBHOOK_SECRET'  # Thêm secret token
        )
    else:
        # Sửa lỗi polling
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        print("Bot đang chạy...")

if __name__ == "__main__":
    main()
