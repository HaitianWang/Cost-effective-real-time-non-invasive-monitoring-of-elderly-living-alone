import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取已经提取的特征数据集
features_df = pd.read_csv('extracted_features.csv')

# Step 7: 可视化所有特征
features_to_plot = ['mean_z', 
                    'std_z', 
                    'min_z', 
                    'max_z', 
                    'rms_z', 
                    'skew_z', 
                    'kurtosis_z', 
                    'fft_max_z', 
                    'psd_z', 
                    'dominant_freq_z']

# 创建每个特征的单独图像
for feature in features_to_plot:
    plt.figure(figsize=(10, 6))
    plt.plot(features_df.index, features_df[feature], label=feature, color='red')
    plt.scatter(features_df.index, features_df[feature], 
                c=features_df['label'].map({'Static': 'blue', 'Walking': 'yellow', 'Fall_Down': 'green'}), 
                label='Labels', alpha=0.6)
    plt.title(f'{feature} Over Time with Labels')
    plt.xlabel('Window Index')
    plt.ylabel(f'{feature}')
    plt.legend()
    plt.tight_layout()
    plt.show()
