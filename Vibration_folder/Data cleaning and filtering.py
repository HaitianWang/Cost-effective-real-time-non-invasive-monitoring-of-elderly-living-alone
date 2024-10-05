import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取标注后的数据集
df = pd.read_csv('labeled_accelerometer_data_with_priority.csv')

# 显示数据的基本信息
print(df.info())

# Step 1: 数据清洗
# 去除包含缺失值的行
df.dropna(inplace=True)

# 去除明显异常的加速度值（X, Y, Z 通常加速度应该在 -40 到 40 m/s^2 之间）
df = df[(df['X (m/s^2)'].between(-40, 40)) & 
        (df['Y (m/s^2)'].between(-40, 40)) & 
        (df['Z (m/s^2)'].between(-40, 40))]

# Step 2: 平滑处理
# 使用滑动平均法对数据进行平滑
window_size = 2  # 定义滑动窗口大小，适当选择窗口大小来平滑数据

df['X_smoothed'] = df['X (m/s^2)'].rolling(window=window_size, center=True).mean()
df['Y_smoothed'] = df['Y (m/s^2)'].rolling(window=window_size, center=True).mean()
df['Z_smoothed'] = df['Z (m/s^2)'].rolling(window=window_size, center=True).mean()

# Step 3: 可视化平滑前后的数据对比，带有标签
plt.figure(figsize=(12, 8))

# 绘制 Z 轴原始数据和平滑后数据
plt.subplot(2, 1, 1)
plt.plot(df['Timestamp (ms)'], df['Z (m/s^2)'], label='Original Z Data', color='r')

# 使用不同颜色绘制不同的标签区域
for label, color in zip(['Static', 'Walking', 'Fall_Down'], ['blue', 'yellow', 'green']):
    indices = df[df['Label'] == label].index
    plt.scatter(df.loc[indices, 'Timestamp (ms)'], df.loc[indices, 'Z (m/s^2)'], label=label, color=color, alpha=0.5)

plt.title('Original Z Data with Labels')
plt.ylabel('Z (m/s^2)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df['Timestamp (ms)'], df['Z_smoothed'], label='Smoothed Z Data', color='r')

# 对平滑后的数据同样使用不同颜色绘制不同的标签区域
for label, color in zip(['Static', 'Walking', 'Fall_Down'], ['blue', 'yellow', 'green']):
    indices = df[df['Label'] == label].index
    plt.scatter(df.loc[indices, 'Timestamp (ms)'], df.loc[indices, 'Z_smoothed'], label=label, color=color, alpha=0.5)

plt.title('Smoothed Z Data with Labels')
plt.ylabel('Z (m/s^2)')
plt.xlabel('Timestamp (ms)')
plt.legend()

plt.tight_layout()
plt.show()

# 保存清洗和平滑后的数据集
df.to_csv('cleaned_smoothed_labeled_accelerometer_data.csv', index=False)
print("Done, saved as cleaned_smoothed_labeled_accelerometer_data.csv")
