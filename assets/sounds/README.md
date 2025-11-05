# Sound Assets

Đặt các file âm thanh *.wav trong thư mục này.

## Danh sách File Âm Thanh Cần Thiết

| Tên File | Mô Tả | Gợi Ý |
|----------|-------|-------|
| `background_music.wav` | Nhạc nền chính cho game | Âm nhạc loop, thoải mái, ~1-2 phút |
| `eat_sound.wav` | Âm thanh khi rắn ăn thức ăn | Âm thanh ngắn, vui vẻ, ~0.2-0.5s |
| `powerup_sound.wav` | Âm thanh khi pickup power-up | Âm thanh tươi sáng, ~0.3-0.5s |
| `death_sound.wav` | Âm thanh khi rắn chết | Âm thanh buồn, ~0.5-1s |
| `level_complete.wav` | Âm thanh khi hoàn thành level | Âm thanh chiến thắng, ~1-2s |
| `menu_select.wav` | Âm thanh khi chọn trong menu | Âm thanh ngắn, ~0.1-0.2s |
| `menu_back.wav` | Âm thanh khi quay lại menu | Âm thanh ngắn, ~0.1-0.2s |

## Hướng Dẫn Tạo Âm Thanh

### Cách 1: Sử dụng Audacity (Miễn phí)
1. Tải Audacity: https://www.audacityteam.org/
2. Tạo/chỉnh sửa âm thanh
3. Export as WAV (16-bit PCM)

### Cách 2: Sử dụng Website Miễn Phí
- https://pixabay.com/sound-effects/ (Pixabay Sound Effects)
- https://freesound.org/ (Freesound)
- https://zapsplat.com/ (Zapsplat)

### Cách 3: Sử dụng Text-to-Speech + Audacity
1. Tạo âm thanh bằng text-to-speech
2. Chỉnh sửa trong Audacity
3. Export as WAV

## Lưu Ý Kỹ Thuật

- **Định dạng**: WAV (16-bit, 44.1kHz hoặc 48kHz)
- **Codec**: PCM (uncompressed)
- **Kích thước**: Giữ file nhỏ để tránh làm chậm game
- **Looping**: Background music nên có extension .wav để hỗ trợ looping

## Kiểm Tra Âm Thanh

Âm thanh sẽ được tự động load khi game khởi động nếu file tồn tại. Nếu file không có, game sẽ chạy bình thường nhưng không có âm thanh.

Kiểm tra Console/Log để xem lỗi loading.
