import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 读取CSV数据
data = pd.read_csv('teraterm1.csv')

# 去除列名中的前后空格
data.columns = data.columns.str.strip()

# 绘制时间序列图
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(data['Timestamp (ms)'], data['X (m/s^2)'], label='X-axis',marker='^', color='r')
plt.xlabel('Timestamp (ms)')
plt.ylabel('X (m/s^2)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(data['Timestamp (ms)'], data['Y (m/s^2)'], label='Y-axis',marker='^', color='g')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Y (m/s^2)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(data['Timestamp (ms)'], data['Z (m/s^2)'], label='Z-axis',marker='^' ,color='b')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Z (m/s^2)')
plt.legend()

plt.tight_layout()
plt.show()

# # 绘制三维加速度轨迹图
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(data['X (m/s^2)'], data['Y (m/s^2)'], data['Z (m/s^2)'], label='Acceleration 3D Trajectory')
# ax.set_xlabel('X (m/s^2)')
# ax.set_ylabel('Y (m/s^2)')
# ax.set_zlabel('Z (m/s^2)')
# plt.legend()
# plt.show()

# 计算并绘制合成加速度
data['Magnitude'] = np.sqrt(data['X (m/s^2)']**2 + data['Y (m/s^2)']**2 + data['Z (m/s^2)']**2)
plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp (ms)'], data['Magnitude'], label='Magnitude of Acceleration', color='m')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Magnitude (m/s^2)')
plt.legend()
plt.show()

# # 绘制加速度值的直方图
# plt.figure(figsize=(10, 6))
# plt.hist(data['X (m/s^2)'], bins=30, alpha=0.5, label='X-axis', color='r')
# plt.hist(data['Y (m/s^2)'], bins=30, alpha=0.5, label='Y-axis', color='g')
# plt.hist(data['Z (m/s^2)'], bins=30, alpha=0.5, label='Z-axis', color='b')
# plt.xlabel('Acceleration (m/s^2)')
# plt.ylabel('Frequency')
# plt.legend()
# plt.show()









