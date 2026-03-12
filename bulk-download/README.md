# EnglishPod MP3 Bulk Downloader

Script Python để tải hàng loạt 365 file MP3 từ EnglishPod với tốc độ 10 file song song.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

```bash
python download_englishpod.py
```

## Tính năng

- Tải 10 file cùng lúc (có thể thay đổi biến `MAX_WORKERS`)
- Hiển thị tiến độ real-time
- Tự động bỏ qua file đã tải
- Xử lý lỗi và retry tự động
- File được lưu vào thư mục `downloads/`

## Tùy chỉnh

Mở file `download_englishpod.py` và thay đổi các biến:

- `START_NUM`: Số file bắt đầu (mặc định: 1)
- `END_NUM`: Số file kết thúc (mặc định: 365)
- `MAX_WORKERS`: Số file tải cùng lúc (mặc định: 10)
- `DOWNLOAD_DIR`: Thư mục lưu file (mặc định: "downloads")
