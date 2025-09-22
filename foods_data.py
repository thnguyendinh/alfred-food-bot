import random

VIETNAMESE_FOODS = {
    "Phở": {
        "type": "nước",
        "ingredients": ["thịt bò", "bánh phở", "nước dùng", "hành lá", "rau mùi", "gừng", "quế", "hồi"],
        "recipe": "Nấu nước dùng từ xương bò, thêm gia vị (quế, hồi, gừng), cho bánh phở và thịt bò thái mỏng, trang trí hành lá, rau mùi.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Nam Định", "Hải Phòng"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Phở gà": {
        "type": "nước",
        "ingredients": ["thịt gà", "bánh phở", "nước dùng", "hành lá", "rau mùi", "gừng", "hành tây"],
        "recipe": "Nấu nước dùng từ xương gà, thêm gia vị, cho bánh phở và thịt gà xé, trang trí hành lá, rau mùi.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Bắc Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "450-550 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh chưng": {
        "type": "khô",
        "ingredients": ["gạo nếp", "đậu xanh", "thịt lợn", "lá dong", "hạt tiêu", "muối"],
        "recipe": "Gói gạo nếp, đậu xanh, thịt lợn bằng lá dong, luộc 10-12 giờ, ăn kèm chả lụa hoặc dưa hành.",
        "popular_regions": ["Hà Nội", "Bắc Bộ", "Bắc Giang", "Vĩnh Phúc", "Phú Thọ"],
        "holidays": ["Tết Nguyên Đán"],
        "calories": "700-800 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bánh tét": {
        "type": "khô",
        "ingredients": ["gạo nếp", "đậu xanh", "thịt lợn", "lá chuối", "muối"],
        "recipe": "Gói gạo nếp, đậu xanh, thịt lợn trong lá chuối, luộc 6-8 giờ, ăn kèm dưa hành.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Cần Thơ", "Vĩnh Long"],
        "holidays": ["Tết Nguyên Đán"],
        "calories": "600-700 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bún bò Huế": {
        "type": "nước",
        "ingredients": ["thịt bò", "bún", "nước dùng", "sả", "ớt", "rau thơm", "tiết heo", "chả cua"],
        "recipe": "Nấu nước dùng từ xương bò và sả, thêm bún, thịt bò, tiết heo, chả cua, ăn kèm rau thơm và ớt.",
        "popular_regions": ["Huế", "Đà Nẵng", "Quảng Nam"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bánh xèo": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm", "thịt lợn", "giá đỗ", "hành lá", "nước cốt dừa", "nghệ"],
        "recipe": "Trộn bột gạo với nước cốt dừa và nghệ, chiên với tôm, thịt, giá đỗ, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Cần Thơ", "Vũng Tàu"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cơm tấm": {
        "type": "khô",
        "ingredients": ["tấm", "sườn nướng", "trứng ốp la", "dưa leo", "nước mắm", "hành phi", "bì"],
        "recipe": "Nấu tấm, nướng sườn, chiên trứng, ăn kèm dưa leo, bì và nước mắm ớt.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Đồng Nai", "Bình Dương"],
        "holidays": ["Ngày thường"],
        "calories": "700-800 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bún chả": {
        "type": "khô",
        "ingredients": ["chả nướng", "bún", "nước mắm", "rau sống", "đu đủ muối", "tỏi", "ớt"],
        "recipe": "Nướng chả, nấu nước mắm chua ngọt, ăn kèm bún, rau sống và đu đủ muối.",
        "popular_regions": ["Hà Nội", "Hải Phòng", "Bắc Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh cuốn": {
        "type": "khô",
        "ingredients": ["bột gạo", "thịt băm", "mộc nhĩ", "hành phi", "nước mắm", "rau thơm"],
        "recipe": "Tráng bột gạo thành bánh mỏng, cho nhân thịt băm và mộc nhĩ, cuộn lại, rắc hành phi, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Bắc Bộ", "Lạng Sơn", "Bắc Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Bánh mì": {
        "type": "khô",
        "ingredients": ["bánh mì", "thịt heo", "pate", "dưa leo", "rau mùi", "nước tương", "mayonnaise"],
        "recipe": "Xẻ bánh mì, phết pate, cho thịt heo, dưa leo, rau mùi, thêm nước tương hoặc mayonnaise.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng", "Hải Phòng"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Hủ tiếu": {
        "type": "nước",
        "ingredients": ["hủ tiếu", "thịt heo", "tôm", "hẹ", "nước dùng", "giá đỗ", "chanh"],
        "recipe": "Nấu nước dùng từ xương heo, thêm hủ tiếu, thịt heo, tôm, trang trí hẹ và giá đỗ.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Tiền Giang", "Long An"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Chả lụa": {
        "type": "khô",
        "ingredients": ["thịt heo", "nước mắm", "lá chuối", "tiêu", "tỏi"],
        "recipe": "Xay thịt heo với nước mắm, gói trong lá chuối, hấp chín, ăn kèm bánh mì hoặc cơm.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Hưng Yên", "Quảng Ninh"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bún riêu": {
        "type": "nước",
        "ingredients": ["bún", "cua", "cà chua", "đậu phụ", "rau muống", "mắm tôm", "hành lá"],
        "recipe": "Nấu nước dùng từ cua và cà chua, thêm đậu phụ, bún, ăn kèm rau muống và mắm tôm.",
        "popular_regions": ["Hà Nội", "Bắc Bộ", "Hải Dương", "Hưng Yên"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cao lầu": {
        "type": "khô",
        "ingredients": ["mì cao lầu", "thịt heo", "rau sống", "đậu phộng", "nước mắm", "bánh tráng"],
        "recipe": "Luộc mì cao lầu, thêm thịt heo xá xíu, rau sống, rắc đậu phộng, chấm nước mắm.",
        "popular_regions": ["Hội An", "Đà Nẵng", "Quảng Nam"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Mì Quảng": {
        "type": "nước",
        "ingredients": ["mì Quảng", "tôm", "thịt heo", "đậu phộng", "bánh tráng", "rau răm", "hành lá"],
        "recipe": "Nấu nước dùng với tôm, thịt heo, thêm mì Quảng, đậu phộng, ăn kèm bánh tráng và rau sống.",
        "popular_regions": ["Quảng Nam", "Đà Nẵng", "Quảng Ngãi"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bánh rế": {
        "type": "khô",
        "ingredients": ["bột gạo", "đường", "vừng", "dừa nạo"],
        "recipe": "Trộn bột gạo với đường, chiên thành bánh mỏng, rắc vừng, ăn như món tráng miệng.",
        "popular_regions": ["Miền Tây", "Cần Thơ", "Sóc Trăng"],
        "holidays": ["Trung Thu", "Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Chè ba màu": {
        "type": "nước",
        "ingredients": ["đậu đỏ", "đậu xanh", "nước cốt dừa", "thạch", "đường", "đá"],
        "recipe": "Nấu đậu đỏ, đậu xanh, làm thạch, trộn với nước cốt dừa và đá, ăn lạnh.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Vĩnh Long", "Bến Tre"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Gỏi cuốn": {
        "type": "khô",
        "ingredients": ["bánh tráng", "tôm", "thịt heo", "bún", "rau sống", "tương đậu"],
        "recipe": "Cuốn tôm, thịt heo, bún, rau sống trong bánh tráng, chấm nước mắm hoặc tương đậu.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Vũng Tàu", "Phú Quốc"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Nem chua": {
        "type": "khô",
        "ingredients": ["thịt heo", "bì heo", "tỏi", "ớt", "lá đinh lăng", "lá ổi"],
        "recipe": "Trộn thịt heo xay, bì heo, tỏi, ớt, gói lá chuối, ủ 2-3 ngày, ăn kèm tỏi ớt.",
        "popular_regions": ["Thanh Hóa", "Hà Nội", "Nghệ An", "Hà Tĩnh"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Canh chua": {
        "type": "nước",
        "ingredients": ["cá", "cà chua", "dứa", "rau muống", "me", "ngò gai", "giá đỗ"],
        "recipe": "Nấu nước dùng với me, cà chua, dứa, thêm cá và rau muống, ăn kèm cơm.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Cần Thơ", "An Giang"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Lẩu mắm": {
        "type": "nước",
        "ingredients": ["mắm cá", "thịt heo", "tôm", "cá", "rau", "bún", "nước cốt dừa"],
        "recipe": "Nấu mắm cá với nước, thêm thịt heo, tôm, cá, ăn kèm rau và bún.",
        "popular_regions": ["Miền Tây", "Cần Thơ", "Sóc Trăng", "Kiên Giang"],
        "holidays": ["Ngày thường"],
        "calories": "600-800 kcal",
        "meal_time": ["tối"]
    },
    "Xôi gà": {
        "type": "khô",
        "ingredients": ["gạo nếp", "gà luộc", "hành phi", "muối tiêu", "nước mắm", "chanh"],
        "recipe": "Nấu gạo nếp thành xôi, xé gà luộc, rắc hành phi, ăn kèm muối tiêu chanh.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Sơn La", "Lào Cai"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bún nước lèo": {
        "type": "nước",
        "ingredients": ["bún", "mắm cá", "tôm", "thịt heo", "rau", "hành lá", "sả"],
        "recipe": "Nấu nước dùng từ mắm cá, thêm bún, tôm, thịt heo, ăn kèm rau sống.",
        "popular_regions": ["Miền Tây", "Sóc Trăng", "Kiên Giang", "Cà Mau"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Chả cá Lã Vọng": {
        "type": "khô",
        "ingredients": ["cá lăng", "thì là", "hành lá", "bún", "đậu phộng", "mắm tôm", "nghệ"],
        "recipe": "Ướp cá lăng với nghệ, chiên, xào với thì là và hành lá, ăn kèm bún và đậu phộng.",
        "popular_regions": ["Hà Nội", "Hải Phòng"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh bèo": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm khô", "hành phi", "nước mắm", "ớt", "đường"],
        "recipe": "Hấp bột gạo trong chén nhỏ, thêm tôm khô, hành phi, chấm nước mắm.",
        "popular_regions": ["Huế", "Đà Nẵng", "Quảng Bình"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Bánh khoái": {
        "type": "khô",
        "ingredients": ["bột gạo", "tôm", "thịt", "giá đỗ", "trứng", "nước lèo"],
        "recipe": "Chiên bột gạo với tôm, thịt, giá đỗ, ăn kèm rau sống và nước lèo.",
        "popular_regions": ["Huế", "Đà Nẵng", "Quảng Trị"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh ướt thịt nướng": {
        "type": "khô",
        "ingredients": ["bánh ướt", "thịt nướng", "rau sống", "nước mắm", "hành phi", "dưa leo"],
        "recipe": "Tráng bánh ướt, thêm thịt nướng, rau sống, chấm nước mắm chua ngọt.",
        "popular_regions": ["Huế", "Đà Nẵng", "Đà Lạt"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bún bò Nam Bộ": {
        "type": "khô",
        "ingredients": ["bún", "thịt bò", "rau thơm", "đậu phộng", "nước mắm", "chanh", "tỏi"],
        "recipe": "Xào thịt bò với tỏi, trộn với bún, rau thơm, đậu phộng, chấm nước mắm.",
        "popular_regions": ["Sài Gòn", "Nha Trang", "Bình Dương"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh bột lọc": {
        "type": "khô",
        "ingredients": ["bột sắn", "tôm", "thịt heo", "nước mắm", "hành phi", "ớt"],
        "recipe": "Nhồi bột sắn với tôm, thịt heo, gói lá chuối, hấp chín, chấm nước mắm.",
        "popular_regions": ["Huế", "Quảng Bình", "Quảng Trị"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Chè đậu trắng": {
        "type": "nước",
        "ingredients": ["đậu trắng", "nước cốt dừa", "đường", "gừng", "muối"],
        "recipe": "Nấu đậu trắng với đường, thêm nước cốt dừa, ăn nóng hoặc lạnh.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Bến Tre", "Trà Vinh"],
        "holidays": ["Trung Thu", "Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh canh": {
        "type": "nước",
        "ingredients": ["bánh canh", "tôm", "thịt heo", "nước dùng", "hành lá", "tiêu"],
        "recipe": "Nấu nước dùng từ xương heo, thêm bánh canh, tôm, thịt heo, trang trí hành lá.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Bà Rịa"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh đúc": {
        "type": "khô",
        "ingredients": ["bột gạo", "nước", "muối", "mắm tôm", "thịt rim", "tương ớt"],
        "recipe": "Pha bột gạo với nước, đun sôi đến khi đặc, để nguội, cắt miếng, ăn kèm mắm tôm hoặc thịt rim.",
        "popular_regions": ["Bắc Bộ", "Hà Nội", "Nam Định"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh tráng trộn": {
        "type": "khô",
        "ingredients": ["bánh tráng", "trứng cút", "xoài xanh", "rau răm", "tương ớt", "muối tôm"],
        "recipe": "Cắt bánh tráng thành sợi, trộn với trứng cút, xoài xanh, rau răm, tương ớt và muối tôm.",
        "popular_regions": ["Sài Gòn", "Đà Lạt", "Nha Trang"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["chiều", "tối"]
    },
    "Bánh tráng nướng": {
        "type": "khô",
        "ingredients": ["bánh tráng", "trứng", "hành lá", "tương ớt", "ruốc", "xúc xích"],
        "recipe": "Nướng bánh tráng, đập trứng lên trên, thêm hành lá, tương ớt, ruốc và xúc xích.",
        "popular_regions": ["Đà Lạt", "Sài Gòn", "Nha Trang"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["chiều", "tối"]
    },
    "Bánh căn": {
        "type": "khô",
        "ingredients": ["bột gạo", "trứng", "tôm", "hành lá", "nước mắm", "dầu ăn"],
        "recipe": "Đổ bột gạo vào khuôn, thêm trứng, tôm, hành lá, nướng chín, chấm nước mắm.",
        "popular_regions": ["Nha Trang", "Phan Thiết", "Đà Lạt"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh hỏi": {
        "type": "khô",
        "ingredients": ["bánh hỏi", "thịt heo quay", "hành phi", "nước mắm", "rau thơm"],
        "recipe": "Luộc bánh hỏi, thêm thịt heo quay, rắc hành phi, ăn kèm nước mắm và rau thơm.",
        "popular_regions": ["Bình Định", "Phú Yên", "Ninh Thuận"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bún đậu mắm tôm": {
        "type": "khô",
        "ingredients": ["bún", "đậu hũ", "chả cốm", "nem chua", "mắm tôm", "rau sống"],
        "recipe": "Luộc bún, chiên đậu hũ, ăn kèm chả cốm, nem chua, mắm tôm và rau sống.",
        "popular_regions": ["Hà Nội", "Hải Phòng", "Bắc Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bánh gối": {
        "type": "khô",
        "ingredients": ["bột mì", "thịt heo", "mộc nhĩ", "miến", "hành lá", "nước mắm"],
        "recipe": "Nhồi bột mì, cho nhân thịt heo, mộc nhĩ, miến, gói thành bánh, chiên giòn, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Hải Phòng", "Nam Định"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Cháo lòng": {
        "type": "nước",
        "ingredients": ["gạo tẻ", "lòng heo", "hành lá", "rau mùi", "tiêu", "quẩy"],
        "recipe": "Nấu cháo từ gạo tẻ, thêm lòng heo, trang trí hành lá, rau mùi, ăn kèm quẩy.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Bánh mì xíu mại": {
        "type": "nước",
        "ingredients": ["bánh mì", "xíu mại", "nước dùng", "hành lá", "tiêu"],
        "recipe": "Hấp xíu mại, thả vào nước dùng, ăn kèm bánh mì, rắc hành lá và tiêu.",
        "popular_regions": ["Sài Gòn", "Đà Lạt", "Nha Trang"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh flan": {
        "type": "khô",
        "ingredients": ["trứng", "sữa", "caramen", "vanilla", "đường"],
        "recipe": "Đánh trứng với sữa, đường và vanilla, hấp cách thủy, rưới caramen lên trên.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Chè khúc bạch": {
        "type": "nước",
        "ingredients": ["đậu phụ", "nước đường", "thạch", "nho khô", "đá bào"],
        "recipe": "Làm đậu phụ non, thêm nước đường, thạch, nho khô và đá bào.",
        "popular_regions": ["Hà Nội", "Sài Gòn", "Hải Phòng"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Bánh da lợn": {
        "type": "khô",
        "ingredients": ["bột năng", "đậu xanh", "nước cốt dừa", "đường", "lá dứa"],
        "recipe": "Trộn bột năng với nước cốt dừa và đường, hấp từng lớp với đậu xanh và lá dứa.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Bến Tre"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Bánh chuối": {
        "type": "khô",
        "ingredients": ["chuối", "bột gạo", "nước cốt dừa", "đường", "vừng"],
        "recipe": "Trộn chuối với bột gạo, nướng hoặc hấp, rưới nước cốt dừa, rắc vừng.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Bánh pía": {
        "type": "khô",
        "ingredients": ["bột mì", "đậu xanh", "sầu riêng", "lòng đỏ trứng", "đường"],
        "recipe": "Nhồi bột mì, cho nhân đậu xanh và sầu riêng, nướng với lòng đỏ trứng phết mặt.",
        "popular_regions": ["Sóc Trăng", "Bạc Liêu", "Cần Thơ"],
        "holidays": ["Trung Thu", "Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Bánh phồng tôm": {
        "type": "khô",
        "ingredients": ["tôm", "bột sắn", "đường", "muối", "dầu ăn"],
        "recipe": "Xay tôm với bột sắn, cán mỏng, phơi khô, chiên giòn.",
        "popular_regions": ["Bến Tre", "Tiền Giang", "Sóc Trăng"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["khai vị"]
    },
    "Bánh đa kê": {
        "type": "khô",
        "ingredients": ["bánh đa", "kê", "đường", "nước cốt dừa", "gừng"],
        "recipe": "Nấu kê với đường và gừng, trải lên bánh đa, rưới nước cốt dừa.",
        "popular_regions": ["Hải Phòng", "Quảng Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh cuốn Thanh Trì": {
        "type": "khô",
        "ingredients": ["bột gạo", "hành phi", "nước mắm", "rau thơm"],
        "recipe": "Tráng bột gạo thành bánh mỏng, không nhân, rắc hành phi, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Thanh Trì"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Bánh gai": {
        "type": "khô",
        "ingredients": ["bột nếp", "lá gai", "đậu xanh", "dừa", "đường"],
        "recipe": "Trộn bột nếp với lá gai xay, nhân đậu xanh với dừa, gói lá chuối, hấp chín.",
        "popular_regions": ["Nam Định", "Thái Bình", "Hải Dương"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh rán": {
        "type": "khô",
        "ingredients": ["bột nếp", "đậu xanh", "đường", "mè", "dầu ăn"],
        "recipe": "Nhồi bột nếp, cho nhân đậu xanh, viên tròn, rắc mè, chiên giòn.",
        "popular_regions": ["Hà Nội", "Hải Phòng", "Bắc Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh tôm": {
        "type": "khô",
        "ingredients": ["bột mì", "tôm", "khoai lang", "dầu ăn", "nước mắm"],
        "recipe": "Trộn bột mì với khoai lang thái sợi, thêm tôm, chiên giòn, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Hải Phòng"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh cá": {
        "type": "khô",
        "ingredients": ["bột mì", "cá", "hành lá", "gia vị", "dầu ăn"],
        "recipe": "Trộn bột mì với cá xay, hành lá, chiên thành bánh hình cá, chấm nước mắm.",
        "popular_regions": ["Hải Phòng", "Quảng Ninh"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh bao": {
        "type": "khô",
        "ingredients": ["bột mì", "thịt heo", "trứng cút", "nấm mèo", "hành tây", "gia vị"],
        "recipe": "Nhồi bột mì ủ men, bọc nhân thịt heo xay với nấm mèo, trứng cút, hấp chín.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Hải Phòng", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "250-350 kcal",
        "meal_time": ["sáng", "xế"]
    },
    "Bánh bò": {
        "type": "khô",
        "ingredients": ["bột gạo", "nước cốt dừa", "đường", "men", "lá dứa"],
        "recipe": "Trộn bột gạo với nước cốt dừa, đường và men, ủ lên men, hấp chín.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "tráng miệng"]
    },
    "Bánh đúc nóng": {
        "type": "khô",
        "ingredients": ["bột gạo", "thịt băm", "mộc nhĩ", "hành phi", "nước mắm"],
        "recipe": "Nấu bột gạo thành cháo đặc, rắc thịt băm xào mộc nhĩ, hành phi, chấm nước mắm.",
        "popular_regions": ["Hà Nội", "Bắc Ninh", "Hải Dương"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh khọt": {
        "type": "khô",
        "ingredients": ["bột gạo", "nước cốt dừa", "tôm", "dầu ăn", "nước mắm"],
        "recipe": "Đổ bột vào khuôn nhỏ, thêm tôm, chiên giòn, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Vũng Tàu", "Bà Rịa", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "350-450 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bánh mì chảo": {
        "type": "khô",
        "ingredients": ["bánh mì", "trứng", "chả lụa", "pate", "xúc xích", "nước tương"],
        "recipe": "Chiên trứng, chả lụa, xúc xích ăn kèm bánh mì và pate.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Lạt"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Bánh tằm bì": {
        "type": "khô",
        "ingredients": ["bánh tằm", "bì heo", "nước cốt dừa", "nước mắm", "đậu phộng"],
        "recipe": "Trộn bánh tằm với bì heo, nước cốt dừa, nước mắm và đậu phộng.",
        "popular_regions": ["Sóc Trăng", "Cần Thơ", "Bạc Liêu"],
        "holidays": ["Ngày thường"],
        "calories": "450-550 kcal",
        "meal_time": ["sáng", "trưa"]
    },
    "Bò lá lốt": {
        "type": "khô",
        "ingredients": ["thịt bò", "lá lốt", "gia vị", "bún", "nước mắm"],
        "recipe": "Bọc thịt bò xay trong lá lốt, nướng hoặc chiên, ăn kèm bún và nước mắm.",
        "popular_regions": ["Sài Gòn", "Miền Đông", "Đồng Nai"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bò nướng ngói": {
        "type": "khô",
        "ingredients": ["thịt bò", "sả", "tỏi", "mật ong", "dầu hào", "rau sống"],
        "recipe": "Ướp thịt bò với sả, tỏi, mật ong, nướng trên ngói, ăn kèm rau sống.",
        "popular_regions": ["Đà Lạt", "Sài Gòn", "Nha Trang"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["tối"]
    },
    "Bún mắm": {
        "type": "nước",
        "ingredients": ["bún", "mắm cá", "tôm", "thịt heo", "cà tím", "rau sống"],
        "recipe": "Nấu nước dùng từ mắm cá, thêm tôm, thịt, cà tím, ăn kèm bún và rau.",
        "popular_regions": ["Miền Tây", "Sóc Trăng", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "550-650 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Bún thịt nướng": {
        "type": "khô",
        "ingredients": ["bún", "thịt heo nướng", "rau sống", "nước mắm", "đậu phộng"],
        "recipe": "Xếp bún, thịt nướng, rau sống, rắc đậu phộng, chan nước mắm.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Đà Lạt"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cá kho tộ": {
        "type": "khô",
        "ingredients": ["cá", "nước dừa", "nước mắm", "đường", "tiêu", "ớt"],
        "recipe": "Kho cá với nước dừa, nước mắm, đường trong nồi đất.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Cần Thơ"],
        "holidays": ["Tết Nguyên Đán", "Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cá lóc nướng trui": {
        "type": "khô",
        "ingredients": ["cá lóc", "muối", "ớt", "rau sống", "nước mắm"],
        "recipe": "Nướng cá nguyên con trên than, ăn kèm rau sống và nước mắm.",
        "popular_regions": ["Miền Tây", "Đồng Tháp", "An Giang"],
        "holidays": ["Ngày thường"],
        "calories": "350-450 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cháo gà": {
        "type": "nước",
        "ingredients": ["gạo", "thịt gà", "hành lá", "rau răm", "gừng"],
        "recipe": "Nấu cháo từ gạo và nước luộc gà, thêm thịt gà xé, hành lá, rau răm.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Cháo sườn": {
        "type": "nước",
        "ingredients": ["gạo", "sườn heo", "hành lá", "quẩy", "gia vị"],
        "recipe": "Nấu cháo với sườn heo, thêm hành lá, ăn kèm quẩy.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "450-550 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Chè hạt sen": {
        "type": "nước",
        "ingredients": ["hạt sen", "đường", "lá dứa", "nước cốt dừa"],
        "recipe": "Nấu hạt sen với đường và lá dứa, thêm nước cốt dừa.",
        "popular_regions": ["Huế", "Hà Nội", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Chè thái": {
        "type": "nước",
        "ingredients": ["trái cây thái hạt lựu", "thạch", "nước cốt dừa", "đường", "đá"],
        "recipe": "Trộn các loại trái cây với thạch, nước cốt dừa, đường và đá.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Hà Nội"],
        "holidays": ["Ngày thường"],
        "calories": "350-450 kcal",
        "meal_time": ["tráng miệng"]
    },
    "Cốm": {
        "type": "khô",
        "ingredients": ["cốm non", "đường", "dừa nạo", "muối vừng"],
        "recipe": "Ăn cốm non với chuối, hoặc trộn với đường, dừa nạo.",
        "popular_regions": ["Hà Nội", "Vĩnh Phúc", "Bắc Ninh"],
        "holidays": ["Mùa thu"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "xế"]
    },
    "Cơm gà Hội An": {
        "type": "khô",
        "ingredients": ["gà", "gạo", "nước mắm", "rau răm", "tỏi"],
        "recipe": "Nấu cơm với nước luộc gà, ăn kèm gà xé, rau răm, nước mắm tỏi.",
        "popular_regions": ["Hội An", "Đà Nẵng", "Quảng Nam"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cơm niêu": {
        "type": "khô",
        "ingredients": ["gạo", "nước", "niêu đất", "thịt kho", "cá kho"],
        "recipe": "Nấu cơm trong niêu đất, ăn kèm các món kho.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Huế"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Cơm rang": {
        "type": "khô",
        "ingredients": ["cơm nguội", "trứng", "thịt", "rau củ", "nước tương"],
        "recipe": "Rang cơm với trứng, thịt, rau củ và nước tương.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["sáng", "trưa", "tối"]
    },
    "Gà nướng muối ớt": {
        "type": "khô",
        "ingredients": ["gà", "muối", "ớt", "chanh", "gia vị"],
        "recipe": "Ướp gà với muối ớt, nướng vàng, ăn kèm muối tiêu chanh.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Gỏi đu đủ khô bò": {
        "type": "khô",
        "ingredients": ["đu đủ xanh", "khô bò", "rau răm", "đậu phộng", "nước mắm"],
        "recipe": "Trộn đu đủ bào sợi với khô bò, rau răm, đậu phộng và nước mắm.",
        "popular_regions": ["Sài Gòn", "Đà Lạt", "Nha Trang"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Gỏi ngó sen": {
        "type": "khô",
        "ingredients": ["ngó sen", "tôm", "thịt heo", "rau răm", "nước mắm"],
        "recipe": "Trộn ngó sen với tôm, thịt heo luộc, rau răm và nước mắm.",
        "popular_regions": ["Miền Tây", "Sài Gòn", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "250-350 kcal",
        "meal_time": ["khai vị"]
    },
    "Hột vịt lộn": {
        "type": "khô",
        "ingredients": ["trứng vịt lộn", "rau răm", "gừng", "muối tiêu"],
        "recipe": "Luộc trứng vịt lộn, ăn kèm rau răm, gừng, chấm muối tiêu.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Khoai lang kén": {
        "type": "khô",
        "ingredients": ["khoai lang", "bột mì", "đường", "dầu ăn", "mè"],
        "recipe": "Nghiền khoai lang trộn bột, viên thành kén, chiên giòn, lăn đường mè.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Lạt"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["xế", "tráng miệng"]
    },
    "Mì xào giòn": {
        "type": "khô",
        "ingredients": ["mì vàng", "tôm", "thịt", "rau củ", "nước tương"],
        "recipe": "Chiên mì giòn, xào tôm thịt với rau củ, rưới lên mì.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "600-700 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Nem nướng": {
        "type": "khô",
        "ingredients": ["thịt heo", "gia vị", "bánh tráng", "rau sống", "nước mắm"],
        "recipe": "Nướng nem chua viên, cuốn bánh tráng với rau sống, chấm nước mắm.",
        "popular_regions": ["Nha Trang", "Đà Lạt", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Ốc luộc": {
        "type": "khô",
        "ingredients": ["ốc", "sả", "gừng", "lá chanh", "muối tiêu chanh"],
        "recipe": "Luộc ốc với sả, gừng, lá chanh, chấm muối tiêu chanh.",
        "popular_regions": ["Hà Nội", "Hải Phòng", "Sài Gòn"],
        "holidays": ["Ngày thường"],
        "calories": "200-300 kcal",
        "meal_time": ["tối"]
    },
    "Pizza Việt Nam": {
        "type": "khô",
        "ingredients": ["bột mì", "trứng", "chả lụa", "hành lá", "tương ớt"],
        "recipe": "Tráng bột mì với trứng, rắc chả lụa, hành lá, sốt tương ớt.",
        "popular_regions": ["Sài Gòn", "Hà Nội"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "xế"]
    },
    "Súp cua": {
        "type": "nước",
        "ingredients": ["thịt cua", "trứng", "bắp", "nấm mèo", "hành lá"],
        "recipe": "Nấu súp với thịt cua, trứng, bắp, nấm mèo, thêm hành lá.",
        "popular_regions": ["Sài Gòn", "Hà Nội", "Đà Nẵng"],
        "holidays": ["Ngày thường"],
        "calories": "300-400 kcal",
        "meal_time": ["sáng", "tối"]
    },
    "Sườn xào chua ngọt": {
        "type": "khô",
        "ingredients": ["sườn heo", "cà chua", "dứa", "ớt chuông", "gia vị"],
        "recipe": "Xào sườn với cà chua, dứa, ớt chuông trong sốt chua ngọt.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Ngày thường"],
        "calories": "500-600 kcal",
        "meal_time": ["trưa", "tối"]
    },
    "Xôi chiên phồng": {
        "type": "khô",
        "ingredients": ["xôi", "dầu ăn", "muối", "đường", "mè"],
        "recipe": "Ép xôi thành miếng, chiên phồng, rắc muối đường hoặc mè.",
        "popular_regions": ["Sài Gòn", "Miền Tây", "Cần Thơ"],
        "holidays": ["Ngày thường"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "xế"]
    },
    "Xôi gấc": {
        "type": "khô",
        "ingredients": ["gạo nếp", "gấc", "đường", "dừa nạo"],
        "recipe": "Trộn gạo nếp với thịt gấc, đồ xôi, ăn kèm dừa nạo.",
        "popular_regions": ["Toàn quốc"],
        "holidays": ["Tết Nguyên Đán", "Cưới hỏi"],
        "calories": "400-500 kcal",
        "meal_time": ["sáng", "trưa"]
    }
}

REGIONAL_FOODS = {
    "Hà Nội": ["Phở", "Bún chả", "Bánh cuốn", "Chả cá Lã Vọng", "Chả lụa", "Bún riêu", "Xôi gà", "Bánh tôm", "Bánh rán", "Bánh đúc", "Bún đậu mắm tôm", "Bánh gối", "Bánh cuốn Thanh Trì"],
    "Sài Gòn": ["Bánh xèo", "Cơm tấm", "Hủ tiếu", "Chè ba màu", "Gỏi cuốn", "Bún bò Nam Bộ", "Chè đậu trắng", "Bánh tráng trộn", "Bánh canh", "Bánh flan", "Bánh chuối", "Cháo lòng"],
    "Huế": ["Bún bò Huế", "Bánh bèo", "Bánh khoái", "Bánh ướt thịt nướng", "Bánh bột lọc", "Chè đậu trắng", "Bánh flan"],
    "Đà Nẵng": ["Mì Quảng", "Cao lầu", "Bún bò Huế", "Bánh ướt thịt nướng", "Bánh bèo", "Bánh xèo"],
    "Miền Tây": ["Bánh xèo", "Cơm tấm", "Hủ tiếu", "Bánh rế", "Canh chua", "Lẩu mắm", "Bún nước lèo", "Chè ba màu", "Bánh pía", "Bánh da lợn", "Bánh chuối", "Bánh phồng tôm"],
    "Bắc Bộ": ["Bánh chưng", "Bánh cuốn", "Chả lụa", "Bún riêu", "Bánh đúc", "Bánh gai", "Bánh rán", "Nem chua"],
    "Nam Định": ["Phở", "Bánh gai", "Bánh đúc", "Bánh nhãn", "Kẹo Sìu Châu"],
    "Quảng Nam": ["Mì Quảng", "Cao lầu", "Bánh bột lọc", "Bánh tổ", "Bánh ướt"],
    "Thanh Hóa": ["Nem chua", "Bánh đa", "Cháo lòng"],
    "Hội An": ["Cao lầu", "Bánh bao", "Bánh vạc"],
    "Cần Thơ": ["Bánh xèo", "Canh chua", "Lẩu mắm", "Bún nước lèo", "Bánh tét"],
    "Vũng Tàu": ["Bánh xèo", "Gỏi cuốn", "Hải sản nướng", "Bánh khọt", "Hải sản", "Bún suông", "Bánh xèo"],
    "Phú Quốc": ["Gỏi cuốn", "Bún nước lèo", "Hải sản tươi sống"],
    "Nha Trang": ["Bún bò Nam Bộ", "Bánh căn", "Bánh tráng nướng", "Hải sản", "Bún cá", "Nem nướng"],
    "Đà Lạt": ["Bánh ướt thịt nướng", "Bánh tráng nướng", "Bánh căn", "Dâu tây", "Atisô"],
    "Bình Định": ["Bánh hỏi", "Bánh xèo", "Bún song thằn", "Chả cá"],
    "Quảng Ngãi": ["Mì Quảng", "Bánh tráng nước dừa", "Bánh đậu xanh", "Cá bống sông Trà", "Nem chua"],
    "Hải Phòng": ["Bánh mì", "Chả lụa", "Bánh đa cua", "Bánh cá", "Bánh đa kê"],
    "Quảng Ninh": ["Chả lụa", "Hải sản", "Bánh đa kê", "Bánh cá"],
    "Lạng Sơn": ["Bánh cuốn", "Vịt quay", "Măng ớt"],
    "Bắc Giang": ["Bánh chưng", "Vải thiều", "Mì gạo"],
    "Bắc Ninh": ["Bánh cuốn", "Bánh tẻ", "Bún đậu mắm tôm"],
    "Hưng Yên": ["Chả lụa", "Nhãn lồng", "Bánh gai"],
    "Vĩnh Phúc": ["Bánh chưng", "Bánh giầy", "Thịt chua"],
    "Phú Thọ": ["Bánh chưng", "Cá thính", "Xôi ngũ sắc"],
    "Thái Nguyên": ["Bánh chưng", "Chè Tân Cương", "Bánh trứng kiến"],
    "Sơn La": ["Xôi gà", "Thịt trâu gác bếp", "Mận hậu"],
    "Lào Cai": ["Xôi gà", "Thắng cố", "Cơm lam"],
    "Yên Bái": ["Xôi gà", "Cơm lam", "Măng đắng"],
    "Điện Biên": ["Xôi gà", "Cơm lam", "Pa pỉnh tộp"],
    "Hòa Bình": ["Bánh chưng", "Cá nướng", "Rượu cần"],
    "Tây Ninh": ["Bánh xèo", "Bánh tráng phơi sương", "Mãng cầu", "Hủ tiếu"],
    "Long An": ["Canh chua", "Lẩu mắm", "Dừa", "Lẩu mắm", "Bún gỏi dà", "Khô cá lóc"],
    "Tiền Giang": ["Hủ tiếu", "Trái cây", "Bánh phồng tôm", "Mắm tôm chua"],
    "Kiên Giang": ["Bún nước lèo", "Hải sản", "Nước mắm Phú Quốc", "Khô mực"],
    "An Giang": ["Lẩu mắm", "Bún cá", "Mắm cá linh", "Bánh bò", "Khô cá sặc"],
    "Đồng Tháp": ["Lẩu mắm", "Cá lóc nướng trui", "Hoa sen", "Quýt hồng"],
    "Bến Tre": ["Chè đậu trắng", "Bánh da lợn", "Kẹo dừa", "Mắm cá"],
    "Trà Vinh": ["Chè đậu trắng", "Bánh tét", "Mắm bò hóc", "Bún nước lèo"],
    "Sóc Trăng": ["Bún nước lèo", "Bánh pía", "Lẩu mắm", "Bánh tằm bì"],
    "Bạc Liêu": ["Bánh pía", "Hủ tiếu", "Cua biển", "Mắm ba khía"],
    "Cà Mau": ["Bún nước lèo", "Tôm khô", "Mắm ba khía", "Cá thòi lòi"],
    "Ninh Thuận": ["Bánh hỏi", "Nho", "Thịt cừu", "Mắm cá"],
    "Bình Thuận": ["Bánh căn", "Hải sản", "Thanh long", "Bánh xèo"],
    "Hà Giang": ["Thắng cố", "Cơm lam", "Mèn mén", "Lợn cắp nách"],
    "Cao Bằng": ["Phở chua", "Vịt quay", "Bánh cuốn chan", "Khâu nhục"],
    "Bắc Kạn": ["Cá hồ", "Rêu đá", "Măng đá", "Cơm lam"],
    "Tuyên Quang": ["Cá sông Lô", "Thịt chua", "Xôi ngũ sắc", "Bánh gai"],
    "Thái Bình": ["Bánh cáy", "Bánh gai", "Canh cá diếc", "Bún bung"],
    "Ninh Bình": ["Cơm cháy", "Dê núi Ninh Bình", "Ốc núi", "Miến lươn"],
    "Hà Nam": ["Bún đậu", "Chả cá", "Bánh cuốn", "Nem chua"],
    "Nghệ An": ["Nem chua", "Bánh mướt", "Cháo lươn", "Nhút Thanh Chương"],
    "Hà Tĩnh": ["Kẹo cu đơ", "Bánh bèo", "Bánh đa", "Nước mắm"],
    "Quảng Bình": ["Bánh bột lọc", "Cháo canh", "Bánh xèo", "Hải sản"],
    "Quảng Trị": ["Bánh khoái", "Bánh ướt", "Bún bò", "Cơm hến"],
    "Thừa Thiên Huế": ["Bún bò Huế", "Bánh bèo", "Cơm hến", "Chè Huế"],
    "Phú Yên": ["Bánh canh", "Bánh hỏi", "Hải sản", "Chả cá"],
    "Khánh Hòa": ["Bún cá", "Bánh căn", "Nem nướng", "Hải sản"],
    "Kon Tum": ["Cơm lam", "Thịt nướng", "Rượu cần", "Măng rừng"],
    "Gia Lai": ["Cơm lam", "Gà nướng", "Rượu cần", "Phở khô"],
    "Đắk Lắk": ["Cơm lam", "Bò nướng", "Cà phê", "Rượu cần"],
    "Đắk Nông": ["Cơm lam", "Thịt thú rừng", "Mật ong", "Rượu cần"],
    "Lâm Đồng": ["Bánh ướt", "Bánh tráng nướng", "Dâu tây", "Atisô"],
    "Bình Phước": ["Bánh canh", "Bún thịt nướng", "Hạt điều", "Trái cây"],
    "Bình Dương": ["Bún thịt nướng", "Bánh bèo", "Bánh xèo", "Cơm tấm"],
    "Đồng Nai": ["Bò lá lốt", "Bún thịt nướng", "Bánh canh", "Hủ tiếu"],
}


HOLIDAYS = {
    "Tết Nguyên Đán": (1, 1, 1, 10),      # Mùng 1-10 tháng 1 âm lịch
    "Tết Hàn Thực": (3, 3, 3, 3),         # Ngày 3 tháng 3 âm lịch
    "Giỗ Tổ Hùng Vương": (3, 10, 3, 10),  # Ngày 10 tháng 3 âm lịch
    "Phật Đản": (4, 15, 4, 15),           # Ngày 15 tháng 4 âm lịch
    "Vu Lan": (7, 15, 7, 15),             # Ngày 15 tháng 7 âm lịch
    "Trung Thu": (8, 15, 8, 15),          # Ngày 15 tháng 8 âm lịch
    "Ông Táo chầu trời": (12, 23, 12, 23), # Ngày 23 tháng 12 âm lịch
    #"Ngày thường": (1, 1, 12, 31)         # Các ngày không phải lễ
    "Tết Nguyên Tiêu": (1, 15, 1, 15),    # Rằm tháng Giêng
    "Tết Thanh Minh": (3, 3, 3, 10),      # Tiết Thanh Minh (3-10/3 âm lịch)
    "Tết Đoan Ngọ": (5, 5, 5, 5),         # Mùng 5 tháng 5 âm lịch
    "Tết Trùng Cửu": (9, 9, 9, 9),        # Mùng 9 tháng 9 âm lịch
    "Tết Trùng Thập": (10, 10, 10, 10),   # Mùng 10 tháng 10 âm lịch
    "Tết Táo Quân": (12, 23, 12, 23),     # Ông Táo chầu trời
    "Rằm tháng Giêng": (1, 15, 1, 15),
    "Rằm tháng Bảy": (7, 15, 7, 15),
    "Rằm tháng Mười": (10, 15, 10, 15)
}
