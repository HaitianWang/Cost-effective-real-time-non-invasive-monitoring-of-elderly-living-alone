import pandas as pd
import numpy as np

# 读取数据集
df = pd.read_csv('cleaned_smoothed_labeled_accelerometer_data.csv')

# 将类别标签转换为数值 (0: No_Fall, 1: Fall_Down)
df['Label'] = df['Label'].map({'Static': 0, 'Walking': 0, 'Fall_Down': 1})

# Step 1: 数据增强，增加摔倒数据
def augment_data(data, factor=2):
    augmented_data = data.copy()
    
    # 只对数值型列添加噪声，跳过非数值列
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    for i in range(factor - 1):
        noise = np.random.normal(0, 0.1, size=data[numeric_cols].shape)
        augmented_sample = data[numeric_cols] + noise  # 只对数值列添加噪声
        augmented_sample = pd.concat([augmented_sample, data.drop(columns=numeric_cols)], axis=1)  # 加回非数值列
        augmented_data = pd.concat([augmented_data, augmented_sample])
        
    return augmented_data

# 增加摔倒类数据
fall_data = df[df['Label'] == 1]
augmented_fall_data = augment_data(fall_data)

# 将增强的数据合并回原始数据集
df = pd.concat([df, augmented_fall_data]).reset_index(drop=True)

# Step 2: 将标签分为fall down 和 no fall down两类
# 已经在上一步完成，摔倒事件标记为1，其他的标记为0

# Step 3: 使用100ms的窗口重新标注
# 假设采样率是100Hz, 即每行代表10ms，100ms窗口就是10行数据
window_size = 10  # 100ms窗口大小（每行代表10ms）
new_labels = []

for i in range(0, len(df), window_size):
    window = df.iloc[i:i + window_size]
    if len(window) < window_size:
        continue  # 如果窗口小于100ms，则跳过
    label = 1 if window['Label'].sum() > 0 else 0  # 如果窗口内有任何Fall_Down，则标记为1，否则为0
    new_labels.extend([label] * window_size)  # 为该窗口内的每一行都打上相同的标签

# 确保新标注的标签数量和原始数据集匹配
df = df.iloc[:len(new_labels)]
df['Label'] = new_labels

# 保存新数new_cleaned_labeled_data.csv据集
df.to_csv('Data_Augmentation_Relabeling.csv', index=False)
print("Data_Augmentation_Relabeling.csv'")
