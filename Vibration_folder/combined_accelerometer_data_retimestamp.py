import csv

# 定义文件路径
input_file = 'combined_accelerometer_data.csv'
output_file = 'reordered_combined_accelerometer_data.csv'

# 读取原始数据并重新排序时间戳
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    header = next(reader)  # 跳过表头

    # 初始化时间戳起始点和间隔
    start_timestamp = 3046082
    time_interval = 12  # 每条记录的时间间隔为12ms
    current_timestamp = start_timestamp

    # 读取所有行数据并修改时间戳
    data = []
    for row in reader:
        row[0] = str(current_timestamp)  # 修改时间戳列
        data.append(row)
        current_timestamp += time_interval  # 每次递增12ms

# 写入新的CSV文件
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp (ms)', 'X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)', 'Person_ID'])  # 写入表头
    writer.writerows(data)  # 写入修改后的数据

print("Time reordering complete. The new file is saved as:", output_file)
