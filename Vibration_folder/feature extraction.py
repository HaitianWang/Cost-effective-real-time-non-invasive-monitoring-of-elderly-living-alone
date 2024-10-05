import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from scipy.fftpack import fft
from scipy.signal import welch

# 读取标注后的数据集
df = pd.read_csv('cleaned_smoothed_labeled_accelerometer_data.csv')

# Step 1: 数据清洗
# 去除包含缺失值的行
df.dropna(inplace=True)

# Step 2: 平滑处理
window_size = 10  # 定义滑动窗口大小
df['X_smoothed'] = df['X (m/s^2)'].rolling(window=window_size, center=True).mean()
df['Y_smoothed'] = df['Y (m/s^2)'].rolling(window=window_size, center=True).mean()
df['Z_smoothed'] = df['Z (m/s^2)'].rolling(window=window_size, center=True).mean()

# 确保没有NaN值，去掉空值的行
df.dropna(inplace=True)

# Step 3: 特征提取函数
def extract_features(window):
    features = {}
    
    # 时域特征
    features['mean_x'] = window['X_smoothed'].mean()  # X轴的均值
    features['mean_y'] = window['Y_smoothed'].mean()  # Y轴的均值
    features['mean_z'] = window['Z_smoothed'].mean()  # Z轴的均值

    features['std_x'] = window['X_smoothed'].std()  # X轴的标准差
    features['std_y'] = window['Y_smoothed'].std()  # Y轴的标准差
    features['std_z'] = window['Z_smoothed'].std()  # Z轴的标准差

    features['min_x'] = window['X_smoothed'].min()  # X轴的最小值
    features['min_y'] = window['Y_smoothed'].min()  # Y轴的最小值
    features['min_z'] = window['Z_smoothed'].min()  # Z轴的最小值

    features['max_x'] = window['X_smoothed'].max()  # X轴的最大值
    features['max_y'] = window['Y_smoothed'].max()  # Y轴的最大值
    features['max_z'] = window['Z_smoothed'].max()  # Z轴的最大值

    features['rms_x'] = np.sqrt(np.mean(window['X_smoothed'] ** 2))  # X轴的均方根值
    features['rms_y'] = np.sqrt(np.mean(window['Y_smoothed'] ** 2))  # Y轴的均方根值
    features['rms_z'] = np.sqrt(np.mean(window['Z_smoothed'] ** 2))  # Z轴的均方根值

    features['skew_x'] = skew(window['X_smoothed'])  # X轴的偏度
    features['skew_y'] = skew(window['Y_smoothed'])  # Y轴的偏度
    features['skew_z'] = skew(window['Z_smoothed'])  # Z轴的偏度

    features['kurtosis_x'] = kurtosis(window['X_smoothed'])  # X轴的峰度
    features['kurtosis_y'] = kurtosis(window['Y_smoothed'])  # Y轴的峰度
    features['kurtosis_z'] = kurtosis(window['Z_smoothed'])  # Z轴的峰度

    # 频域特征
    X_array = window['X_smoothed'].values  # 转换为NumPy数组
    Y_array = window['Y_smoothed'].values
    Z_array = window['Z_smoothed'].values

    X_fft = fft(X_array)  # X轴的FFT
    Y_fft = fft(Y_array)  # Y轴的FFT
    Z_fft = fft(Z_array)  # Z轴的FFT

    features['fft_max_x'] = np.abs(X_fft).max()  # X轴的FFT最大值
    features['fft_max_y'] = np.abs(Y_fft).max()  # Y轴的FFT最大值
    features['fft_max_z'] = np.abs(Z_fft).max()  # Z轴的FFT最大值

    freqs, psd_x = welch(X_array, fs=50)  # X轴的功率谱密度
    freqs, psd_y = welch(Y_array, fs=50)  # Y轴的功率谱密度
    freqs, psd_z = welch(Z_array, fs=50)  # Z轴的功率谱密度

    features['psd_x'] = np.mean(psd_x)  # X轴的平均功率谱密度
    features['psd_y'] = np.mean(psd_y)  # Y轴的平均功率谱密度
    features['psd_z'] = np.mean(psd_z)  # Z轴的平均功率谱密度

    features['dominant_freq_x'] = freqs[np.argmax(psd_x)]  # X轴的主频率
    features['dominant_freq_y'] = freqs[np.argmax(psd_y)]  # Y轴的主频率
    features['dominant_freq_z'] = freqs[np.argmax(psd_z)]  # Z轴的主频率

    return features

# Step 4: 滑动窗口特征提取
window_size = 4  
step_size = 2  

features_list = []
labels = []

for i in range(0, len(df) - window_size, step_size):
    window = df.iloc[i:i + window_size]
    features = extract_features(window)
    features['label'] = window['Label'].mode()[0]  # 获取窗口内出现最多的标签
    features_list.append(features)

# 将提取的特征转换为DataFrame
features_df = pd.DataFrame(features_list)

# Step 5: 保存特征数据
features_df.to_csv('extracted_features.csv', index=False)

# Step 6: 可视化
plt.figure(figsize=(12, 8))

# 可视化特征：Z轴的均值
plt.plot(features_df.index, features_df['mean_z'], label='Mean Z', color='blue')
plt.scatter(features_df.index, features_df['mean_z'], c=features_df['label'].map({'Static': 'green', 'Walking': 'yellow', 'Fall_Down': 'red'}), label='Labels', alpha=0.6)
plt.title('Mean Z-axis Acceleration with Labels')
plt.xlabel('Window Index')
plt.ylabel('Mean Z (m/s^2)')
plt.legend()
plt.tight_layout()
plt.show()

print("Done saved in extracted_features.csv")
