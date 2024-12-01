import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 读取CSV数据
data = pd.read_csv('Static4_10s_3_conversion.csv')

# 绘制时间序列图
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(data['Timestamp(ms)'], data['X(m/s^2)'], label='X-axis',marker='^', color='r')
plt.xlabel('Timestamp(ms)')
plt.ylabel('X(m/s^2)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(data['Timestamp(ms)'], data['Y(m/s^2)'], label='Y-axis',marker='^', color='g')
plt.xlabel('Timestamp(ms)')
plt.ylabel('Y(m/s^2)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(data['Timestamp(ms)'], data['Z(m/s^2)'], label='Z-axis',marker='^' ,color='b')
plt.xlabel('Timestamp(ms)')
plt.ylabel('Z(m/s^2)')
plt.legend()

plt.tight_layout()
plt.show()

# 计算并绘制合成加速度
data['Magnitude'] = np.sqrt(data['X(m/s^2)']**2 + data['Y(m/s^2)']**2 + data['Z(m/s^2)']**2)
plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp(ms)'], data['Magnitude'], label='Magnitude of Acceleration', color='m')
plt.xlabel('Timestamp(ms)')
plt.ylabel('Magnitude (m/s^2)')
plt.legend()
plt.show()