import os
import pandas as pd

# 存储合并数据的列表
combined_data = []

# 遍历文件夹中的每个文件
for i in range(1, 3):
    file_name = f"Synthetic {i}.csv"
    
    # 检查文件是否存在
    if os.path.exists(file_name):
        # 读取当前文件数据
        df = pd.read_csv(file_name)
        
        # 添加一列标记当前数据集是哪个人的数据（如编号）
        df['Person_ID'] = f'Person_{i}'
        
        # 将数据添加到合并列表中
        combined_data.append(df)
    else:
        print(f"File {file_name} not found.")

# 将所有数据合并成一个DataFrame
combined_df = pd.concat(combined_data, ignore_index=True)

# 保存合并后的数据到一个新的CSV文件中
combined_df.to_csv('combined_accelerometer_data.csv', index=False)

print("saved in combined_accelerometer_data.csv")
