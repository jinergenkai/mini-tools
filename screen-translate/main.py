"""
Screen Translate Tool
=====================
Hotkey → Screenshot vùng chọn → OCR (GPT-4V) → Dịch (GPT) → Telegram + TTS

Flow:
  1. Bấm ← (mũi tên trái) lần 1 → ghi nhận vị trí cursor = góc TRÊN-TRÁI
  2. Di chuột đến góc dưới-phải
  3. Bấm ← lần 2 → chụp vùng → OCR → LLM → gửi kết quả

Windows only. Chạy: python main.py
"""

import os
import sys
import io
import time
import json
import base64
import threading
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

import yaml
import mss
import mss.tools
from pynput import keyboard, mouse
from PIL import Image
import requests

# ─────────────────────────────────────────────
# Load config
# ─────────────────────────────────────────────
CONFIG_PATH = Path(__file__).parent / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

# ─────────────────────────────────────────────
# State
# ─────────────────────────────────────────────
class State:
    """Track selection state"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.corner1 = None  # (x, y) góc trên-trái
        self.corner2 = None  # (x, y) góc dưới-phải
        self.waiting_for_second = False
        self.processing = False

state = State()
pressed_keys = set()

# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────
def get_cursor_position():
    """Lấy vị trí cursor hiện tại"""
    from ctypes import windll, Structure, c_long, byref
    
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]
    
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return (pt.x, pt.y)


def beep(freq=800, duration=100):
    """Beep nhẹ để xác nhận"""
    try:
        import winsound
        winsound.Beep(freq, duration)
    except:
        pass


def capture_region(x1, y1, x2, y2):
    """Chụp vùng màn hình, trả về PIL Image"""
    # Đảm bảo x1 < x2, y1 < y2
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    # Tối thiểu 10px
    if right - left < 10 or bottom - top < 10:
        print("[!] Vùng chọn quá nhỏ, bỏ qua")
        return None
    
    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top,
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    # Debug save
    if config.get("screenshot", {}).get("save_debug"):
        debug_dir = Path(config["screenshot"].get("debug_path", "./debug_screenshots/"))
        debug_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        img.save(debug_dir / f"capture_{ts}.png")
        print(f"[DEBUG] Saved screenshot to {debug_dir / f'capture_{ts}.png'}")
    
    return img


def image_to_base64(img: Image.Image, format="PNG") -> str:
    """Convert PIL Image → base64 string"""
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ─────────────────────────────────────────────
# OpenAI API
# ─────────────────────────────────────────────
def ocr_with_vision(img: Image.Image) -> str:
    """Dùng GPT-4V để OCR ảnh → text"""
    api_key = config["openai"]["api_key"]
    b64 = image_to_base64(img)
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract ALL text from this image exactly as shown. Preserve formatting, line breaks, and structure. Return ONLY the extracted text, nothing else."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def translate_with_llm(text: str) -> str:
    """Gửi text qua LLM để dịch/xử lý theo prompt"""
    api_key = config["openai"]["api_key"]
    model = config["openai"].get("model", "gpt-4o")
    prompt = config.get("prompt", "Dịch sang tiếng Việt:")
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": config["openai"].get("max_tokens", 2000),
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ]
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def ocr_and_translate(img: Image.Image) -> dict:
    """
    Kết hợp OCR + Translate trong 1 call (tiết kiệm API)
    Gửi ảnh + prompt dịch luôn
    """
    api_key = config["openai"]["api_key"]
    model = config["openai"].get("model", "gpt-4o")
    prompt = config.get("prompt", "Dịch sang tiếng Việt:")
    b64 = image_to_base64(img)
    
    combined_prompt = f"""Thực hiện 2 bước:
1. OCR: Trích xuất toàn bộ text từ ảnh
2. Xử lý: {prompt}

