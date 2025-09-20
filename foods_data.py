import random

VIETNAMESE_FOODS = {
    "Phở": {
        "type": "nước",
        "ingredients": ["thịt bò", "bánh phở", "nước dùng", "hành lá", "rau mùi"],
        "recipe": "Nấu nước dùng từ xương bò, thêm gia vị (quế, hồi), cho bánh phở và thịt bò thái mỏng, trang trí hành lá, rau mùi.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Nam Định"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh chưng": {
        "type": "khô",
        "ingredients": ["gạo nếp", "đậu xanh", "thịt lợn", "lá dong"],
        "recipe": "Gói gạo nếp, đậu xanh, thịt lợn bằng lá dong, luộc 10-12 giờ, ăn kèm chả lụa hoặc dưa hành.",
        "popular_regions": ["Hà Nội", "Bắc Bộ"],
        "holidays": ["Tết Nguyên Đán"],
        "calories": "700-800 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bún bò Huế": {
        "type": "nước",
        "ingredients": ["thịt bò", "bún", "nước dùng", "sả", "ớt", "rau thơm"],
        "recipe": "Nấu nước dùng từ xương bò và sả, thêm bún, thịt bò, tiết heo, ăn kèm rau thơm và ớt.",
        "popular_regions": ["Huế", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh xèo": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm", "thịt lợn", "giá đỗ", "hành lá"],
        "recipe": "Trộn bột gạo với nước và nghệ, chiên với tôm, thịt, giá đỗ, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cơm tấm": {
        "type": "khô",
        "ingredients": ["tấm", "sườn nướng", "trứng ốp la", "dưa leo", "nước mắm"],
        "recipe": "Nấu tấm, nướng sườn, chiên trứng, ăn kèm dưa leo và nước mắm ớt.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "700-800 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bún chả": {
        "type": "khô",
        "ingredients": ["chả nướng", "bún", "nước mắm", "rau sống", "đu đủ muối"],
        "recipe": "Nướng chả, nấu nước mắm chua ngọt, ăn kèm bún, rau sống và đu đủ muối.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa"]
    },
    "Bánh cuốn": {
        "type": "khô",
        "ingredients": ["bột gạo", "thịt băm", "mộc nhĩ", "hành phi", "nước mắm"],
        "recipe": "Tráng bột gạo thành bánh mỏng, cho nhân thịt băm và mộc nhĩ, cuộn lại, rắc hành phi, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Bắc Bộ"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng"]
    },
    "Bánh mì": {
        "type": "khô",
        "ingredients": ["bánh mì", "thịt heo", "pate", "dưa leo", "rau mùi"],
        "recipe": "Xẻ bánh mì, phết pate, cho thịt heo, dưa leo, rau mùi, thêm nước tương hoặc mayonnaise.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Hủ tiếu": {
        "type": "nước",
        "ingredients": ["hủ tiếu", "thịt heo", "tôm", "hẹ", "nước dùng"],
        "recipe": "Nấu nước dùng từ xương heo, thêm hủ tiếu, thịt heo, tôm, trang trí hẹ và giá đỗ.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Chả lụa": {
        "type": "khô",
        "ingredients": ["thịt heo", "nước mắm", "lá chuối"],
        "recipe": "Xay thịt heo với nước mắm, gói trong lá chuối, hấp chín, ăn kèm bánh mì hoặc cơm.",
        "popular_regions": ["Hà Nội", "Sài Gòn"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bún riêu": {
        "type": "nước",
        "ingredients": ["bún", "cua", "cà chua", "đậu phụ", "rau muống"],
        "recipe": "Nấu nước dùng từ cua và cà chua, thêm đậu phụ, bún, ăn kèm rau muống và mắm tôm.",
        "popular_regions": ["Hà Nội", "Bắc Bộ"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cao lầu": {
        "type": "khô",
        "ingredients": ["mì cao lầu", "thịt heo", "rau sống", "đậu phộng"],
        "recipe": "Luộc mì cao lầu, thêm thịt heo xá xíu, rau sống, rắc đậu phộng, chấm nước mắm.",
        "popular_regions": ["Hội An", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa"]
    },
    "Mì Quảng": {
        "type": "nước",
        "ingredients": ["mì Quảng", "tôm", "thịt heo", "đậu phộng", "bánh tráng"],
        "recipe": "Nấu nước dùng với tôm, thịt heo, thêm mì Quảng, đậu phộng, ăn kèm bánh tráng và rau sống.",
        "popular_regions": ["Quảng Nam", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh rế": {
        "type": "khô",
        "ingredients": ["bột gạo", "đường", "vừng"],
        "recipe": "Trộn bột gạo với đường, chiên thành bánh mỏng, rắc vừng, ăn như món tráng miệng.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Trung Thu", "Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Chè ba màu": {
        "type": "nước",
        "ingredients": ["đậu đỏ", "đậu xanh", "nước cốt dừa", "thạch"],
        "recipe": "Nấu đậu đỏ, đậu xanh, làm thạch, trộn với nước cốt dừa và đá, ăn lạnh.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Gỏi cuốn": {
        "type": "khô",
        "ingredients": ["bánh tráng", "tôm", "thịt heo", "bún", "rau sống"],
        "recipe": "Cuốn tôm, thịt heo, bún, rau sống trong bánh tráng, chấm nước mắm hoặc tương đậu.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Nem chua": {
        "type": "khô",
        "ingredients": ["thịt heo", "bì heo", "tỏi", "ớt"],
        "recipe": "Trộn thịt heo xay, bì heo, tỏi, ớt, gói lá chuối, ủ 2-3 ngày, ăn kèm tỏi ớt.",
        "popular_regions": ["Thanh Hóa", "Hà Nội"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bánh tét": {
        "type": "khô",
        "ingredients": ["gạo nếp", "đậu xanh", "thịt lợn", "lá chuối"],
        "recipe": "Gói gạo nếp, đậu xanh, thịt lợn trong lá chuối, luộc 6-8 giờ, ăn kèm dưa hành.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Tết Nguyên Đán"],
        "calories": "600-700 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Canh chua": {
        "type": "nước",
        "ingredients": ["cá", "cà chua", "dứa", "rau muống", "me"],
        "recipe": "Nấu nước dùng với me, cà chua, dứa, thêm cá và rau muống, ăn kèm cơm.",
        "popular_regions": ["Miền Tây", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Lẩu mắm": {
        "type": "nước",
        "ingredients": ["mắm cá", "thịt heo", "tôm", "cá", "rau"],
        "recipe": "Nấu mắm cá với nước, thêm thịt heo, tôm, cá, ăn kèm rau và bún.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "600-800 kcal",
        "meal_time": ["tối"]
    },
    "Xôi gà": {
        "type": "khô",
        "ingredients": ["gạo nếp", "gà luộc", "hành phi", "muối tiêu"],
        "recipe": "Nấu gạo nếp thành xôi, xé gà luộc, rắc hành phi, ăn kèm muối tiêu chanh.",
        "popular_regions": ["Hà Nội", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng"]
    },
    "Bún nước lèo": {
        "type": "nước",
        "ingredients": ["bún", "mắm cá", "tôm", "thịt heo", "rau"],
        "recipe": "Nấu nước dùng từ mắm cá, thêm bún, tôm, thịt heo, ăn kèm rau sống.",
        "popular_regions": ["Miền Tây"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Chả cá Lã Vọng": {
        "type": "khô",
        "ingredients": ["cá lăng", "thì là", "hành lá", "bún", "đậu phộng"],
        "recipe": "Ướp cá lăng với nghệ, chiên, xào với thì là và hành lá, ăn kèm bún và đậu phộng.",
        "popular_regions": ["Hà Nội"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh bèo": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm khô", "hành phi", "nước mắm"],
        "recipe": "Hấp bột gạo trong chén nhỏ, thêm tôm khô, hành phi, chấm nước mắm.",
        "popular_regions": ["Huế"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh khoái": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm", "thịt", "giá đỗ"],
        "recipe": "Chiên bột gạo với tôm, thịt, giá đỗ, ăn kèm rau sống và nước lèo.",
        "popular_regions": ["Huế"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh ướt thịt nướng": {
        "type": "khô",
        "ingredients": ["bánh ướt", "thịt nướng", "rau sống", "nước mắm"],
        "recipe": "Tráng bánh ướt, thêm thịt nướng, rau sống, chấm nước mắm chua ngọt.",
        "popular_regions": ["Huế", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["trưa"]
    },
    "Bún bò Nam Bộ": {
        "type": "khô",
        "ingredients": ["bún", "thịt bò", "rau thơm", "đậu phộng", "nước mắm"],
        "recipe": "Xào thịt bò với tỏi, trộn với bún, rau thơm, đậu phộng, chấm nước mắm.",
        "popular_regions": ["Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh bột lọc": {
        "type": "khô",
        "ingredients": ["bột sắn", "tôm", "thịt heo", "nước mắm"],
        "recipe": "Nhồi bột sắn với tôm, thịt heo, gói lá chuối, hấp chín, chấm nước mắm.",
        "popular_regions": ["Huế"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Chè đậu trắng": {
        "type": "nước",
        "ingredients": ["đậu trắng", "nước cốt dừa", "đường"],
        "recipe": "Nấu đậu trắng với đường, thêm nước cốt dừa, ăn nóng hoặc lạnh.",
        "popular_regions": ["Sài Gòn", "Miền Tây"],
        "holidays": ["Trung Thu", "Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    }
}

REGIONAL_FOODS = {
    "Hà Nội": ["Phở", "Bún chả", "Bánh cuốn", "Chả cá Lã Vọng", "Chả lụa", "Bún riêu", "Xôi gà"],
    "Sài Gòn": ["Bánh xèo", "Cơm tấm", "Hủ tiếu", "Chè ba màu", "Gỏi cuốn", "Bún bò Nam Bộ", "Chè đậu trắng"],
    "Huế": ["Bún bò Huế", "Bánh bèo", "Bánh khoái", "Bánh ướt thịt nướng", "Bánh bột lọc"],
    "Đà Nẵng": ["Mì Quảng", "Cao lầu", "Bún bò Huế", "Bánh ướt thịt nướng"],
    "Miền Tây": ["Bánh xèo", "Cơm tấm", "Hủ tiếu", "Bánh rế", "Canh chua", "Lẩu mắm", "Bún nước lèo", "Chè ba màu"],
    "Bắc Bộ": ["Bánh chưng", "Bánh cuốn", "Chả lụa", "Bún riêu"],
    "Nam Định": ["Phở"],
    "Quảng Nam": ["Mì Quảng", "Cao lầu"],
    "Thanh Hóa": ["Nem chua"],
    "Hội An": ["Cao lầu"],
    "Cần Thơ": ["Bánh xèo", "Canh chua", "Lẩu mắm"],
    "Vũng Tàu": ["Bánh xèo", "Gỏi cuốn"],
    "Phú Quốc": ["Gỏi cuốn", "Bún nước lèo"],
    "Nha Trang": ["Bún bò Nam Bộ"],
    "Đà Lạt": ["Bánh ướt thịt nướng"],
    "Bình Định": ["Bánh khoái"],
    "Quảng Ngãi": ["Mì Quảng"],
    "Hải Phòng": ["Bánh mì", "Chả lụa"],
    "Quảng Ninh": ["Chả lụa"],
    "Lạng Sơn": ["Bánh cuốn"],
    "Bắc Giang": ["Bánh chưng"],
    "Bắc Ninh": ["Bánh cuốn"],
    "Hưng Yên": ["Chả lụa"],
    "Vĩnh Phúc": ["Bánh chưng"],
    "Phú Thọ": ["Bánh chưng"],
    "Thái Nguyên": ["Bánh chưng"],
    "Sơn La": ["Xôi gà"],
    "Lào Cai": ["Xôi gà"],
    "Yên Bái": ["Xôi gà"],
    "Điện Biên": ["Xôi gà"],
    "Hòa Bình": ["Bánh chưng"],
    "Tây Ninh": ["Bánh xèo"],
    "Long An": ["Canh chua"],
    "Tiền Giang": ["Hủ tiếu"],
    "Kiên Giang": ["Bún nước lèo"]
}

HOLIDAYS = {
    "Tết Nguyên Đán": (1, 1, 1, 10),  # Mùng 1-10 tháng 1 âm lịch
    "Trung Thu": (8, 15, 8, 15),      # Ngày 15 tháng 8 âm lịch
    "Ngày thường": (1, 1, 12, 31)     # Các ngày không phải lễ
}
