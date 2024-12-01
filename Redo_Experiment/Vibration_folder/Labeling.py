import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# 读取标注后的数据集
df = pd.read_csv('labeled_accelerometer_data_with_priority.csv')

# 显示数据的基本信息
print(df.info())

# Step 1: 数据清洗
# 去除包含缺失值的行
df.dropna(inplace=True)

# 去除明显异常的加速度值（X, Y, Z 通常加速度应该在 -20 到 20 m/s^2 之间）
df = df[(df['X (m/s^2)'].between(-40, 40)) & 
        (df['Y (m/s^2)'].between(-40, 40)) & 
        (df['Z (m/s^2)'].between(-40, 40))]

# Step 2: 滤波处理
# 定义巴特沃斯低通滤波器
def butter_lowpass(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_lowpass_filter(data, cutoff=0.3, fs=50, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data)
    return y

# 采样频率（假设为50Hz）
fs = 100

# 对X, Y, Z轴分别进行滤波
df['X_filtered'] = apply_lowpass_filter(df['X (m/s^2)'], cutoff=0.3, fs=fs)
df['Y_filtered'] = apply_lowpass_filter(df['Y (m/s^2)'], cutoff=0.3, fs=fs)
df['Z_filtered'] = apply_lowpass_filter(df['Z (m/s^2)'], cutoff=0.3, fs=fs)

# Step 3: 可视化滤波前后的数据对比，带有标签
plt.figure(figsize=(12, 8))

# 绘制 Z 轴原始数据和滤波后数据
plt.subplot(2, 1, 1)
plt.plot(df['Timestamp (ms)'], df['Z (m/s^2)'], label='Original Z Data', color='r')

# 使用不同颜色绘制不同的标签区域
for label, color in zip(['Static', 'Walking', 'Fall_Down'], ['green', 'blue', 'red']):
    indices = df[df['Label'] == label].index
    plt.scatter(df.loc[indices, 'Timestamp (ms)'], df.loc[indices, 'Z (m/s^2)'], label=label, color=color, alpha=0.5)

plt.title('Original Z Data with Labels')
plt.ylabel('Z (m/s^2)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df['Timestamp (ms)'], df['Z_filtered'], label='Filtered Z Data', color='b')

# 对滤波后的数据同样使用不同颜色绘制不同的标签区域
for label, color in zip(['Static', 'Walking', 'Fall_Down'], ['green', 'blue', 'red']):
    indices = df[df['Label'] == label].index
    plt.scatter(df.loc[indices, 'Timestamp (ms)'], df.loc[indices, 'Z_filtered'], label=label, color=color, alpha=0.5)

plt.title('Filtered Z Data with Labels')
plt.ylabel('Z (m/s^2)')
plt.xlabel('Timestamp (ms)')
plt.legend()

plt.tight_layout()
plt.show()

# 保存清洗和滤波后的数据集
df.to_csv('cleaned_filtered_labeled_accelerometer_data.csv', index=False)
print("Done, saved as cleaned_filtered_labeled_accelerometer_data.csv")
