import can

# Phát hiện tất cả các cấu hình CAN khả dụng
configs = can.detect_available_configs()
print("Available CAN Configurations:")
for config in configs:
    print(config)

# # Phát hiện cấu hình cho giao diện cụ thể (ví dụ: 'socketcan')
# socketcan_configs = can.detect_available_configs()
# print("\nSocketCAN Configurations:")
# for config in socketcan_configs:
#     print(config)
