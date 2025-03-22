import can
from can import CanInitializationError

def initialize_can_bus():
    try:
        # Thử khởi tạo một CAN Bus với thông số sai hoặc không tồn tại
        bus = can.Bus(interface='socketcan', channel='non_existent_channel', bitrate=500000)
    except CanInitializationError as e:
        # Xử lý ngoại lệ nếu có lỗi khởi tạo CAN Bus
        print(f"CanInitializationError occurred: {e}")
    except ValueError as ve:
        # Xử lý ngoại lệ nếu có giá trị sai trong cấu hình
        print(f"ValueError: {ve}")
    except Exception as ex:
        # Xử lý các lỗi không mong đợi khác
        print(f"Unexpected error: {ex}")
    else:
        print("CAN Bus initialized successfully!")
        # Đừng quên đóng bus sau khi sử dụng
        bus.shutdown()

if __name__ == "__main__":
    initialize_can_bus()
