import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.fftpack import fft
from scipy.signal import welch

# 读取标注后的数据集
df = pd.read_csv('Data_Augmentation_Relabeling.csv')

# 确保数据按照时间戳排序
df = df.sort_values(by='Timestamp (ms)')

# Step 1: 窗口化数据 (1秒=100行数据)
window_size = 100  # 1秒的窗口大小（假设采样率是100Hz）

features_list = []
labels = []

# Step 2: 特征提取函数（只针对Z轴）
def extract_features(window):
    features = {}
    
    # 时域特征
    features['mean_z'] = window['Z_smoothed'].mean()  # Z轴的均值
    features['std_z'] = window['Z_smoothed'].std()    # Z轴的标准差
    features['min_z'] = window['Z_smoothed'].min()    # Z轴的最小值
    features['max_z'] = window['Z_smoothed'].max()    # Z轴的最大值
    features['rms_z'] = np.sqrt(np.mean(window['Z_smoothed'] ** 2))  # Z轴的均方根值
    features['skew_z'] = skew(window['Z_smoothed'])  # Z轴的偏度
    features['kurtosis_z'] = kurtosis(window['Z_smoothed'])  # Z轴的峰度

    # 频域特征
    Z_array = window['Z_smoothed'].values  # 转换为NumPy数组

    Z_fft = fft(Z_array)  # Z轴的FFT
    features['fft_max_z'] = np.abs(Z_fft).max()  # Z轴的FFT最大值

    # 修改这里：明确设置 nperseg 为窗口大小
    freqs, psd_z = welch(Z_array, fs=100, nperseg=len(Z_array))  # Z轴的功率谱密度
    features['psd_z'] = np.mean(psd_z)  # Z轴的平均功率谱密度
    features['dominant_freq_z'] = freqs[np.argmax(psd_z)]  # Z轴的主频率

    return features


# Step 3: 滑动窗口特征提取
for i in range(0, len(df), window_size):
    window = df.iloc[i:i + window_size]
    if len(window) < window_size:
        continue  # 如果窗口小于1秒，则跳过
    
    # 提取特征
    features = extract_features(window)
    
    # 修改这里：只要窗口内有一次 fall down（假设 fall down 对应标签为1），整个窗口标记为 fall down
    if (window['Label'] == 1).any():
        features['label'] = 1  # 标记为 fall down
    else:
        features['label'] = 0  # 否则标记为 no fall down
    
    features_list.append(features)

# Step 4: 将提取的特征转换为DataFrame
features_df = pd.DataFrame(features_list)

# Step 5: 保存提取的特征数据
features_df.to_csv('z_axis_extracted_features.csv', index=False)
print("Feature extraction completed. Saved to 'z_axis_extracted_features.csv'")
