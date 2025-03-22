import isotp
import logging
from can.interfaces.socketcan import SocketcanBus
from can import Notifier, Listener

def my_error_handler(error):
    # Called from a different thread, needs to be thread-safe
    logging.warning('IsoTp error happened: %s - %s' % (error.__class__.__name__, str(error)))

# Custom listener để xử lý tin nhắn CAN
class CustomCanListener(Listener):
    def on_message_received(self, msg):
        print(f"[CUSTOM LISTENER] Đã nhận tin nhắn CAN: {msg}")

# 1. Cấu hình CAN bus
bus = SocketcanBus(channel='vcan0')

# 2. Cấu hình địa chỉ ISO-TP
addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x123, rxid=0x456)

# 3. Tạo Custom Listener
custom_listener = CustomCanListener()

# 4. Tạo Notifier và truyền vào lớp NotifierBasedCanStack
notifier = Notifier(bus, [custom_listener])  # Thêm custom listener để xử lý tin nhắn CAN
stack = isotp.NotifierBasedCanStack(bus=bus, notifier=notifier, address=addr, error_handler=my_error_handler)

try:
    # 5. Bắt đầu giao tiếp ISO-TP
    stack.start()
    print("[RECEIVER] Chờ nhận dữ liệu từ Sender...")

    while True:
        # 6. Nhận dữ liệu (blocking)
        payload = stack.recv(timeout=5)  # Đợi tối đa 5 giây để nhận dữ liệu
        if payload:
            print(f"[RECEIVER] Đã nhận payload: {payload.decode('utf-8')}")
            break
        else:
            print("[RECEIVER] Không nhận được dữ liệu, đang chờ...")
except isotp.ReceiveTimeoutError:
    print("[RECEIVER] Quá thời gian chờ nhận dữ liệu.")
except Exception as e:
    print(f"[RECEIVER] Xảy ra lỗi: {e}")
finally:
    # 7. Dừng giao tiếp và giải phóng tài nguyên
    stack.stop()
    notifier.stop()  # Dừng Notifier
    bus.shutdown()
    print("[RECEIVER] Giao tiếp đã dừng.")
