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
- **Tường cố định**: Các khối tường cần tránh
- **Gai nhọn**: Chướng ngại vật nguy hiểm
- **Băng**: Chướng ngại vật băng giá
- **Lửa**: Chướng ngại vật lửa

### 🎨 Giao diện đẹp mắt
- **Menu chính**: Start, Select Level, Settings, High Scores, Quit
- **Chọn độ khó**: 5 level từ Easy đến Master với số chướng ngại vật và tốc độ khác nhau
- **Cài đặt**: Điều chỉnh FPS, màu sắc, kích thước màn hình
- **High Scores**: Lưu điểm cao nhất
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
- **Kích thước màn hình**: 600x400 đến 1280x720
- **Màu sắc**: Màu snake và background
- Tất cả cài đặt được lưu tự động

## 📁 Cấu trúc project

```
snakegame/
├── game.py              # File chính chạy game
├── components/          # Thư mục components
│   ├── core/           # Core system
│   │   ├── config.py   # Quản lý cài đặt
│   │   ├── game_state.py # Quản lý trạng thái game
│   │   ├── event_handler.py # Xử lý sự kiện
│   │   ├── game_renderer.py # Hệ thống render
│   │   ├── game_engine.py # Engine cơ bản
│   │   └── __init__.py
│   ├── entities/       # Game objects
│   │   ├── snake.py    # Class Snake
│   │   ├── food.py     # Hệ thống thức ăn
│   │   ├── powerup.py  # Hệ thống power-up
│   │   ├── obstacle.py # Hệ thống chướng ngại vật
│   │   └── __init__.py
│   └── ui/            # User interface
│       ├── base_menu.py     # Base menu class
│       ├── game_menus.py    # Main/Level/GameOver menus
│       ├── settings_menu.py # Settings menu
│       ├── score_menu.py    # High score menu
│       └── __init__.py
├── requirements.txt     # Dependencies
├── README.md           # Hướng dẫn này
├── config.json         # File cài đặt (tự tạo)
└── high_scores.json    # Điểm cao (tự tạo)
```

## 🌟 Điểm khác biệt

- **Timer-based Food System**: Thức ăn đặc biệt và có hại xuất hiện theo thời gian với visual warnings
- **Power-up Animations**: Hiệu ứng glow, pulse và fade với math-based animations
- **Dual Input Support**: Hỗ trợ đồng thời keyboard và mouse cho UX tốt nhất
- **Lives System**: 3 mạng sống thay vì game over ngay - tạo gameplay strategy
- **Level-based Obstacles**: Chướng ngại vật tăng dần theo độ khó được chọn
- **Clean Architecture**: Cấu trúc theo industry standards (Core/Entities/UI)

## ⚡ Hiệu suất

- **Font Caching**: Cache fonts trong countdown để tránh tạo lại mỗi frame
- **Tối ưu Rendering**: Giảm tạo surface và các thao tác alpha blending
- **Xử lý lỗi**: Xử lý lỗi mạnh mẽ cho độ ổn định cao
- **Tiết kiệm bộ nhớ**: Quản lý đối tượng thông minh và phát hiện va chạm
- **Animation mượt mà**: Gameplay 60 FPS với các lệnh vẽ được tối ưu

## 🎯 Tính năng kỹ thuật

- **Clean Architecture**: Cấu trúc components rõ ràng (Core, Entities, UI)
- **Object-Oriented Programming**: Sử dụng OOP với inheritance và encapsulation
- **Separation of Concerns**: Tách biệt logic game, rendering và UI
- **Configuration system**: Lưu cài đặt trong file JSON với dot notation
- **State Management**: Quản lý trạng thái game hiệu quả
- **Event-Driven Architecture**: Xử lý sự kiện tập trung
- **Modular Design**: Dễ bảo trì và mở rộng
- **Error handling**: Xử lý lỗi robust
- **Animation system**: Hiệu ứng mượt mà với math-based animations
- **Collision detection**: Phát hiện va chạm chính xác với pygame.Rect

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
