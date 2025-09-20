Alfred Vị Việt
Alfred Vị Việt là bot Telegram thông minh giúp bạn khám phá ẩm thực Việt Nam với các gợi ý món ăn theo ngày lễ, thời gian trong ngày, loại món, vùng miền, hoặc nguyên liệu. Bot hỗ trợ nhập liệu không dấu và bắt lỗi chính tả, tích hợp database để lưu món yêu thích, và giao diện người dùng với inline keyboard. Với 29 món ăn và 35 vùng miền, bot mang đến trải nghiệm cá nhân hóa. Chạy trên Flask, hỗ trợ SQLite và PostgreSQL, không phụ thuộc API ngoài trừ lunarcalendar cho ngày lễ.
Tính năng chính

Gợi ý món ăn thông minh (/suggest [khô/nước]):

Gợi ý món ngẫu nhiên từ 29 món, ưu tiên theo:
Ngày lễ: Tết Nguyên Đán (bánh chưng, bánh tét), Trung Thu (bánh rế, chè đậu trắng), Ngày thường (bất kỳ).
Thời gian: Sáng (bánh mì, xôi gà), trưa (cơm tấm, mì Quảng), tối (lẩu mắm, bánh xèo).
Loại món: Khô (bánh xèo) hoặc nước (phở) nếu nhập /suggest khô hoặc /suggest nước.
Lịch sử: Tránh lặp 10 món gần nhất.


Hiển thị chi tiết: loại, nguyên liệu, cách làm, vùng, dịp, calo.
Inline keyboard: Xem công thức, gợi ý khác, lưu món.


Món theo vùng (/region [tên vùng]):

Gợi ý món từ 35 vùng (Hà Nội, Sài Gòn, Huế, v.v.).
Hỗ trợ không dấu và bắt lỗi chính tả (ví dụ: "sai gon" → "Sài Gòn").


Món theo nguyên liệu (/ingredient [nguyên liệu1, nguyên liệu2]):

Gợi ý món từ nguyên liệu, hỗ trợ không dấu (ví dụ: "thit bo").
Inline keyboard: Xem công thức, gợi ý khác, lưu món.


Món theo vị trí (/location [tên vùng] hoặc GPS):

Gợi ý món theo vùng nhập (hỗ trợ không dấu) hoặc GPS (hiện giả lập vùng "Sài Gòn").


Lưu món yêu thích (/save [món]):

Lưu tối đa 10 món vào database, hỗ trợ không dấu (ví dụ: /save pho).


Xem món yêu thích (/favorites):

Hiển thị danh sách món yêu thích với inline keyboard.


Tra món (gửi tên món):

Gửi tên món (có dấu hoặc không, ví dụ: "Phở" hoặc "pho") để xem chi tiết và nút lưu.


Ủng hộ bot (/donate):

Hiển thị link donate (PayPal, Momo) qua inline keyboard.


Hỗ trợ không dấu và bắt lỗi chính tả:

Nhận diện vùng và món ăn dù nhập không dấu hoặc sai chính tả (ví dụ: "pho" → "Phở", "banh xeo" → "Bánh xèo").
Dùng fuzzy matching (Levenshtein distance) với ngưỡng 3 ký tự.


Database:

Lưu lịch sử gợi ý (eaten_foods) và món yêu thích (favorite_foods), giới hạn 10 món/user.
Hỗ trợ SQLite (local) và PostgreSQL (Render).


Hỗ trợ calo: Ước tính calo mỗi món.

Ngày lễ: Gợi ý món theo Tết, Trung Thu (dùng lunarcalendar).

Thời gian: Gợi ý món theo sáng, trưa, tối.


Dữ liệu

29 món ăn: Phở, Bánh chưng, Bún bò Huế, Bánh xèo, Cơm tấm, Bún chả, Bánh cuốn, Bánh mì, Hủ tiếu, Chả lụa, Bún riêu, Cao lầu, Mì Quảng, Bánh rế, Chè ba màu, Gỏi cuốn, Nem chua, Bánh tét, Canh chua, Lẩu mắm, Xôi gà, Bún nước lèo, Chả cá Lã Vọng, Bánh bèo, Bánh khoái, Bánh ướt thịt nướng, Bún bò Nam Bộ, Bánh bột lọc, Chè đậu trắng.
35 vùng miền: Hà Nội, Sài Gòn, Huế, Đà Nẵng, Miền Tây, Bắc Bộ, Nam Định, Quảng Nam, Thanh Hóa, Hội An, Cần Thơ, Vũng Tàu, Phú Quốc, Nha Trang, Đà Lạt, Bình Định, Quảng Ngãi, Hải Phòng, Quảng Ninh, Lạng Sơn, Bắc Giang, Bắc Ninh, Hưng Yên, Vĩnh Phúc, Phú Thọ, Thái Nguyên, Sơn La, Lào Cai, Yên Bái, Điện Biên, Hòa Bình, Tây Ninh, Long An, Tiền Giang, Kiên Giang.

Cài đặt
Yêu cầu

Python 3.8+
Thư viện (xem requirements.txt):Flask==2.3.3
python-telegram-bot==20.7
gunicorn==21.2.0
gevent==21.8.0
pg8000==1.30.3
lunarcalendar==0.0.9



Cài đặt local

Clone repository:git clone https://github.com/your_username/alfred-vi-viet.git
cd alfred-vi-viet


Tạo virtual environment:python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Cài thư viện:pip install -r requirements.txt


Đặt biến môi trường:export TELEGRAM_BOT_TOKEN="your_bot_token"  # Linux/Mac
set TELEGRAM_BOT_TOKEN="your_bot_token"     # Windows
export PORT=10000


Chạy bot:python alfred_bot.py



Deploy trên Render

Fork repository trên GitHub.
Tạo service trên Render:
Chọn Web Service, liên kết với repository.
Environment: Python.
Start command: gunicorn -w 4 -k gevent --bind 0.0.0.0:$PORT alfred_bot:flask_app.


Thêm biến môi trường:
TELEGRAM_BOT_TOKEN: Token từ @BotFather.
WEBHOOK_URL: https://your-service.onrender.com.
DATABASE_URL: URL PostgreSQL (hoặc dùng SQLite mặc định).
PORT: 10000.


Deploy: Chọn "Manual Deploy" > "Clear build cache & deploy".
Đặt webhook:curl -X POST https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://your-service.onrender.com/webhook



Sử dụng

Tìm bot trên Telegram: @AlfredViViet (thay bằng tên thật sau khi tạo).
Gửi lệnh:
/start: Xem hướng dẫn.
/suggest: Gợi ý món ngẫu nhiên.
/suggest khô: Gợi ý món khô.
/region Hà Nội hoặc sai gon: Món theo vùng.
/ingredient thịt bò hoặc thit bo: Món từ nguyên liệu.
/location Sài Gòn hoặc sai gon: Món theo vùng.
/save Phở hoặc pho: Lưu món.
/favorites: Xem món yêu thích.
/donate: Ủng hộ bot.
Gửi "Phở" hoặc "pho": Xem chi tiết món.


Nhấn nút inline để tương tác.

Đóng góp

Báo lỗi: Mở issue trên GitHub.
Thêm món/vùng: Sửa foods_data.py, tạo pull request.
Cải tiến: Đề xuất tính năng qua issue hoặc pull request.
Donate: Gửi qua PayPal (https://paypal.me/your_link) hoặc Momo (https://me.momo.vn/your_id).

Giấy phép
MIT License. Xem LICENSE để biết thêm chi tiết.
Liên hệ

Telegram: @YourTelegram
Email: your_email@example.com
