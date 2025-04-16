import threading
import time

move = None
cal_thread = None  # Biến để theo dõi luồng tính toán

def cal():
    global move
    time.sleep(2)  # Mô phỏng thời gian tính toán
    move = "aaa"
    print("✅ cal() đã hoàn thành!")

def do():
    global move
    print("➡️ move:", move)
    move = None  # Đặt lại move để kiểm tra lần sau

while True:
    time.sleep(1)  # Để tránh CPU chạy quá tải

    if move:
        do()
    elif not cal_thread or not cal_thread.is_alive():  # Nếu chưa có luồng hoặc luồng trước đã kết thúc
        print("🚀 Bắt đầu cal() trong luồng riêng...")
        cal_thread = threading.Thread(target=cal)
        cal_thread.start()
