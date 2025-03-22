import can
import asyncio
import time
 
async def dual_rate_periodic_send(bus, msg, initial_period, subsequent_period, count):
    """Gửi tin nhắn với chu kỳ thay đổi sau một số lần nhất định."""
    # Gửi tin nhắn `count` lần với chu kỳ `initial_period`
    for _ in range(count):
        bus.send(msg)
        print(f"Đã gửi tin nhắn với period {initial_period} giây.")
        await asyncio.sleep(initial_period)
 
    # Sau đó gửi liên tục với `subsequent_period`
    while True:
        bus.send(msg)
        print(f"Đã gửi tin nhắn với period {subsequent_period} giây.")
        await asyncio.sleep(subsequent_period)
 
async def main():
    # Khởi tạo bus CAN ảo
    with can.Bus(interface='socketcan', channel='vcan1', bitrate=250000) as bus:
        # Tạo một tin nhắn CAN
        msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5])
        
        # Tạo tác vụ gửi tin nhắn với chu kỳ thay đổi
        task = asyncio.create_task(dual_rate_periodic_send(bus, msg, initial_period=0.001, subsequent_period=0.5, count=10))
 
        # Đợi 2 giây, sau đó thay đổi dữ liệu
        await asyncio.sleep(2)
        print("Changing data[0] = 0x42")
        msg.data[0] = 0x42
 
        # Đợi thêm 2 giây trước khi dừng tác vụ
        await asyncio.sleep(2)
        task.cancel()  # Hủy tác vụ gửi theo chu kỳ
        print("stopped cyclic send")
 
# Chạy hàm main trong asyncio
asyncio.run(main())