import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('./Static_1_Conversion.csv', parse_dates=['Timestamp'])

# 检查数据格式
print(data.head())

# 数据去噪 - 使用低通滤波器去除高频噪声
def low_pass_filter(data, cutoff_frequency, sampling_rate):
    nyquist_frequency = 0.5 * sampling_rate
    normal_cutoff = cutoff_frequency / nyquist_frequency
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# 设置滤波器参数
sampling_rate = 100  # 数据采样频率
cutoff_frequency = 20  # 截止频率

# 对X, Y, Z轴加速度数据进行滤波
data['X_filtered'] = low_pass_filter(data['X(m/s^2)'], cutoff_frequency, sampling_rate)
data['Y_filtered'] = low_pass_filter(data['Y(m/s^2)'], cutoff_frequency, sampling_rate)
data['Z_filtered'] = low_pass_filter(data['Z(m/s^2)'], cutoff_frequency, sampling_rate)

# 查看滤波后的数据
print(data[['X(m/s^2)', 'X_filtered']].head())

# 可视化滤波效果
plt.figure(figsize=(10, 5))
plt.plot(data['Timestamp'], data['X(m/s^2)'], label='Original X', alpha=0.5)
plt.plot(data['Timestamp'], data['X_filtered'], label='Filtered X', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Low-Pass Filter on X-axis Acceleration')
plt.legend()
plt.show()

# 定义分段函数
def segment_data(data, window_size=2, overlap=0.5):
    segments = []
    labels = []
    start = 0
    step = int(window_size * (1 - overlap) * sampling_rate)
    while start < len(data):
        end = start + int(window_size * sampling_rate)
        if end > len(data):
            break
        segment = data.iloc[start:end]
        label = segment['Label'].mode()[0]  # 使用众数作为片段的标签
        segments.append(segment)
        labels.append(label)
        start += step
    return segments, labels

# 分段
window_size = 2  # 秒
overlap = 0.5  # 重叠率
segments, labels = segment_data(data, window_size, overlap)

# 检查分段结果
print(f"Total segments: {len(segments)}")
print(segments[0].head())

# 定义特征提取函数
def extract_time_domain_features(segment):
    features = {}
    features['mean_x'] = segment['X_filtered'].mean()
    features['mean_y'] = segment['Y_filtered'].mean()
    features['mean_z'] = segment['Z_filtered'].mean()
    
    features['std_x'] = segment['X_filtered'].std()
    features['std_y'] = segment['Y_filtered'].std()
    features['std_z'] = segment['Z_filtered'].std()
    
    features['max_x'] = segment['X_filtered'].max()
    features['max_y'] = segment['Y_filtered'].max()
    features['max_z'] = segment['Z_filtered'].max()
    
    features['min_x'] = segment['X_filtered'].min()
    features['min_y'] = segment['Y_filtered'].min()
    features['min_z'] = segment['Z_filtered'].min()
    
    features['rms_x'] = np.sqrt(np.mean(segment['X_filtered']**2))
    features['rms_y'] = np.sqrt(np.mean(segment['Y_filtered']**2))
    features['rms_z'] = np.sqrt(np.mean(segment['Z_filtered']**2))
    
    return features

# 提取所有段的特征
time_domain_features = [extract_time_domain_features(seg) for seg in segments]

# 转换为DataFrame
features_df = pd.DataFrame(time_domain_features)
print(features_df.head())


from scipy.fftpack import fft

# 定义频域特征提取函数
def extract_frequency_domain_features(segment, sampling_rate):
    features = {}
    N = len(segment)
    
    # FFT
    X_fft = fft(segment['X_filtered'])
    Y_fft = fft(segment['Y_filtered'])
    Z_fft = fft(segment['Z_filtered'])
    
    # 计算频率分量
    freqs = np.fft.fftfreq(N, 1/sampling_rate)
    
    # 只使用正频率部分
    X_magnitude = np.abs(X_fft[:N//2])
    Y_magnitude = np.abs(Y_fft[:N//2])
    Z_magnitude = np.abs(Z_fft[:N//2])
    
    features['max_freq_x'] = freqs[np.argmax(X_magnitude)]
    features['max_freq_y'] = freqs[np.argmax(Y_magnitude)]
    features['max_freq_z'] = freqs[np.argmax(Z_magnitude)]
    
    features['psd_x'] = np.mean(X_magnitude**2)
    features['psd_y'] = np.mean(Y_magnitude**2)
    features['psd_z'] = np.mean(Z_magnitude**2)
    
    return features

# 提取所有段的频域特征
frequency_domain_features = [extract_frequency_domain_features(seg, sampling_rate) for seg in segments]

# 转换为DataFrame
frequency_features_df = pd.DataFrame(frequency_domain_features)
print(frequency_features_df.head())



from sklearn.preprocessing import StandardScaler

# 整合特征
all_features = pd.concat([features_df, frequency_features_df], axis=1)

# 标准化特征
scaler = StandardScaler()
scaled_features = scaler.fit_transform(all_features)

# 转换为DataFrame
scaled_features_df = pd.DataFrame(scaled_features, columns=all_features.columns)
print(scaled_features_df.head())




