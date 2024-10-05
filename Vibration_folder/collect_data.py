import serial
import csv
import time

# 配置串口参数
port = 'COM6'  # 请替换为你的ESP32连接的端口
baud_rate = 115200
timeout = 1  # 1秒超时

# 打开串口
ser = serial.Serial(port, baud_rate, timeout=timeout)

# 创建CSV文件并写入表头
with open('accelerometer_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp (ms)', 'X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)'])

    try:
        while True:
            # 从串口读取数据
            data = ser.readline().decode('utf-8').strip()
            
            # 如果读取到有效数据
            if data:
                # 在屏幕上显示数据
                print(f"Received: {data}")  # 显示接收到的数据
                
                # 将数据分割为列表
                data_list = data.split(', ')
                
                # 保存数据到CSV文件
                writer.writerow(data_list)
                
                # 每条数据写入之后可以添加短暂延迟，避免过快
                time.sleep(0.01)  # 10ms

    except KeyboardInterrupt:
        # 当按下Ctrl+C终止时，关闭串口
        print("Data collection stopped.")
        ser.close()
