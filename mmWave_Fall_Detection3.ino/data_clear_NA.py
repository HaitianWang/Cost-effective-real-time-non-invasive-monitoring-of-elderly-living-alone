import pandas as pd
import numpy as np

# 读取数据
file_path = "radar_data.csv"
data = pd.read_csv(file_path)

# 遍历数据集并进行清洗
for i in range(1, len(data) - 1):
    if data.loc[i, "Target Number"] == 0:
        # 修改目标数量为1
        data.loc[i, "Target Number"] = 1

        # 处理距离值
        prev_distance = data.loc[i - 1, "Distance(m)"]
        next_distance = data.loc[i + 1, "Distance(m)"]

        if prev_distance != "N/A" and next_distance != "N/A":
            # 如果前后都有有效的距离值，取平均值
            data.loc[i, "Distance(m)"] = (float(prev_distance) + float(next_distance)) / 2
        elif prev_distance != "N/A":
            # 如果只有前一个距离有效，用前一个距离
            data.loc[i, "Distance(m)"] = float(prev_distance)
        elif next_distance != "N/A":
            # 如果只有后一个距离有效，用后一个距离
            data.loc[i, "Distance(m)"] = float(next_distance)
        else:
            # 如果前后距离都不可用，则留空，之后统一插值
            data.loc[i, "Distance(m)"] = np.nan

        # 设置速度为 0.01 - 0.11 之间的随机值
        data.loc[i, "Speed(m/s)"] = round(np.random.uniform(0.01, 0.11), 2)

        # 设置能量为 50 - 100 之间的随机值
        data.loc[i, "Energy"] = np.random.randint(50, 101)

# 对所有可能出现的连续缺失距离值进行线性插值
data["Distance(m)"] = data["Distance(m)"].interpolate(method='linear')

# 如果数据的边缘还存在缺失值，则使用最近有效值进行填充
data["Distance(m)"].fillna(method='bfill', inplace=True)
data["Distance(m)"].fillna(method='ffill', inplace=True)

# 保存清洗后的数据
data.to_csv("cleaned_radar_data_NA.csv", index=False)
