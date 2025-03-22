import isotp

# Định nghĩa hàm nhận dữ liệu từ tầng liên kết dữ liệu
def my_rxfn(timeout: float):
    """
    Mô phỏng nhận tin nhắn từ CAN bus.
    """
    print(f"[RXFN] Đang chờ dữ liệu với timeout: {timeout}s...")
    # Mô phỏng một tin nhắn CAN nhận được
    can_message = isotp.CanMessage(arbitration_id=0x123, data=bytearray([0x02, 0x01, 0x02, 0x03, 0x04]), is_extended_id=False)
    return can_message


# Định nghĩa hàm gửi dữ liệu tới tầng liên kết dữ liệu
def my_txfn(msg: isotp.CanMessage):
    """
    Mô phỏng gửi tin nhắn tới CAN bus.
    """
    print(f"[TXFN] Đang gửi tin nhắn: Arbitration ID: {msg.arbitration_id}, Data: {list(msg.data)}, Extended: {msg.is_extended_id}")


# Cấu hình địa chỉ ISO-TP (giả sử ID truyền và nhận là 0x123 và 0x456)
address = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x123, rxid=0x456)

# Tạo đối tượng TransportLayer
transport_layer = isotp.TransportLayer(rxfn=my_rxfn, txfn=my_txfn, address=address)

# Bắt đầu tầng giao vận
transport_layer.start()

try:
    # Gửi một thông điệp lớn hơn 8 byte
    print("[INFO] Bắt đầu gửi dữ liệu...")
    data_to_send = bytearray([0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0])
    transport_layer.send(data_to_send)
    print("[INFO] Dữ liệu đã được gửi thành công!")

    # Mô phỏng nhận dữ liệu từ phía nhận
    print("[INFO] Đang chờ nhận dữ liệu...")
    received_message = transport_layer.recv()
    if received_message:
        print(f"[INFO] Đã nhận tin nhắn: {list(received_message)}")
    else:
        print("[INFO] Không nhận được tin nhắn nào.")
except Exception as e:
    print(f"[ERROR] Xảy ra lỗi: {e}")
finally:
    # Dừng tầng giao vận
    transport_layer.stop()
    print("[INFO] Đã dừng Transport Layer.")
