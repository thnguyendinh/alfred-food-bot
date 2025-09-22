# Alfred Bot

**Alfred Bot** là một bot Telegram thông minh, giúp bạn khám phá ẩm thực Việt Nam với các tính năng gợi ý món ăn, lưu quán ăn yêu thích, và hơn thế nữa. Bot sử dụng MongoDB Atlas để lưu trữ dữ liệu bền vững và SQLite làm dự phòng, đảm bảo không mất dữ liệu sau khi triển khai lại. Username bot: @alfred_foot_bot

## Tính năng nổi bật
- **Gợi ý món ăn (`/suggest`)**: Đề xuất món ăn Việt Nam ngẫu nhiên, tránh trùng với 15 món bạn đã ăn gần đây.
- **Tìm món theo dịp lễ (`/holiday`)**: Gợi ý món phù hợp với các ngày lễ như Tết Nguyên Đán. Nhập `/holiday` để xem danh sách lễ.
- **Quản lý món yêu thích (`/favorites`)**: Lưu, xem, và xóa món ăn yêu thích của bạn.
- **Lưu và quản lý quán ăn (`/restaurant`, `/myrestaurants`)**: 
  - Lưu quán ăn với vị trí GPS, đánh giá, và nhận xét.
  - Xem top 20 quán ăn được đánh giá cao nhất từ cộng đồng.
  - Xóa quán ăn đã lưu từ danh sách cá nhân (`/myrestaurants`).
- **Tìm quán gần đây**: Gửi vị trí GPS để tìm các quán ăn trong vòng 1km.

## Yêu cầu cài đặt
1. **Python 3.11.9** và các thư viện:
   ```plaintext
   Flask==2.3.3
   python-telegram-bot==20.7
   gunicorn==21.2.0
   pg8000==1.30.3
   httpx==0.25.2
   lunarcalendar==0.0.9
   geopy==2.4.1
   pymongo==4.6.3
   ```
2. **MongoDB Atlas**:
   - Tạo cluster miễn phí tại [mongodb.com/atlas](https://www.mongodb.com/atlas).
   - Thiết lập biến môi trường `MONGODB_URI` với connection string (ví dụ: `mongodb+srv://user:pass@cluster0.mongodb.net/alfred_bot`).
3. **Token Telegram Bot**: Lấy từ BotFather và đặt vào biến môi trường `BOT_TOKEN`.

## Cài đặt và triển khai
1. Clone repository và cài đặt thư viện:
   ```bash
   git clone <repository_url>
   cd alfred-bot
   pip install -r requirements.txt
   ```
2. Thiết lập biến môi trường:
   - `BOT_TOKEN`: Token từ BotFather.
   - `MONGODB_URI`: Connection string từ MongoDB Atlas.
   - `DB_PATH` (tùy chọn): Đường dẫn SQLite dự phòng (mặc định: `alfred.db`).
3. Chạy bot cục bộ:
   ```bash
   python alfred_bot.py
   ```
4. Triển khai trên Render:
   - Tạo Web Service, chọn Python, thêm biến môi trường.
   - Push code và deploy.

## Hướng dẫn sử dụng
- `/start`: Bắt đầu và xem hướng dẫn.
- `/suggest`: Gợi ý món ăn mới.
- `/holiday [tên lễ]`: Tìm món phù hợp với dịp lễ.
- `/favorites`: Xem/xóa món yêu thích.
- `/restaurant`: Xem top 20 quán ăn được đánh giá cao.
- `/myrestaurants`: Quản lý quán ăn của bạn (thêm/xóa).
- Gửi vị trí GPS để lưu quán hoặc tìm quán gần.

## Lưu ý
- Dữ liệu được lưu trên MongoDB Atlas, đảm bảo không mất khi redeploy.
- Mỗi người dùng chỉ lưu tối đa 15 món ăn gần nhất trong lịch sử.
- Hỗ trợ SQLite fallback nếu không có MongoDB.
- Telegram: @thnguyendinh