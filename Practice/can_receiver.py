import can
import time

logger = can.SqliteWriter('received_msg.db')

def log_can_messages():
    # Kết nối tới kênh CAN (vcan1)
    with can.Bus(interface='socketcan', channel='vcan1', bitrate=250000) as bus:


        print("Đang nhận dữ liệu CAN... Nhấn Ctrl+C để dừng.")

        try:
            # Liên tục đọc và ghi các thông điệp CAN vào tệp
            msg = bus.recv(timeout=2)  # Nhận tin nhắn CAN (timeout sau 1 giây)
            if msg:
                logger.on_message_received(msg)
                logger.GET_MESSAGE_TIMEOUT()
                print(f"Nhận tin nhắn: {msg}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nNgừng ghi dữ liệu.")
        finally:
            logger.stop()  # Dừng Logger khi kết thúc
            print("Đã lưu tin nhắn vào 'received_msg.log'.")

if __name__ == "__main__":
    log_can_messages()
