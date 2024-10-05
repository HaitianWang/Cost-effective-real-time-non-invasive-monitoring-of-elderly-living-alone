import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取数据集
df = pd.read_csv('extracted_features.csv')

# Step 1: 将 'label' 列替换为数值以便计算相关性
label_mapping = {'Static': 0, 'Walking': 1, 'Fall_Down': 2}  # 设定标签映射
df['label_numeric'] = df['label'].map(label_mapping)

# Step 2: 计算与 Z 相关的特征和 label 之间的相关矩阵
z_related_columns = [col for col in df.columns if 'z' in col.lower()]  # 只筛选与 Z 相关的列
z_related_columns.append('label_numeric')  # 包含 'label_numeric'
df_z_related = df[z_related_columns]

# 计算相关矩阵
corr_matrix_z = df_z_related.corr()

# Step 3: 可视化相关矩阵 - 热力图，显示具体数值
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_z, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Z-Related Features and Label with Values')
plt.show()

# Step 4: 打印相关矩阵
print(corr_matrix_z)

# Step 5: 保存数值矩阵为 CSV 文件
corr_matrix_z.to_csv('correlation_matrix_z_related.csv')
print("Correlation matrix saved as 'correlation_matrix_z_related.csv'.")
