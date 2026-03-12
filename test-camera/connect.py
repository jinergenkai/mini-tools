import cv2

# Thông tin kết nối RTSP (thay đổi cho phù hợp với cấu hình camera của bạn)
username = "admin"  # hoặc tài khoản bạn đã đặt
password = "QWErty789)"
ip_address = "hh.smartddns.tv"  # địa chỉ IP camera (kiểm tra trên router hoặc dùng ConfigTool)
port = 554  # mặc định RTSP
channel = 1
subtype = 0  # 0: main stream, 1: sub stream

# Tạo URL RTSP
rtsp_url = f"rtsp://{username}:{password}@{ip_address}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"

# Mở video stream từ camera
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Không kết nối được camera.")
else:
    print("Đã kết nối camera. Nhấn 'q' để thoát.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không lấy được frame.")
            break
        cv2.imshow("Camera Dahua", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
