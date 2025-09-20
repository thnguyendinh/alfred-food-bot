# -*- coding: utf-8 -*-
import random

VIETNAMESE_FOODS = {
    "Phở": {
        "type": "nước",
        "ingredients": [
            "xương bò",
            "thịt bò tái/chín",
            "bánh phở",
            "hành lá",
            "rau mùi",
            "quế",
            "hồi",
            "gừng",
            "hành tây",
            "chanh",
            "ớt",
            "nước mắm"
        ],
        "recipe": "Chần xương bò, hầm nước dùng 6-8 giờ cùng gừng, hành tây nướng, quế, hồi. Trụng bánh phở, thái thịt, xếp vào bát, chan nước dùng, thêm hành, rau mùi, chanh, ớt.",
        "popular_regions": [
            "Hà Nội",
            "Nam Định",
            "Hải Phòng"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "500-600 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Bún chả": {
        "type": "khô",
        "ingredients": [
            "thịt ba chỉ",
            "chả nướng",
            "bún tươi",
            "nước mắm",
            "đường",
            "tỏi",
            "ớt",
            "rau sống"
        ],
        "recipe": "Ướp thịt, nướng trên than; làm chả viên; pha nước mắm chua ngọt; ăn kèm bún và rau sống.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-550 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún bò Huế": {
        "type": "nước",
        "ingredients": [
            "xương heo",
            "thịt bò",
            "bún",
            "mắm ruốc",
            "sả",
            "ớt",
            "hành",
            "rau răm"
        ],
        "recipe": "Hầm xương và sả, nêm mắm ruốc, thêm thịt bò và bún, gia vị sa tế tạo vị cay đặc trưng.",
        "popular_regions": [
            "Huế",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "550-650 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Cơm tấm": {
        "type": "khô",
        "ingredients": [
            "gạo tấm",
            "sườn nướng",
            "bì",
            "chả",
            "trứng ốp la",
            "nước mắm",
            "dưa leo"
        ],
        "recipe": "Nấu cơm tấm; ướp và nướng sườn; chuẩn bị bì, chả; xếp lên dĩa, chan nước mắm.",
        "popular_regions": [
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-750 kcal/đĩa",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Hủ tiếu": {
        "type": "nước",
        "ingredients": [
            "xương heo",
            "hủ tiếu sợi",
            "tôm",
            "thịt heo",
            "hẹ",
            "giá đỗ"
        ],
        "recipe": "Nấu nước dùng từ xương; trụng hủ tiếu; xếp tôm, thịt; chan nước dùng, rắc hành, giá.",
        "popular_regions": [
            "Miền Nam",
            "Cần Thơ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh chưng": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đậu xanh",
            "thịt lợn",
            "lá dong",
            "hạt tiêu"
        ],
        "recipe": "Ngâm gạo và đậu; ướp thịt; gói bánh bằng lá dong; luộc 8-12 giờ; để nguội mới ăn.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "700-900 kcal/cái vừa",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Gỏi cuốn": {
        "type": "khô",
        "ingredients": [
            "bánh tráng",
            "tôm",
            "thịt heo",
            "bún tươi",
            "rau sống",
            "húng quế"
        ],
        "recipe": "Luộc tôm, luộc thịt; cuốn cùng bún và rau trong bánh tráng; chấm tương hoặc nước mắm.",
        "popular_regions": [
            "Miền Nam",
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "70-120 kcal/cuốn (tùy kích thước)",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh xèo": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "nước cốt dừa",
            "tôm",
            "thịt",
            "giá",
            "hành lá"
        ],
        "recipe": "Pha bột với nước cốt dừa, nghệ; đổ chảo, thêm nhân tôm-thịt-giá; chiên giòn, ăn kèm rau và nước mắm.",
        "popular_regions": [
            "Miền Nam",
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-800 kcal/phần lớn",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh mì": {
        "type": "khô",
        "ingredients": [
            "bánh mì",
            "pate",
            "thịt nguội/thịt nướng",
            "dưa leo",
            "đồ chua",
            "ngò"
        ],
        "recipe": "Xẻ bánh, phết pate, thêm thịt, đồ chua, rau, sốt tuỳ chọn.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-700 kcal/ổ (tùy nhân)",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Bún riêu": {
        "type": "nước",
        "ingredients": [
            "cua đồng",
            "bún",
            "cà chua",
            "đậu phụ",
            "rau muống"
        ],
        "recipe": "Nấu nước dùng từ cua và cà chua; thêm đậu phụ; ăn với bún và rau sống, mắm tôm tuỳ khẩu vị.",
        "popular_regions": [
            "Hà Nội",
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Cao lầu": {
        "type": "khô",
        "ingredients": [
            "mì cao lầu",
            "thịt heo xá xíu",
            "rau sống",
            "đậu phộng",
            "nước lèo ít"
        ],
        "recipe": "Luộc mì; xếp thịt xá xíu, rau và đậu phộng; ăn gần giống mì trộn với ít nước dùng.",
        "popular_regions": [
            "Hội An",
            "Quảng Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Mì Quảng": {
        "type": "nước",
        "ingredients": [
            "mì Quảng",
            "tôm",
            "thịt heo",
            "đậu phộng",
            "rau sống",
            "bánh tráng"
        ],
        "recipe": "Nấu nước dùng cô đặc; bày mì, thịt, tôm; rắc đậu phộng, ăn kèm rau và bánh tráng.",
        "popular_regions": [
            "Quảng Nam",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-700 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh cuốn": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "thịt băm",
            "mộc nhĩ",
            "hành phi",
            "nước mắm"
        ],
        "recipe": "Tráng lớp bánh mỏng, cho nhân thịt-mộc nhĩ, cuộn; rắc hành phi; chấm nước mắm pha.",
        "popular_regions": [
            "Hà Nội",
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-450 kcal/đĩa",
        "meal_time": [
            "sáng"
        ]
    },
    "Chả lụa": {
        "type": "khô",
        "ingredients": [
            "thịt heo xay",
            "nước mắm",
            "lá chuối"
        ],
        "recipe": "Xay thịt nhuyễn, trộn gia vị, gói lá chuối, hấp chín; cắt lát dùng kèm bánh mì hoặc cơm.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "300-400 kcal/100g",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh bèo": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "tôm khô",
            "hành phi",
            "nước mắm"
        ],
        "recipe": "Hấp bột gạo trong chén nhỏ, rắc tôm khô và hành phi; chấm nước mắm.",
        "popular_regions": [
            "Huế"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-300 kcal/phần",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh bột lọc": {
        "type": "khô",
        "ingredients": [
            "bột sắn",
            "tôm",
            "thịt",
            "lá chuối"
        ],
        "recipe": "Nhồi bột sắn, cho tôm-thịt vào gói lá, hấp; bóc ăn với nước mắm.",
        "popular_regions": [
            "Huế",
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-300 kcal/2-3 cái",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh tét": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đậu xanh",
            "thịt lợn",
            "lá chuối"
        ],
        "recipe": "Gói gạo nếp, đậu, thịt vào lá chuối; luộc 6-8 giờ; ăn kèm dưa hành.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "600-800 kcal/cây vừa",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Bánh rán": {
        "type": "khô",
        "ingredients": [
            "bột nếp",
            "đậu xanh",
            "đường",
            "dầu ăn"
        ],
        "recipe": "Nhồi bột nếp với nhân đậu xanh, viên, chiên ngập dầu đến vàng.",
        "popular_regions": [
            "Miền Bắc"
        ],
        "holidays": [
            "Trung Thu",
            "Ngày thường"
        ],
        "calories": "150-250 kcal/chiếc",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Nem chua": {
        "type": "khô",
        "ingredients": [
            "thịt heo xay",
            "bì heo",
            "tỏi",
            "ớt",
            "lá chuối"
        ],
        "recipe": "Trộn thịt với gia vị, gói lá, ủ lên men 2-3 ngày; ăn kèm tỏi ớt.",
        "popular_regions": [
            "Thanh Hóa",
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "200-300 kcal/100g",
        "meal_time": [
            "ăn vặt",
            "nhậu"
        ]
    },
    "Xôi gà": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "gà xé",
            "hành phi",
            "muối tiêu"
        ],
        "recipe": "Nấu xôi; xé thịt gà luộc, ướp gia vị; rắc hành phi, ăn nóng.",
        "popular_regions": [
            "Hà Nội",
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-650 kcal/phần",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Chè ba màu": {
        "type": "nước",
        "ingredients": [
            "đậu đỏ",
            "đậu xanh",
            "nước cốt dừa",
            "thạch",
            "đường"
        ],
        "recipe": "Nấu các loại đậu; làm thạch; xếp lớp, thêm nước cốt dừa và đá; ăn lạnh.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "250-350 kcal/cốc",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Chè đậu trắng": {
        "type": "nước",
        "ingredients": [
            "đậu trắng",
            "nước cốt dừa",
            "đường"
        ],
        "recipe": "Nấu đậu trắng mềm; thêm đường và nước cốt dừa; ăn nóng hoặc lạnh.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Trung Thu",
            "Ngày thường"
        ],
        "calories": "200-300 kcal/cốc",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Canh chua": {
        "type": "nước",
        "ingredients": [
            "cá",
            "cà chua",
            "dứa",
            "rau muống",
            "me",
            "hành"
        ],
        "recipe": "Nấu nước dùng chua từ me, thêm cá và rau, nêm vừa ăn; ăn kèm cơm.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-350 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Lẩu mắm": {
        "type": "nước",
        "ingredients": [
            "mắm cá",
            "tôm",
            "cá",
            "thịt heo",
            "rau ăn lẩu",
            "bún"
        ],
        "recipe": "Nấu nước lẩu với mắm cá; chuẩn bị hải sản và rau; ăn kèm bún hoặc cơm.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-900 kcal/suất ăn chung",
        "meal_time": [
            "tối"
        ]
    },
    "Bún nước lèo": {
        "type": "nước",
        "ingredients": [
            "mắm cá",
            "bún",
            "tôm",
            "thịt heo",
            "rau sống"
        ],
        "recipe": "Nấu nước dùng mắm cá đặc trưng vùng miền; ăn kèm bún và rau sống.",
        "popular_regions": [
            "Miền Tây",
            "Kiên Giang"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Chả cá Lã Vọng": {
        "type": "khô",
        "ingredients": [
            "cá lăng hoặc cá chép",
            "thì là",
            "riềng",
            "hành",
            "bún",
            "đậu phộng"
        ],
        "recipe": "Ướp cá với gia vị, chiên/xào cùng thì là; ăn kèm bún và lạc rang.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún bò Nam Bộ": {
        "type": "khô",
        "ingredients": [
            "bún",
            "thịt bò",
            "rau thơm",
            "đậu phộng",
            "nước mắm"
        ],
        "recipe": "Xào thịt bò; trộn với bún, rau, nước mắm và đậu phộng rang.",
        "popular_regions": [
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh rế": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "đường",
            "vừng",
            "dầu ăn"
        ],
        "recipe": "Nhào bột, cán mỏng và chiên, rắc đường và vừng khi còn nóng.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Trung Thu",
            "Ngày thường"
        ],
        "calories": "200-300 kcal/chiếc",
        "meal_time": [
            "tráng miệng",
            "ăn vặt"
        ]
    },
    "Bánh khoái": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "tôm",
            "thịt",
            "giá đỗ",
            "hành"
        ],
        "recipe": "Đổ bột giống bánh xèo nhưng dày hơn; thêm nhân tôm-thịt-giá; chiên vàng, ăn kèm nước lèo.",
        "popular_regions": [
            "Huế"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh ướt thịt nướng": {
        "type": "khô",
        "ingredients": [
            "bánh ướt",
            "thịt nướng",
            "rau sống",
            "nước mắm"
        ],
        "recipe": "Tráng bánh ướt; thêm thịt nướng thái lát; cuốn hoặc ăn kèm rau và nước mắm.",
        "popular_regions": [
            "Huế",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-500 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Bánh mì Hội An": {
        "type": "khô",
        "ingredients": [
            "bánh mì",
            "patê",
            "chà bông",
            "xá xíu",
            "rau thơm",
            "nước sốt đặc trưng"
        ],
        "recipe": "Nhân phong phú, bánh mì thường mềm vỏ mỏng; ăn làm món đường phố.",
        "popular_regions": [
            "Hội An",
            "Quảng Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/ổ",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh mì que": {
        "type": "khô",
        "ingredients": [
            "bột mì",
            "nhân xúc xích",
            "bơ",
            "phô mai"
        ],
        "recipe": "Làm bánh mì dài nhỏ, nướng hoặc chiên; thường bán hàng quà vặt.",
        "popular_regions": [
            "Sài Gòn",
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "150-300 kcal/chiếc",
        "meal_time": [
            "ăn vặt"
        ]
    },
    "Bún mắm": {
        "type": "nước",
        "ingredients": [
            "mắm",
            "bún",
            "hải sản",
            "thịt heo",
            "rau sống"
        ],
        "recipe": "Nấu nước mắm đặc trưng miền Tây; thêm hải sản và thịt; bày bún với rau sống.",
        "popular_regions": [
            "Miền Tây",
            "Cần Thơ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-700 kcal/tô",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh cuốn Thanh Trì": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "thịt băm",
            "mộc nhĩ",
            "hành phi",
            "nước mắm"
        ],
        "recipe": "Tráng mỏng, cuộn nhân thịt mộc nhĩ; ăn kèm chả và nước mắm.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-450 kcal/đĩa",
        "meal_time": [
            "sáng"
        ]
    },
    "Ốc luộc": {
        "type": "khô",
        "ingredients": [
            "ốc",
            "sả",
            "gừng",
            "chanh",
            "tỏi ớt"
        ],
        "recipe": "Luộc ốc với sả; chấm muối tiêu chanh hoặc nước mắm gừng.",
        "popular_regions": [
            "Đà Nẵng",
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "150-300 kcal/phần",
        "meal_time": [
            "ăn vặt",
            "tối"
        ]
    },
    "Bánh nậm": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "tôm",
            "thịt",
            "lá dong"
        ],
        "recipe": "Tráng bột mỏng, cho nhân tôm-thịt, gói lá, hấp chín.",
        "popular_regions": [
            "Huế"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "150-250 kcal/cái",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bò kho": {
        "type": "khô",
        "ingredients": [
            "thịt bò",
            "cà rốt",
            "bánh mì",
            "gia vị kho",
            "cà chua"
        ],
        "recipe": "Hầm bò với gia vị (ngũ vị hương, hành tỏi, cà chua) cho đến mềm; ăn kèm bánh mì hoặc bún.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-800 kcal/phần",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Gà nướng mật ong": {
        "type": "khô",
        "ingredients": [
            "gà",
            "mật ong",
            "tỏi",
            "nước mắm",
            "tiêu"
        ],
        "recipe": "Ướp gà với mật ong và gia vị; nướng đến chín vàng, thơm.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày lễ gia đình",
            "Ngày thường"
        ],
        "calories": "500-700 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Sườn nướng": {
        "type": "khô",
        "ingredients": [
            "sườn heo",
            "nước mắm",
            "tỏi",
            "mật ong",
            "tiêu"
        ],
        "recipe": "Ướp sườn; nướng than hoặc lò đến chín và caramel hóa.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-800 kcal/đĩa",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Cá kho tộ": {
        "type": "khô",
        "ingredients": [
            "cá",
            "nước mắm",
            "đường",
            "tiêu",
            "hành"
        ],
        "recipe": "Kho cá trong nồi đất với nước mắm và đường đến khi sốt sánh, cá thấm vị.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Thịt kho tàu": {
        "type": "khô",
        "ingredients": [
            "thịt ba chỉ",
            "trứng vịt",
            "nước dừa",
            "đường",
            "nước mắm"
        ],
        "recipe": "Kho thịt và trứng với nước dừa và gia vị đến khi thấm và nước cạn sánh.",
        "popular_regions": [
            "Miền Nam",
            "Toàn quốc"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "600-900 kcal/đĩa",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Xôi vò": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đậu xanh",
            "đường",
            "hành phi"
        ],
        "recipe": "Nấu xôi; rắc đậu xanh giã và hành phi lên trên; ăn nóng.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "sáng"
        ]
    },
    "Bánh giò": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "thịt băm",
            "mộc nhĩ",
            "lá chuối"
        ],
        "recipe": "Nhồi bột, cho nhân thịt-mộc nhĩ, gói bằng lá, hấp chín.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "250-350 kcal/chiếc",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh đa cua": {
        "type": "nước",
        "ingredients": [
            "cua đồng",
            "bún",
            "rau sống",
            "tôm",
            "măng"
        ],
        "recipe": "Nấu nước dùng từ cua; thêm măng, tôm; ăn với bún và rau sống.",
        "popular_regions": [
            "Hải Phòng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Bún thang": {
        "type": "nước",
        "ingredients": [
            "gà xé",
            "giò lụa",
            "trứng rán",
            "bún tươi",
            "nước dùng gà"
        ],
        "recipe": "Chuẩn bị nước dùng gà trong, xếp gà xé, giò, trứng rán băm lên bún, chan nước dùng, rắc rau thơm.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường",
            "Tết Nguyên Đán"
        ],
        "calories": "400-550 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh cáy": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đường",
            "mạch nha",
            "vừng"
        ],
        "recipe": "Trộn gạo nếp và mạch nha, nướng/chiên mỏng, cắt miếng; là món quà truyền thống.",
        "popular_regions": [
            "Thái Bình",
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "200-350 kcal/miếng",
        "meal_time": [
            "ăn vặt",
            "tráng miệng"
        ]
    },
    "Bánh gai": {
        "type": "khô",
        "ingredients": [
            "bột nếp",
            "lá gai",
            "đậu xanh",
            "mứt",
            "dừa"
        ],
        "recipe": "Nhào bột với lá gai, cho nhân đậu xanh, gói lá, hấp chín.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "250-400 kcal/cái",
        "meal_time": [
            "sáng",
            "tráng miệng"
        ]
    },
    "Bún ốc": {
        "type": "nước",
        "ingredients": [
            "ốc",
            "bún",
            "cà chua",
            "măng chua",
            "rau mùi"
        ],
        "recipe": "Nấu nước dùng chua; luộc ốc; ăn cùng bún và rau, thêm giấm hoặc me nếu thích.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-500 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Xôi xéo": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đậu xanh",
            "hành tím phi",
            "mỡ"
        ],
        "recipe": "Nấu xôi; rắc đậu xanh giã và hành phi lên trên; ăn nóng.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "sáng"
        ]
    },
    "Bánh khọt": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "tôm",
            "dầu ăn",
            "nước cốt dừa"
        ],
        "recipe": "Đổ khuôn nhỏ, cho tôm, chiên vàng; ăn kèm rau và nước mắm chua ngọt.",
        "popular_regions": [
            "Vũng Tàu",
            "Miền Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-500 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh hỏi": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "mỡ hành",
            "thịt nướng",
            "rau thơm"
        ],
        "recipe": "Tráng mỏng sợi bột thành miếng mỏng (bánh hỏi); rắc mỡ hành và ăn với thịt nướng.",
        "popular_regions": [
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-450 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Bánh cuốn chả mỡ": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "thịt băm",
            "mộc nhĩ",
            "chả mỡ",
            "nước mắm"
        ],
        "recipe": "Tráng bánh, cuộn nhân, ăn kèm chả mỡ và nước mắm pha.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-450 kcal/đĩa",
        "meal_time": [
            "sáng"
        ]
    },
    "Bánh bao": {
        "type": "khô",
        "ingredients": [
            "bột mì",
            "thịt băm",
            "trứng",
            "mộc nhĩ"
        ],
        "recipe": "Nhồi bột; vo nhân thịt; hấp chín; ăn nóng.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-500 kcal/chiếc lớn",
        "meal_time": [
            "sáng",
            "ăn vặt"
        ]
    },
    "Bánh chuối chiên": {
        "type": "khô",
        "ingredients": [
            "chuối",
            "bột mì",
            "đường",
            "dầu ăn"
        ],
        "recipe": "Lăn chuối qua bột và đường, chiên vàng; ăn nóng như món tráng miệng.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-400 kcal/phần",
        "meal_time": [
            "tráng miệng",
            "ăn vặt"
        ]
    },
    "Bánh cam": {
        "type": "khô",
        "ingredients": [
            "bột nếp",
            "đậu xanh",
            "đường",
            "vừng"
        ],
        "recipe": "Nhân đậu xanh, bọc bột nếp, chiên ngập dầu; lăn vừng.",
        "popular_regions": [
            "Miền Bắc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-300 kcal/chiếc",
        "meal_time": [
            "ăn vặt"
        ]
    },
    "Bún đậu mắm tôm": {
        "type": "khô",
        "ingredients": [
            "bún",
            "đậu phụ rán",
            "thịt luộc",
            "rau sống",
            "mắm tôm",
            "chanh",
            "tỏi"
        ],
        "recipe": "Bày bún, đậu rán, thịt luộc và rau; chấm mắm tôm đã đánh với chanh, tỏi.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún măng vịt": {
        "type": "nước",
        "ingredients": [
            "vịt",
            "măng",
            "bún",
            "hành",
            "gia vị"
        ],
        "recipe": "Hầm vịt và măng; nêm gia vị; ăn với bún và hành lá.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-650 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Mực chiên giòn": {
        "type": "khô",
        "ingredients": [
            "mực",
            "bột chiên",
            "tỏi ớt",
            "chanh"
        ],
        "recipe": "Tẩm bột mực và chiên giòn; ăn kèm nước chấm chua ngọt hoặc muối tiêu chanh.",
        "popular_regions": [
            "Đà Nẵng",
            "Nha Trang"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-450 kcal/phần",
        "meal_time": [
            "tối",
            "ăn vặt"
        ]
    },
    "Gỏi đu đủ": {
        "type": "khô",
        "ingredients": [
            "đu đủ xanh",
            "tôm khô",
            "đậu phộng",
            "nước mắm",
            "ớt",
            "tỏi"
        ],
        "recipe": "Bào đu đủ, trộn với tôm khô, đậu phộng và nước mắm chua ngọt; ăn kèm rau thơm.",
        "popular_regions": [
            "Miền Nam",
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "150-250 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh hỏi lòng heo": {
        "type": "khô",
        "ingredients": [
            "bánh hỏi",
            "lòng heo",
            "rau thơm",
            "mắm nêm"
        ],
        "recipe": "Chế biến lòng heo luộc hoặc nướng; ăn kèm bánh hỏi và mắm nêm.",
        "popular_regions": [
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh ướt": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "nhân thịt nướng",
            "rau thơm",
            "nước mắm"
        ],
        "recipe": "Tráng bánh ướt mỏng; xếp nhân thịt nướng; chấm nước mắm.",
        "popular_regions": [
            "Huế",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-450 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Cháo lòng": {
        "type": "nước",
        "ingredients": [
            "gạo",
            "lòng heo",
            "rau răm",
            "hành"
        ],
        "recipe": "Nấu cháo nhuyễn; thêm lòng luộc thái lát; nêm gia vị và rắc hành, rau răm.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-500 kcal/phần",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bún kèn": {
        "type": "nước",
        "ingredients": [
            "cá",
            "bún",
            "cà",
            "đậu",
            "rau sống"
        ],
        "recipe": "Món súp cá đặc trưng miền Tây; nấu nước dùng cay và chua nhẹ; ăn kèm bún.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-650 kcal/tô",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún cá": {
        "type": "nước",
        "ingredients": [
            "cá",
            "bún",
            "cà chua",
            "thì là",
            "rau sống"
        ],
        "recipe": "Nấu nước dùng cá; cho bún và cá; thêm thì là và rau sống.",
        "popular_regions": [
            "Quảng Ninh",
            "Hải Phòng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Gà luộc": {
        "type": "khô",
        "ingredients": [
            "gà",
            "muối",
            "gừng",
            "rau sống"
        ],
        "recipe": "Luộc gà vừa chín tới; chặt miếng; ăn kèm nước mắm gừng hoặc muối tiêu chanh.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày lễ gia đình",
            "Tết Nguyên Đán"
        ],
        "calories": "300-500 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Nem rán": {
        "type": "khô",
        "ingredients": [
            "bánh tráng",
            "thịt băm",
            "mộc nhĩ",
            "miến",
            "cà rốt"
        ],
        "recipe": "Cuốn nhân trong bánh tráng; chiên giòn; ăn với rau sống và nước chấm.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "200-400 kcal/chiếc",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh dừa nướng": {
        "type": "khô",
        "ingredients": [
            "dừa",
            "bột gạo",
            "đường"
        ],
        "recipe": "Trộn dừa với bột và đường, nướng đến chín vàng; ăn tráng miệng.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "150-300 kcal/miếng",
        "meal_time": [
            "tráng miệng"
        ]
    },
    "Bánh tằm bì": {
        "type": "khô",
        "ingredients": [
            "bánh tằm",
            "bì",
            "đậu phộng",
            "nước mắm",
            "rau sống"
        ],
        "recipe": "Trộn bánh tằm với bì, đậu phộng và nước mắm; ăn kèm rau sống.",
        "popular_regions": [
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Bánh ít lá gai": {
        "type": "khô",
        "ingredients": [
            "bột nếp",
            "lá gai",
            "đậu xanh",
            "dừa"
        ],
        "recipe": "Làm vỏ bột lá gai, cho nhân đậu xanh-dừa, gói lá, hấp chín.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "200-350 kcal/cái",
        "meal_time": [
            "ăn vặt",
            "tráng miệng"
        ]
    },
    "Bánh tôm Hồ Tây": {
        "type": "khô",
        "ingredients": [
            "tôm",
            "bột chiên",
            "rau thơm",
            "nước chấm"
        ],
        "recipe": "Tẩm bột tôm và chiên giòn; ăn kèm rau và nước chấm.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-500 kcal/phần",
        "meal_time": [
            "ăn vặt",
            "tối"
        ]
    },
    "Lươn um": {
        "type": "khô",
        "ingredients": [
            "lươn",
            "lá lốt",
            "gia vị",
            "cà chua"
        ],
        "recipe": "Ướp và um lươn cùng lá lốt hoặc cà chua; mùi vị đậm đà.",
        "popular_regions": [
            "Miền Bắc",
            "Miền Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-600 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún chả cá": {
        "type": "nước",
        "ingredients": [
            "chả cá",
            "bún",
            "rau thơm",
            "nước mắm"
        ],
        "recipe": "Chiên chả cá; nấu nước dùng nhẹ; ăn với bún và rau.",
        "popular_regions": [
            "Đà Nẵng",
            "Nha Trang"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-550 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Cơm cháy chà bông": {
        "type": "khô",
        "ingredients": [
            "cơm",
            "dầu ăn",
            "chà bông",
            "nước mắm"
        ],
        "recipe": "Nướng hoặc chiên cơm đến giòn; rắc chà bông và sốt mặn ngọt.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-500 kcal/phần",
        "meal_time": [
            "ăn vặt"
        ]
    },
    "Bò nướng lá lốt": {
        "type": "khô",
        "ingredients": [
            "thịt bò băm",
            "lá lốt",
            "tỏi",
            "hành"
        ],
        "recipe": "Cuốn thịt bò băm vào lá lốt, nướng đến thơm; ăn kèm bún và rau sống.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-450 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Gỏi cuốn tôm thịt miền Trung": {
        "type": "khô",
        "ingredients": [
            "bánh tráng",
            "tôm",
            "thịt",
            "rau sống",
            "bún"
        ],
        "recipe": "Cuốn tôm và thịt cùng rau; chấm nước mắm hoặc tương.",
        "popular_regions": [
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "70-120 kcal/cuốn",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh mì chảo": {
        "type": "khô",
        "ingredients": [
            "trứng",
            "xúc xích",
            "pate",
            "bánh mì",
            "phô mai"
        ],
        "recipe": "Chiên trứng và xúc xích trên chảo nhỏ; ăn kèm bánh mì.",
        "popular_regions": [
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-800 kcal/phần",
        "meal_time": [
            "sáng",
            "brunch"
        ]
    },
    "Bún ốc giấm": {
        "type": "nước",
        "ingredients": [
            "ốc",
            "bún",
            "giấm bỗng",
            "rau thơm"
        ],
        "recipe": "Nấu ốc với nước chua nhẹ; ăn cùng bún và rau thơm.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-500 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Bún thịt nướng": {
        "type": "khô",
        "ingredients": [
            "bún",
            "thịt nướng",
            "rau sống",
            "đậu phộng",
            "nước mắm"
        ],
        "recipe": "Nướng thịt; trộn bún với nước mắm, rau và đậu phộng rang.",
        "popular_regions": [
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-650 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Cá nướng trui": {
        "type": "khô",
        "ingredients": [
            "cá sông",
            "muối",
            "lá chuối",
            "rau sống"
        ],
        "recipe": "Nướng cá trên lửa than trực tiếp (trui); ăn với rau sống và nước chấm mặn.",
        "popular_regions": [
            "Miền Bắc",
            "Miền Trung"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "300-500 kcal/phần",
        "meal_time": [
            "tối"
        ]
    },
    "Bún bò Huế chay": {
        "type": "nước",
        "ingredients": [
            "nấm",
            "bún",
            "sả",
            "rau thơm",
            "gia vị chay"
        ],
        "recipe": "Dùng nấm và rau củ nấu nước dùng thay thế xương và thịt, nêm gia vị chay.",
        "popular_regions": [
            "Huế",
            "thành phố lớn"
        ],
        "holidays": [
            "Ngày rằm",
            "Ngày chay"
        ],
        "calories": "300-450 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    },
    "Chè kho": {
        "type": "nước",
        "ingredients": [
            "đậu xanh",
            "đường",
            "dừa khô",
            "muối"
        ],
        "recipe": "Nấu đậu xanh với đường đến sệt; ăn ấm hoặc để nguội.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "300-400 kcal/cốc",
        "meal_time": [
            "tráng miệng"
        ]
    },
    "Bún riêu cua miền Nam": {
        "type": "nước",
        "ingredients": [
            "cua",
            "bún",
            "cà chua",
            "rau thơm",
            "mắm"
        ],
        "recipe": "Nấu nước dùng từ cua và cà chua; thêm đậu phụ và rau sống; khẩu vị nhẹ nhàng hơn phiên bản Bắc.",
        "popular_regions": [
            "Miền Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "trưa"
        ]
    }
}

REGIONAL_FOODS = {
    "Hà Nội": [
        "Phở",
        "Bún chả",
        "Bánh cuốn",
        "Bún thang",
        "Bún ốc",
        "Bánh tôm Hồ Tây",
        "Xôi xéo",
        "Bánh cuốn chả mỡ",
        "Bún đậu mắm tôm",
        "Bún ốc giấm"
    ],
    "Hải Phòng": [
        "Bánh đa cua",
        "Bánh mì",
        "Cháo lòng",
        "Bún cá"
    ],
    "Nam Định": [
        "Phở",
        "Bún chả"
    ],
    "Quảng Ninh": [
        "Bún cá"
    ],
    "Huế": [
        "Bún bò Huế",
        "Bánh bèo",
        "Bánh nậm",
        "Bánh khoái",
        "Bánh ướt thịt nướng",
        "Bánh ướt",
        "Bún bò Huế chay"
    ],
    "Đà Nẵng": [
        "Mì Quảng",
        "Bánh mì Hội An",
        "Bún chả cá",
        "Bánh ướt thịt nướng",
        "Bánh ướt",
        "Mực chiên giòn"
    ],
    "Quảng Nam": [
        "Cao lầu",
        "Mì Quảng",
        "Bánh mì Hội An"
    ],
    "Hội An": [
        "Cao lầu",
        "Bánh mì Hội An"
    ],
    "Quảng Ngãi": [
        "Mì Quảng"
    ],
    "Nha Trang": [
        "Bún cá",
        "Bún chả cá",
        "Mực chiên giòn"
    ],
    "Sài Gòn": [
        "Cơm tấm",
        "Bánh mì",
        "Hủ tiếu",
        "Bánh xèo",
        "Bún bò Nam Bộ",
        "Bánh mì que",
        "Bánh mì chảo",
        "Bún thịt nướng"
    ],
    "Cần Thơ": [
        "Hủ tiếu",
        "Bún mắm",
        "Lẩu mắm"
    ],
    "Miền Tây": [
        "Canh chua",
        "Lẩu mắm",
        "Bánh xèo",
        "Bún nước lèo",
        "Bánh tằm bì",
        "Bánh dừa nướng",
        "Bún kèn"
    ],
    "Bắc Bộ": [
        "Phở",
        "Bánh chưng",
        "Bánh cuốn",
        "Cháo新一

System: Dựa trên dữ liệu mới được cung cấp và yêu cầu chuẩn hóa lại `foods_data.py`, em đã tạo một file mới với artifact ID `7ac53331-1359-4d53-87b1-7eb424808a23`, giữ nguyên cấu trúc cũ (bao gồm `HOLIDAYS` với định dạng ngày tháng) và tích hợp các món ăn, vùng, và thông tin từ dữ liệu mới. Các mục thừa như "món chay", "bánh ngọt", v.v. đã được loại bỏ hoặc thay thế bằng các món cụ thể có trong `VIETNAMESE_FOODS`. Dưới đây là những thay đổi chính:

1. **VIETNAMESE_FOODS**: 
   - Bổ sung tất cả 60 món từ dữ liệu mới, giữ nguyên cấu trúc với các trường `type`, `ingredients`, `recipe`, `popular_regions`, `holidays`, `calories`, `meal_time`.
   - Đảm bảo tính nhất quán, ví dụ: đổi "Thịt kho tàu (thịt kho hột vịt)" thành "Thịt kho tàu" để ngắn gọn, "Bánh rán (bánh cam)" thành "Bánh cam" để tránh trùng lặp.

2. **REGIONAL_FOODS**:
   - Mở rộng danh sách vùng từ dữ liệu mới (thêm Quảng Ngãi, Nha Trang, v.v.) và cập nhật các món ăn tương ứng, loại bỏ "Hải sản" vì không cụ thể.
   - Đảm bảo mọi món trong `REGIONAL_FOODS` đều có trong `VIETNAMESE_FOODS`.

3. **HOLIDAYS**:
   - Khôi phục cấu trúc cũ với tuple `(month_start, day_start, month_end, day_end)` để tương thích với hàm `suggest` trong `alfred_bot.py`.
   - Loại bỏ các mục không cụ thể như "Các món ăn gia đình", "Bánh ngọt", "Món chay truyền thống", v.v., và thay bằng các món cụ thể từ `VIETNAMESE_FOODS`.
   - Gán ngày tháng thực tế cho các ngày lễ dựa trên lịch âm/dương Việt Nam (ví dụ: Tết Nguyên Đán từ mùng 1-7 tháng 1 âm lịch).

### File foods_data.py đã chuẩn hóa

<xaiArtifact artifact_id="7ac53331-1359-4d53-87b1-7eb424808a23" artifact_version_id="4ee13d34-151e-416b-ab9c-fb8419a37df1" title="foods_data.py" contentType="text/python">
# -*- coding: utf-8 -*-
import random

VIETNAMESE_FOODS = {
    "Phở": {
        "type": "nước",
        "ingredients": [
            "xương bò",
            "thịt bò tái/chín",
            "bánh phở",
            "hành lá",
            "rau mùi",
            "quế",
            "hồi",
            "gừng",
            "hành tây",
            "chanh",
            "ớt",
            "nước mắm"
        ],
        "recipe": "Chần xương bò, hầm nước dùng 6-8 giờ cùng gừng, hành tây nướng, quế, hồi. Trụng bánh phở, thái thịt, xếp vào bát, chan nước dùng, thêm hành, rau mùi, chanh, ớt.",
        "popular_regions": [
            "Hà Nội",
            "Nam Định",
            "Hải Phòng"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "500-600 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Bún chả": {
        "type": "khô",
        "ingredients": [
            "thịt ba chỉ",
            "chả nướng",
            "bún tươi",
            "nước mắm",
            "đường",
            "tỏi",
            "ớt",
            "rau sống"
        ],
        "recipe": "Ướp thịt, nướng trên than; làm chả viên; pha nước mắm chua ngọt; ăn kèm bún và rau sống.",
        "popular_regions": [
            "Hà Nội"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-550 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bún bò Huế": {
        "type": "nước",
        "ingredients": [
            "xương heo",
            "thịt bò",
            "bún",
            "mắm ruốc",
            "sả",
            "ớt",
            "hành",
            "rau răm"
        ],
        "recipe": "Hầm xương và sả, nêm mắm ruốc, thêm thịt bò và bún, gia vị sa tế tạo vị cay đặc trưng.",
        "popular_regions": [
            "Huế",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "550-650 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Cơm tấm": {
        "type": "khô",
        "ingredients": [
            "gạo tấm",
            "sườn nướng",
            "bì",
            "chả",
            "trứng ốp la",
            "nước mắm",
            "dưa leo"
        ],
        "recipe": "Nấu cơm tấm; ướp và nướng sườn; chuẩn bị bì, chả; xếp lên dĩa, chan nước mắm.",
        "popular_regions": [
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-750 kcal/đĩa",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Hủ tiếu": {
        "type": "nước",
        "ingredients": [
            "xương heo",
            "hủ tiếu sợi",
            "tôm",
            "thịt heo",
            "hẹ",
            "giá đỗ"
        ],
        "recipe": "Nấu nước dùng từ xương; trụng hủ tiếu; xếp tôm, thịt; chan nước dùng, rắc hành, giá.",
        "popular_regions": [
            "Miền Nam",
            "Cần Thơ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh chưng": {
        "type": "khô",
        "ingredients": [
            "gạo nếp",
            "đậu xanh",
            "thịt lợn",
            "lá dong",
            "hạt tiêu"
        ],
        "recipe": "Ngâm gạo và đậu; ướp thịt; gói bánh bằng lá dong; luộc 8-12 giờ; để nguội mới ăn.",
        "popular_regions": [
            "Bắc Bộ"
        ],
        "holidays": [
            "Tết Nguyên Đán"
        ],
        "calories": "700-900 kcal/cái vừa",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Gỏi cuốn": {
        "type": "khô",
        "ingredients": [
            "bánh tráng",
            "tôm",
            "thịt heo",
            "bún tươi",
            "rau sống",
            "húng quế"
        ],
        "recipe": "Luộc tôm, luộc thịt; cuốn cùng bún và rau trong bánh tráng; chấm tương hoặc nước mắm.",
        "popular_regions": [
            "Miền Nam",
            "Sài Gòn"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "70-120 kcal/cuốn",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh xèo": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "nước cốt dừa",
            "tôm",
            "thịt",
            "giá",
            "hành lá"
        ],
        "recipe": "Pha bột với nước cốt dừa, nghệ; đổ chảo, thêm nhân tôm-thịt-giá; chiên giòn, ăn kèm rau và nước mắm.",
        "popular_regions": [
            "Miền Nam",
            "Miền Tây"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "600-800 kcal/phần lớn",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh mì": {
        "type": "khô",
        "ingredients": [
            "bánh mì",
            "pate",
            "thịt nguội/thịt nướng",
            "dưa leo",
            "đồ chua",
            "ngò"
        ],
        "recipe": "Xẻ bánh, phết pate, thêm thịt, đồ chua, rau, sốt tùy chọn.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "400-700 kcal/ổ",
        "meal_time": [
            "sáng",
            "trưa",
            "tối"
        ]
    },
    "Bún riêu": {
        "type": "nước",
        "ingredients": [
            "cua đồng",
            "bún",
            "cà chua",
            "đậu phụ",
            "rau muống"
        ],
        "recipe": "Nấu nước dùng từ cua và cà chua; thêm đậu phụ; ăn với bún và rau sống, mắm tôm tùy khẩu vị.",
        "popular_regions": [
            "Hà Nội",
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/tô",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Cao lầu": {
        "type": "khô",
        "ingredients": [
            "mì cao lầu",
            "thịt heo xá xíu",
            "rau sống",
            "đậu phộng",
            "nước lèo ít"
        ],
        "recipe": "Luộc mì; xếp thịt xá xíu, rau và đậu phộng; ăn gần giống mì trộn với ít nước dùng.",
        "popular_regions": [
            "Hội An",
            "Quảng Nam"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "450-600 kcal/phần",
        "meal_time": [
            "trưa"
        ]
    },
    "Mì Quảng": {
        "type": "nước",
        "ingredients": [
            "mì Quảng",
            "tôm",
            "thịt heo",
            "đậu phộng",
            "rau sống",
            "bánh tráng"
        ],
        "recipe": "Nấu nước dùng cô đặc; bày mì, thịt, tôm; rắc đậu phộng, ăn kèm rau và bánh tráng.",
        "popular_regions": [
            "Quảng Nam",
            "Đà Nẵng"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "500-700 kcal/phần",
        "meal_time": [
            "trưa",
            "tối"
        ]
    },
    "Bánh cuốn": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "thịt băm",
            "mộc nhĩ",
            "hành phi",
            "nước mắm"
        ],
        "recipe": "Tráng lớp bánh mỏng, cho nhân thịt-mộc nhĩ, cuộn; rắc hành phi; chấm nước mắm pha.",
        "popular_regions": [
            "Hà Nội",
            "Bắc Bộ"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "350-450 kcal/đĩa",
        "meal_time": [
            "sáng"
        ]
    },
    "Chả lụa": {
        "type": "khô",
        "ingredients": [
            "thịt heo xay",
            "nước mắm",
            "lá chuối"
        ],
        "recipe": "Xay thịt nhuyễn, trộn gia vị, gói lá chuối, hấp chín; cắt lát dùng kèm bánh mì hoặc cơm.",
        "popular_regions": [
            "Toàn quốc"
        ],
        "holidays": [
            "Tết Nguyên Đán",
            "Ngày thường"
        ],
        "calories": "300-400 kcal/100g",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh bèo": {
        "type": "khô",
        "ingredients": [
            "bột gạo",
            "tôm khô",
            "hành phi",
            "nước mắm"
        ],
        "recipe": "Hấp bột gạo trong chén nhỏ, rắc tôm khô và hành phi; chấm nước mắm.",
        "popular_regions": [
            "Huế"
        ],
        "holidays": [
            "Ngày thường"
        ],
        "calories": "200-300 kcal/phần",
        "meal_time": [
            "sáng",
            "trưa"
        ]
    },
    "Bánh bột lọc": {
        "type": "khô",
        "ingredients": [
            "
