import can

def send_multiple_can_messages():
    # Kết nối đến kênh `vcan1` với bitrate 250 kbps
    with can.Bus(interface='socketcan', channel='vcan1', bitrate=250000) as bus:
        
        # Danh sách các tin nhắn với các arbitration_id khác nhau
        messages = [
            can.Message(arbitration_id=0x123, data=[1, 2, 3, 4, 5, 6, 7, 8], is_extended_id=False),
            can.Message(arbitration_id=0x456, data=[8, 7, 6, 5, 4, 3, 2, 1], is_extended_id=False),
            can.Message(arbitration_id=0x789, data=[0, 0, 0, 0, 1, 2, 3, 4], is_extended_id=True),
            can.Message(arbitration_id=0xABC, data=[9, 8, 7, 6, 5, 4, 3, 2], is_extended_id=True)
        ]

        for msg in messages:
            try:
                # Gửi từng tin nhắn trong danh sách
                bus.send(msg)
                print(f"Tin nhắn với ID {hex(msg.arbitration_id)} đã được gửi trên kênh {bus.channel_info}")
                
                # Chờ một khoảng thời gian giữa các lần gửi để đảm bảo xử lý
                #time.sleep(0.1)  
            except can.CanError:
                print(f"Không thể gửi tin nhắn với ID {hex(msg.arbitration_id)}")

# Gửi nhiều tin nhắn
send_multiple_can_messages()
