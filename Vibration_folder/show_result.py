import csv
import matplotlib.pyplot as plt

# 定义要读取的CSV文件路径
csv_file = 'reordered_combined_accelerometer_data.csv'

# 初始化时间和Z轴数据列表
timestamps = []
z_values = []

# 读取CSV文件
with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        try:
            # 尝试将时间戳和Z轴数据转换为浮点数
            timestamps.append(float(row[0]))  # 时间戳 (ms)
            z_values.append(float(row[3]))    # Z轴加速度 (m/s^2)
        except ValueError:
            # 忽略无法转换的行
            print(f"Skipping invalid row: {row}")

# 绘制Z轴数据随时间的变化
plt.figure(figsize=(10, 6))
plt.plot(timestamps, z_values, label='Z-axis (m/s^2)', color='b')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Z-axis Acceleration (m/s^2)')
plt.title('Z-axis Acceleration Over Time')
plt.legend()
plt.grid(True)

# 显示图像
plt.show()
