import pandas as pd
import numpy as np

# 仅读取Z(m/s^2)列的数据
z_data = pd.read_csv('Static3_1s.csv', usecols=['Z(m/s^2)'])
print(z_data.head(10))


# # 读取CSV数据，并将Timestamp列解析为日期时间格式
# try:
#     data = pd.read_csv('Static3_1s.csv', parse_dates=['Timestamp(ms)'], dtype={'Z(m/s^2)': float})
# except Exception as e:
#     print("Error reading Z(m/s^2) column:", e)

# # 打印检查Z轴数据
# print("Z-axis data:", data['Z(m/s^2)'].head())

# # 检查所有Z(m/s^2)列的NaN行
# print("NaN values in Z-axis:", data[data['Z(m/s^2)'].isna()])
