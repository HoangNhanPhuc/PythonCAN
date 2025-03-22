import isotp
from typing import Optional

# Giả định các hàm phần cứng (Bạn cần thay thế chúng bằng API cụ thể của phần cứng bạn sử dụng)
def my_hardware_api_recv(timeout: float):
    """
    Hàm nhận dữ liệu từ phần cứng. Blocking read trong thời gian `timeout`.
    Trả về một đối tượng mô phỏng tin nhắn hoặc `None` nếu không có dữ liệu.
    """
    # Giả lập nhận tin nhắn từ phần cứng
    return None  # Trả về None nếu không có tin nhắn

def my_hardware_api_make_msg():
    """
    Hàm tạo một đối tượng tin nhắn. Trả về đối tượng tin nhắn có thể sửa đổi.
    """
    class MockMessage:
        def __init__(self):
            self.arbitration_id = None
            self.data = None
            self.dlc = None
            self.extended_id = None

        def set_id(self, arbitration_id):
            self.arbitration_id = arbitration_id

        def set_data(self, data):
            self.data = data

        def set_dlc(self, dlc):
            self.dlc = dlc

        def set_extended_id(self, extended_id):
            self.extended_id = extended_id

    return MockMessage()

def my_hardware_api_send(msg):
    """
    Hàm gửi tin nhắn qua phần cứng. In ra dữ liệu để kiểm tra.
    """
    print(f"[HARDWARE SEND] ID: {hex(msg.arbitration_id)}, Data: {msg.data}, DLC: {msg.dlc}, Extended: {msg.extended_id}")

def my_hardware_close():
    """
    Đóng kết nối phần cứng. Giải phóng tài nguyên.
    """
    print("[HARDWARE] Đóng kết nối phần cứng.")

# Hàm nhận tin nhắn (rxfn) cho TransportLayer
def my_rxfn(timeout: float) -> Optional[isotp.CanMessage]:
    msg = my_hardware_api_recv(timeout)  # Blocking read
    if msg is None:
        return None  # Không có tin nhắn
    return isotp.CanMessage(arbitration_id=msg.arbitration_id, data=msg.data, dlc=msg.dlc, extended_id=msg.extended_id)

# Hàm gửi tin nhắn (txfn) cho TransportLayer
def my_txfn(isotp_msg: isotp.CanMessage):
    msg = my_hardware_api_make_msg()  # Tạo tin nhắn
    msg.set_id(isotp_msg.arbitration_id)
    msg.set_data(isotp_msg.data)
    msg.set_dlc(isotp_msg.dlc)
    msg.set_extended_id(isotp_msg.is_extended_id)
    my_hardware_api_send(msg)  # Gửi tin nhắn qua phần cứng

# Cấu hình địa chỉ ISO-TP
addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x123456, rxid=0x123457)

# Tạo Transport Layer
layer = isotp.TransportLayer(rxfn=my_rxfn, txfn=my_txfn, address=addr)
layer.start()

try:
    # Gửi payload (dữ liệu cần truyền)
    payload = b'Hello, this is a long ISO-TP message!'
    print("[SENDER] Đang gửi payload...")
    layer.send(payload, send_timeout=2)  # Gửi payload với thời gian chờ tối đa là 2 giây
    print("[SENDER] Payload đã được gửi thành công!")
except isotp.BlockingSendFailure:
    print("[SENDER] Lỗi: Không thể gửi payload (timeout hoặc lỗi phần cứng).")
finally:
    # Dừng Transport Layer và giải phóng tài nguyên phần cứng
    layer.stop()
    my_hardware_close()
    print("[SENDER] Kết thúc chương trình.")
