import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV数据，并将Timestamp列解析为日期时间格式
data = pd.read_csv('Walk_1_Conversion.csv', parse_dates=['Timestamp'])

# 计算合成加速度的模
data['Magnitude'] = np.sqrt(data['X(m/s^2)']**2 + data['Y(m/s^2)']**2 + data['Z(m/s^2)']**2)

# 检查是否成功计算合成加速度
print("Magnitude data:", data['Magnitude'].head())

# 打印数据集的行数
num_rows = data.shape[0]
print(f"{num_rows} lines")

# 绘制合成加速度随时间变化的图
plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp'], data['Magnitude'], label='Magnitude of Acceleration', color='m')
plt.xlabel('Timestamp')
plt.ylabel('Magnitude (m/s^2)')
plt.legend()
plt.title('Magnitude of Acceleration over Time')
plt.tight_layout()
plt.show()
