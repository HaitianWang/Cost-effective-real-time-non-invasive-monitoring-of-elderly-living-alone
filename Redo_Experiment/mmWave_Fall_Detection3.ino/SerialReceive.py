import serial
import csv
import time
import os

# 配置串口参数
serial_port = 'COM6'  # 替换为您的串口号，如 /dev/ttyUSB0 或者 COM6
baud_rate = 115200
timeout = 1

# 配置CSV文件名
csv_filename = "radar_data.csv"

# 检查文件是否存在
file_exists = os.path.isfile(csv_filename)

ser = None  # 初始化 ser 变量

try:
    # 打开串口
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    print(f"Connected to {serial_port} at baud rate {baud_rate}")
    
    # 打开 CSV 文件以追加模式
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # 如果文件不存在，写入表头
        if not file_exists:
            csv_writer.writerow(["Timestamp(ms)", "Target Number", "Distance(m)", "Speed(m/s)", "Energy"])
        
        # 进入无限循环读取串口数据
        while True:
            # 从串口读取一行数据
            line = ser.readline().decode('utf-8').strip()
            if line:
                # 将串口数据输出到控制台
                print(line)
                
                # 解析有效的 CSV 格式数据并写入CSV文件
                try:
                    data_parts = line.split(', ')
                    if len(data_parts) == 5:
                        timestamp = data_parts[0]
                        target_number = data_parts[1]
                        distance = data_parts[2]
                        speed = data_parts[3]
                        energy = data_parts[4]
                        
                        # 将数据写入CSV文件
                        csv_writer.writerow([timestamp, target_number, distance, speed, energy])
                        csv_file.flush()  # 每次写入后刷新到文件，确保内容被保存
                except Exception as e:
                    print(f"Error parsing line: {line}. Error: {e}")

except serial.SerialException as e:
    print(f"Could not open serial port {serial_port}: {e}")
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")
finally:
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed.")
