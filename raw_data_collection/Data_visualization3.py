import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV数据，并将Timestamp列解析为日期时间格式
data = pd.read_csv('Static1.csv', parse_dates=['Timestamp(ms)'])

# 检查是否成功读取Z轴数据
print("Z-axis data:", data['Z(m/s^2)'].head())

# 打印数据集的行数
num_rows = data.shape[0]
print(f"{num_rows} lines")

# 绘制时间序列图
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(data['Timestamp(ms)'], data['X(m/s^2)'], label='X-axis', marker='^', color='r')
plt.xlabel('Timestamp(ms)')
plt.ylabel('X(m/s^2)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(data['Timestamp(ms)'], data['Y(m/s^2)'], label='Y-axis', marker='^', color='g')
plt.xlabel('Timestamp(ms)')
plt.ylabel('Y(m/s^2)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(data['Timestamp(ms)'], data['Z(m/s^2)'], label='Z-axis', marker='^', color='b')
plt.xlabel('Timestamp(ms)')
plt.ylabel('Z(m/s^2)')
plt.legend()

plt.tight_layout()
plt.show()
