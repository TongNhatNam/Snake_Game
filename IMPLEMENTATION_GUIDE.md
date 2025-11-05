# 🎮 Hướng Dẫn Thực Hiện Audio & Multiplayer

## ✅ Phần 1: Hệ Thống Âm Thanh (HOÀN THÀNH)

### Các File Được Tạo/Cập Nhật:

1. **`components/core/audio_manager.py`** (MỚI)
   - Quản lý nhạc nền và hiệu ứng âm thanh
   - Hỗ trợ bật/tắt và điều chỉnh âm lượng

2. **`config.json`** - Thêm phần `audio` với các cấu hình:
   - `music_enabled`: Bật/tắt nhạc (mặc định: true)
   - `sfx_enabled`: Bật/tắt SFX (mặc định: true)
   - `master_volume`: Âm lượng chính (0.0-1.0)
   - `music_volume`: Âm lượng nhạc (0.0-1.0)
   - `sfx_volume`: Âm lượng SFX (0.0-1.0)

3. **`game.py`** - Cập nhật:
   - Import `audio_manager`
   - Phát nhạc nền khi game khởi động
   - Phát SFX khi ăn, chết, pickup power-up, game over
   - Tạm dừng/tiếp tục nhạc khi pause/resume

4. **`assets/sounds/`** (MỚI)
   - Thư mục cho các file .wav
   - README hướng dẫn tạo âm thanh

### 🎵 Các File Âm Thanh Cần Thêm:

Tạo hoặc tải các file WAV sau vào `assets/sounds/`:
- `background_music.wav` - Nhạc nền chính
- `eat_sound.wav` - Khi ăn thức ăn
- `powerup_sound.wav` - Khi pickup power-up
- `death_sound.wav` - Khi rắn chết
- `level_complete.wav` - Khi game over
- `menu_select.wav` - Chọn trong menu
- `menu_back.wav` - Quay lại menu

### 🧪 Kiểm Tra Audio:

```bash
# Chạy game và kiểm tra:
# 1. Nhạc nền phát khi game khởi động
# 2. Âm thanh phát khi ăn thức ăn
# 3. Âm thanh phát khi pickup power-up
# 4. Âm thanh phát khi chết
python game.py
```

---

## 📋 Phần 2: Chế Độ 2 Người Chơi (CHUẨN BỊ)

### Các Bước Tiếp Theo Cần Làm:

#### **Bước 1: Cập Nhật MainMenu - Chọn Chế Độ Chơi**

File: `components/ui/game_menus.py`

Thêm option vào MainMenu:
```python
# Thêm option "Multiplayer" vào menu
# Khi chọn, set game_state.game_mode = "multiplayer"
```

#### **Bước 2: Sửa Event Handler - Xử Lý 2 Rắn**

File: `components/core/event_handler.py`

Thêm xử lý điều khiển cho Player 2:
```python
# Player 1: WASD hoặc Arrows
# Player 2: IJKL hoặc Numpad
# Ví dụ:
# I = Up, K = Down, J = Left, L = Right
```

#### **Bước 3: Sửa Game.py - Tạo 2 Rắn**

File: `game.py`

```python
def start_new_game(self, level=1):
    # Nếu multiplayer:
    if self.game_state.game_mode == "multiplayer":
        # Tạo snake1 và snake2 ở vị trí khác nhau
        self.game_objects["snake1"] = Snake(...)
        self.game_objects["snake2"] = Snake(...)
    else:
        # Single player như hiện tại
        self.game_objects["snake"] = Snake(...)
```

#### **Bước 4: Sửa Collision Logic**

File: `game.py` - `_check_collisions()`

```python
# Xử lý:
# 1. Va chạm giữa 2 rắn (cả hai mất mạng hoặc 1 người thắng)
# 2. Ăn chia sẻ (ai ăn trước được điểm)
# 3. Cập nhật điểm riêng cho mỗi người
```

#### **Bước 5: Sửa Renderer - Hiển Thị HUD 2 Người**

File: `components/core/game_renderer.py`

```python
# Chia màn hình HUD:
# - Bên trái: Player 1 Score, Lives
# - Bên phải: Player 2 Score, Lives
# - Giữa: Game area
```

---

## 🔧 Hướng Dẫn Chi Tiết Từng Phần

### Part A: Thêm Mode Selection Menu

**File: `components/ui/game_menus.py`**

```python
# Tìm class MainMenu
# Thêm option mới trong __init__:

class MainMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = [
            "Single Player",
            "Multiplayer",  # ← Thêm dòng này
            "Settings",
            "High Scores",
            "Quit"
        ]
```

### Part B: Xử Lý Chế Độ Multiplayer

**File: `components/ui/base_menu.py`**

```python
# Trong handle_event của MainMenu:
def handle_event(self, event):
    result = super().handle_event(event)
    if result == "Single Player":
        return "start_single"  # ← Trả về mode
    elif result == "Multiplayer":
        return "start_multiplayer"  # ← Trả về mode
    # ... rest của code
```

### Part C: Update Event Handler

**File: `components/core/event_handler.py`**

```python
# Thêm xử lý cho Player 2:
def _handle_playing_events(self, event, snake=None, snake2=None):
    if event.type == pygame.KEYDOWN:
        # Player 1 controls (existing)
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            snake.change_direction(-self.block_size, 0)
        # ... more Player 1 controls
        
        # Player 2 controls (new - IJKL)
        if snake2:  # Only if multiplayer
            if event.key == pygame.K_j:  # Left
                snake2.change_direction(-self.block_size, 0)
            elif event.key == pygame.K_l:  # Right
                snake2.change_direction(self.block_size, 0)
            elif event.key == pygame.K_i:  # Up
                snake2.change_direction(0, -self.block_size)
            elif event.key == pygame.K_k:  # Down
                snake2.change_direction(0, self.block_size)
```

---

## 📊 Tóm Tắt Trạng Thái

### ✅ Hoàn Thành:
- [x] Audio Manager System
- [x] Config Audio Settings
- [x] Audio Integration (eat, powerup, death)
- [x] Game State Multiplayer Setup

### ⏳ Cần Làm:
- [ ] Mode Selection Menu
- [ ] Multiplayer Event Handling
- [ ] Multiplayer Game Logic
- [ ] Multiplayer Renderer/HUD
- [ ] Test Multiplayer

---

## 🚀 Bước Tiếp Theo

**Bạn muốn tôi tiếp tục với:**
1. **Mode Selection Menu** - Thêm nút Multiplayer vào menu
2. **Event Handling** - Xử lý điều khiển 2 người
3. **Game Logic** - Logic chơi 2 người (va chạm, chia sẻ ăn)
4. **UI/Rendering** - Hiển thị điểm riêng cho mỗi người

**Hoặc bạn cần:**
- Tạo file âm thanh trước tiên?
- Kiểm tra audio hoạt động?
- Sửa gì đó khác?

Hãy cho tôi biết! 🎮
