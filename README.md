# 🐍 Enhanced Snake Game

Một phiên bản nâng cao của game Snake cổ điển với nhiều tính năng mới và thú vị!

## ✨ Tính năng mới

### 🎮 Gameplay nâng cao
- **Hệ thống mạng sống**: Snake có 3 mạng sống thay vì game over ngay lập tức
- **Nhiều level**: Độ khó tăng dần qua các level với chướng ngại vật

### 🍎 Hệ thống thức ăn đa dạng
- **Thức ăn bình thường** (đỏ): +10 điểm
- **Thức ăn đặc biệt** (vàng): +50 điểm, hiếm hơn
- **Thức ăn có hại** (tím): -20 điểm và làm ngắn rắn, cẩn thận!

### ⚡ Power-ups thú vị
- **Làm chậm** (cam): Di chuyển chậm lại trong 5 giây
- **Xuyên tường** (xám): Có thể đi qua tường trong 5 giây

### 🧱 Chướng ngại vật
- **Đa dạng chướng ngại vật**: Tường, gai, băng, lửa với độ khó tăng dần theo level

### 🎨 Giao diện đẹp mắt
- **Menu chính**: Start, Select Level, Settings, High Scores, Achievements, Quit
- **Chọn độ khó**: 5 level từ Easy đến Master với số chướng ngại vật và tốc độ khác nhau
- **Cài đặt**: Điều chỉnh FPS và màu sắc snake
- **High Scores**: Lưu điểm cao nhất
- **Achievement System**: Hệ thống thành tựu hybrid với notifications
- **Countdown**: 3-2-1 trước khi bắt đầu game
- **Hiệu ứng hình ảnh**: Animation và hiệu ứng đẹp mắt

## 🚀 Cài đặt và chạy game

### Yêu cầu hệ thống
- Python 3.7+
- Pygame 2.0+

### Cài đặt
1. Clone repository hoặc tải file về
2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### Chạy game
```bash
python game.py
```

## 🎮 Cách chơi

### Điều khiển
- **WASD** hoặc **Arrow Keys**: Di chuyển snake
- **SPACE**: Tạm dừng/tiếp tục game
- **ESC**: Quay về menu chính
- **Mouse**: Click để tương tác với menu, hover để highlight

### Mục tiêu
- Ăn thức ăn để tăng điểm và độ dài
- Tránh chướng ngại vật và không tự cắn mình
- Sống sót qua nhiều level nhất có thể
- Thu thập power-ups để có lợi thế

### Cơ chế game
- **5 độ khó**: Easy (0 chướng ngại vật), Normal (2), Hard (4), Expert (6), Master (8)
- **Tốc độ tăng dần**: Từ 1.0x đến 3.0x theo level
- **Snake có 3 mạng sống**, mất mạng khi va chạm
- **Power-ups xuất hiện ngẫu nhiên** trên màn hình
- **Chọn level trước khi chơi** thay vì tích lũy điểm

## ⚙️ Cài đặt

Trong menu Settings, bạn có thể điều chỉnh:
- **FPS**: Tốc độ khung hình (5-60)
- **Màu sắc Snake**: Chọn từ 6 màu khác nhau
- Tất cả cài đặt được lưu tự động
- Kích thước màn hình cố định 1000x700 (tối ưu nhất)



## 🌟 Điểm nổi bật

- **🏆 Hybrid Achievement System**: Kết hợp session và persistent achievements độc đáo
- **🔔 Real-time Notifications**: Popup animations khi unlock achievements
- **⚙️ Lives System**: 3 mạng sống thay vì game over ngay lập tức
- **🎮 Dual Input Support**: Hỗ trợ đồng thời keyboard và mouse
- **⚡ Performance Optimized**: Font caching, fixed screen size (1000x700)
- **🏢 Clean Architecture**: Cấu trúc modular dễ bảo trì (Core/Entities/UI)

## 🏆 Hệ thống Achievement

### 🎯 **Hybrid Achievement System**
Game có **17 achievements** chia làm 2 loại:

#### 🔄 **Session Achievements** (6 thành tựu - Màu cam)
- **Reset mỗi game** - Tạo thử thách mới mỗi lần chơi
- **VD**: Speed Demon, Survivor, Perfectionist, Collector...

#### 💾 **Persistent Achievements** (11 thành tựu - Màu xanh)
- **Lưu lâu dài** - Tiến trình không bị mất
- **VD**: First Blood, High Roller, Veteran, Dedication...

### 🔔 **Features**
- **Real-time notifications** với slide-in animation
- **2 sections riêng biệt** trong Achievement Menu
- **Color coding** để phân biệt loại achievement
- **Progress tracking** và unlock time

*💡 Xem chi tiết tất cả achievements trong game!*

## 🏆 Bảng điểm cao

Game tự động lưu 10 điểm cao nhất với thông tin:
- Điểm số
- Level đạt được
- Thời gian chơi

## 🐛 Khắc phục sự cố

Nếu gặp lỗi:
1. Đảm bảo đã cài đặt pygame: `pip install pygame`
2. Kiểm tra phiên bản Python: `python --version`
3. Xóa file `config.json` để khôi phục cài đặt mặc định
4. Chạy lại game

---

**Chúc bạn chơi game vui vẻ! 🎮**