Trả về JSON format (không markdown, không ```) :
{{"original": "text gốc từ ảnh", "result": "kết quả sau khi xử lý"}}"""
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": config["openai"].get("max_tokens", 2000),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": combined_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
        },
        timeout=30,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback nếu không parse được JSON
        return {"original": "", "result": content}


# ─────────────────────────────────────────────
# Telegram
# ─────────────────────────────────────────────
def send_telegram(text: str, image: Image.Image = None):
    """Gửi kết quả qua Telegram"""
    tg = config.get("telegram", {})
    if not tg.get("enabled"):
        return
    
    bot_token = tg["bot_token"]
    chat_id = tg["chat_id"]
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    # Gửi text
    try:
        # Gửi ảnh gốc kèm caption
        if image:
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            buf.seek(0)
            
            # Telegram caption limit = 1024 chars
            caption = text[:1024] if len(text) <= 1024 else text[:1021] + "..."
            
            requests.post(
                f"{base_url}/sendPhoto",
                data={"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"},
                files={"photo": ("screenshot.png", buf, "image/png")},
                timeout=15,
            )
            
            # Nếu text dài hơn caption, gửi thêm message
            if len(text) > 1024:
                requests.post(
                    f"{base_url}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                    timeout=15,
                )
        else:
            requests.post(
                f"{base_url}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=15,
            )
        
        print("[✓] Đã gửi Telegram")
    except Exception as e:
        print(f"[✗] Telegram error: {e}")


# ─────────────────────────────────────────────
# TTS (Text-to-Speech)
# ─────────────────────────────────────────────
def speak_text(text: str):
    """Phát âm thanh bằng edge-tts"""
    tts_cfg = config.get("tts", {})
    if not tts_cfg.get("enabled"):
        return

    voice = tts_cfg.get("voice", "vi-VN-HoaiMyNeural")
    rate = tts_cfg.get("rate", "+0%")

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()

    try:
        # Dùng edge-tts CLI
        cmd = [
            sys.executable, "-m", "edge_tts",
            "--voice", voice,
            "--rate", rate,
            "--text", text,
            "--write-media", tmp.name,
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)

        # Phát bằng Windows MCI (built-in, không cần cài gì, blocking)
        if sys.platform == "win32":
            import ctypes
            mci = ctypes.windll.winmm.mciSendStringW
            path = tmp.name.replace("\\", "/")
            mci(f'open "{path}" type mpegvideo alias tts_media', None, 0, None)
            mci('play tts_media wait', None, 0, None)
            mci('close tts_media', None, 0, None)

        print("[✓] TTS đã phát xong")

    except Exception as e:
        print(f"[✗] TTS error: {e}")
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def process_screenshot(img: Image.Image):
    """Pipeline chính: OCR → Dịch → Output"""
    print("\n" + "="*50)
    print("[→] Đang xử lý...")
    
    try:
        # OCR + Translate combo (1 API call)
        result = ocr_and_translate(img)
        
        original = result.get("original", "")
        translated = result.get("result", "")
        
        print(f"\n[OCR] Gốc:\n{original}")
        print(f"\n[LLM] Kết quả:\n{translated}")
        
        # Format cho Telegram
        tg_text = f"<b>📝 Gốc:</b>\n{original}\n\n<b>🔄 Dịch:</b>\n{translated}"
        
        # Gửi Telegram + TTS chạy nền (daemon) — không block hotkey tiếp theo
        threading.Thread(target=send_telegram, args=(tg_text, img), daemon=True).start()
        threading.Thread(target=speak_text, args=(translated,), daemon=True).start()

        print("\n[✓] OCR+Dịch xong! TTS đang phát nền, có thể chụp tiếp.")
        
    except Exception as e:
        print(f"\n[✗] Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    print("="*50)


# ─────────────────────────────────────────────
# Keyboard Listener
# ─────────────────────────────────────────────
def on_key_press(key):
    """Xử lý hotkey"""
    pressed_keys.add(key)

    # Check hotkey
    hotkey_name = config.get("hotkey", "left")

    target_key = getattr(keyboard.Key, hotkey_name, None)
    if target_key is None:
        return

    if key != target_key:
        return
    
    if state.processing:
        print("[...] Đang xử lý, vui lòng đợi")
        return
    
    cursor_pos = get_cursor_position()
    
    if not state.waiting_for_second:
        # ── Lần bấm 1: Ghi nhận góc trên-trái ──
        state.corner1 = cursor_pos
        state.waiting_for_second = True
        beep(600, 80)
        print(f"\n[1/2] Góc trên-trái: {cursor_pos}")
        print("[...] Di chuột đến góc dưới-phải rồi bấm ← lần nữa")
    
    else:
        # ── Lần bấm 2: Ghi nhận góc dưới-phải → Chụp ──
        state.corner2 = cursor_pos
        state.waiting_for_second = False
        state.processing = True
        beep(1000, 80)
        print(f"[2/2] Góc dưới-phải: {cursor_pos}")
        
        x1, y1 = state.corner1
        x2, y2 = state.corner2
        
        # Chụp trong thread riêng để không block listener
        def do_capture():
            try:
                img = capture_region(x1, y1, x2, y2)
                if img:
                    process_screenshot(img)
            except Exception as e:
                print(f"[✗] Lỗi chụp màn hình: {e}")
                beep(300, 300)
            finally:
                state.processing = False
                state.reset()
        
        threading.Thread(target=do_capture, daemon=True).start()


def on_key_release(key):
    """ESC chỉ hủy chọn vùng, không thoát chương trình"""
    pressed_keys.discard(key)
    if key == keyboard.Key.esc:
        if state.waiting_for_second:
            state.reset()
            beep(300, 150)
            print("\n[✗] Đã hủy chọn vùng")


# ─────────────────────────────────────────────
# Entry
# ─────────────────────────────────────────────
def main():
    print(r"""
    ╔══════════════════════════════════════════╗
    ║       SCREEN TRANSLATE TOOL v1.0         ║
    ║──────────────────────────────────────────║
    ║  ← (lần 1) = Chọn góc trên-trái         ║
    ║  ← (lần 2) = Chọn góc dưới-phải → Dịch  ║
    ║  ESC        = Hủy chọn vùng              ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Validate config
    api_key = config.get("openai", {}).get("api_key", "")
    if not api_key or api_key.startswith("sk-YOUR"):
        print("[!] ⚠️  Chưa cấu hình OpenAI API key trong config.yaml")
        print("[!] Mở config.yaml → thay 'sk-YOUR-API-KEY-HERE' bằng key thật")
        return
    
    tg = config.get("telegram", {})
    if tg.get("enabled") and (not tg.get("bot_token") or "YOUR" in tg.get("bot_token", "")):
        print("[!] ⚠️  Telegram chưa cấu hình. Xem hướng dẫn trong README.md")
        print("[!] Telegram sẽ bị tắt, chỉ dùng TTS")
        config["telegram"]["enabled"] = False
    
    print(f"[✓] Hotkey: ← (mũi tên trái)")
    print(f"[✓] LLM: {config['openai'].get('model', 'gpt-4o')}")
    print(f"[✓] Telegram: {'BẬT' if config.get('telegram', {}).get('enabled') else 'TẮT'}")
    print(f"[✓] TTS: {'BẬT' if config.get('tts', {}).get('enabled') else 'TẮT'}")
    print(f"\n[...] Đang lắng nghe hotkey...\n")
    
    try:
        with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n[EXIT] Ctrl+C - Thoát chương trình.")


if __name__ == "__main__":
    main()
