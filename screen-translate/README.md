# Screen Translate Tool 🖥️→📱

Chụp vùng màn hình ẩn → OCR → LLM dịch thuật → Gửi Telegram + Phát loa

## Flow hoạt động

```
Bấm ← (lần 1)     →  Ghi vị trí cursor = góc trên-trái
Di chuột            →  Đến vùng text cần dịch
Bấm ← (lần 2)     →  Ghi vị trí cursor = góc dưới-phải
                    →  Chụp ẩn → GPT-4V OCR+Dịch
                    →  Gửi Telegram + Phát loa
ESC                 →  Hủy chọn / Thoát
```

## Cài đặt (Windows)

### 1. Cài Python dependencies

```bash
python -m venv venv ; venv/scripts/activate
pip install -r requirements.txt
```

### 2. Cấu hình OpenAI API Key

Mở `config.yaml`, thay:

```yaml
openai:
  api_key: "sk-YOUR-REAL-API-KEY"
```

### 3. Setup Telegram Bot (nhận kết quả trên mobile)

**Bước 1: Tạo Bot**

1. Mở Telegram, tìm `@BotFather`
2. Gửi `/newbot`
3. Đặt tên bot (ví dụ: "My Translate Bot")
4. Copy **Bot Token** (dạng `7123456789:AAH...`)

**Bước 2: Lấy Chat ID**

1. Gửi tin nhắn bất kỳ cho bot vừa tạo
2. Mở trình duyệt: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Tìm `"chat":{"id": 123456789}` → đó là Chat ID

**Bước 3: Điền vào config.yaml**

```yaml
telegram:
  enabled: true
  bot_token: "7123456789:AAHxxx..."
  chat_id: "123456789"
```

### 4. Chạy

```bash
python main.py
```

## Tùy chỉnh

### Đổi prompt (config.yaml)

```yaml
# Dịch thuật
prompt: |
  Dịch đoạn text sau sang tiếng Việt. Giữ thuật ngữ kỹ thuật.

# Hoặc: Trả lời câu hỏi
prompt: |
  Đọc text từ ảnh và trả lời câu hỏi bằng tiếng Việt.
  Giải thích chi tiết, dễ hiểu.

# Hoặc: Tóm tắt
prompt: |
  Tóm tắt nội dung trong ảnh bằng tiếng Việt, ngắn gọn.
```

### Đổi hotkey

```yaml
hotkey: "left" # Mũi tên trái (mặc định)
# hotkey: "right"   # Mũi tên phải
# hotkey: "f2"      # Phím F2
# hotkey: "scroll_lock"  # Scroll Lock
```

### Đổi giọng TTS

```yaml
tts:
  voice: "vi-VN-HoaiMyNeural" # Nữ Việt Nam
  # voice: "vi-VN-NamMinhNeural" # Nam Việt Nam
  # voice: "en-US-JennyNeural"   # Nữ Mỹ
  rate: "+0%" # Bình thường
  # rate: "+20%"                  # Nhanh hơn
  # rate: "-20%"                  # Chậm hơn
```

### Tắt/Bật tính năng

```yaml
telegram:
  enabled: false # Tắt Telegram

tts:
  enabled: false # Tắt phát loa
```

## Cấu trúc project

```
screen-translate/
├── main.py           # Code chính
├── config.yaml       # Cấu hình (API keys, prompt, hotkey...)
├── requirements.txt  # Dependencies
└── README.md         # Hướng dẫn này
```

## Tính ẩn (Stealth)

- Dùng OS-level screenshot API (`mss`) → web/app KHÔNG detect được
- Không hiện overlay, không hiện popup capture
- Không dùng `getDisplayMedia` → không trigger browser recording indicator
- Tương đương bấm Print Screen - hoàn toàn invisible

## Troubleshoot

**"Vùng chọn quá nhỏ"**
→ 2 lần bấm ← phải cách nhau ít nhất 10px

**Telegram không nhận**
→ Kiểm tra bot_token và chat_id
→ Phải gửi tin nhắn cho bot trước (để bot có quyền gửi lại)

**TTS không phát**
→ Cần có speaker/headphone kết nối
→ Thử chạy: `python -m edge_tts --voice "vi-VN-HoaiMyNeural" --text "Xin chào" --write-media test.mp3`

**OCR sai nhiều**
→ Chụp vùng rộng hơn, text rõ hơn
→ GPT-4V hoạt động tốt nhất với text sáng trên nền tối hoặc ngược lại
