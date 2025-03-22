import can

def redirect_messages():
    # Kết nối tới bus nguồn và bus đích
    with can.Bus(interface='socketcan', channel='vcan1', bitrate=250000) as source_bus, \
         can.Bus(interface='socketcan', channel='vcan2', bitrate=250000) as target_bus:

        # Tạo RedirectReader để chuyển tiếp tin nhắn từ source_bus sang target_bus
        redirect_reader = can.RedirectReader(target_bus)

        # Tạo Printer để in thông tin từ target_bus (vcan2)
        print_listener = can.Printer()

        # Gắn RedirectReader vào source_bus và Printer vào target_bus
        notifier_source = can.Notifier(source_bus, [redirect_reader])
        notifier_target = can.Notifier(target_bus, [print_listener])

        print("RedirectReader: Đang chuyển tiếp tin nhắn từ vcan1 sang vcan2...")

        try:
            while True:
                pass  # Chờ lắng nghe và chuyển tiếp liên tục
        except KeyboardInterrupt:
            print("RedirectReader: Dừng chuyển tiếp.")
        finally:
            notifier_source.stop()
            notifier_target.stop()

if __name__ == "__main__":
    redirect_messages()
