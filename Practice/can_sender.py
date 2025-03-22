import can
import time

def send_periodic_messages_sequentially():
    # Kết nối tới kênh vcan1
    with can.Bus(interface='socketcan', channel='vcan1', bitrate=250000) as bus:
        
        # Danh sách các tin nhắn CAN
        messages = [
            can.Message(arbitration_id=0x123, data=[1, 2, 3, 4, 5, 6, 7, 8], is_extended_id=False),
            can.Message(arbitration_id=0x456, data=[8, 7, 6, 5, 4, 3, 2, 1], is_extended_id=False),
            can.Message(arbitration_id=0x789, data=[0, 0, 0, 0, 1, 2, 3, 4], is_extended_id=False),
            can.Message(arbitration_id=0xABC, data=[9, 8, 7, 6, 5, 4, 3, 2], is_extended_id=False)
        ]

        logger_send = can.Logger('sender_msg.log',append = False)
        
        # Gửi các tin nhắn cách nhau mỗi 1 giây
        try:
            for i in range(1):  # Lặp lại 3 lần cho mỗi tin nhắn
                for msg in messages:
                    bus.send(msg)
                    logger_send.on_message_received(msg)
                    print(f"Gửi tin nhắn với ID {hex(msg.arbitration_id)} trên kênh {bus.channel_info}")
                    time.sleep(0.5)  # Chờ 1 giây trước khi gửi tin nhắn tiếp theo
        except KeyboardInterrupt:
            print("Dừng bởi người dùng.")
        finally:
            bus.shutdown()
            print("Kết thúc gửi tin nhắn.")

if __name__ == "__main__":
    send_periodic_messages_sequentially()
