import pandas as pd
import re

# 定义读取非标准CSV格式数据的函数
def read_non_standard_csv(file_path):
    data = {
        'Timestamp': [],
        'X(m/s^2)': [],
        'Y(m/s^2)': [],
        'Z(m/s^2)': [],
        'Label': []
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # 使用正则表达式解析非标准格式的数据
            match = re.match(r'\[(.*?)\]\s*([\d.]+),\s*([\d.]+),\s*([\d.-]+),\s*(\w+)', line.strip())
            if match:
                timestamp = match.group(1)  # 保留原始时间戳格式
                x_value = float(match.group(2))
                y_value = float(match.group(3))
                z_value = float(match.group(4))
                label = match.group(5)
                
                data['Timestamp'].append(timestamp)
                data['X(m/s^2)'].append(x_value)
                data['Y(m/s^2)'].append(y_value)
                data['Z(m/s^2)'].append(z_value)
                data['Label'].append(label)
    
    return pd.DataFrame(data)

# 读取非标准CSV格式数据
file_path = 'Walk_1.csv'  # 替换为您的文件路径
df = read_non_standard_csv(file_path)

# 将数据写入标准CSV格式文件
output_file_path = 'Walk_1_Conversion.csv'  # 替换为您希望保存的文件路径
df.to_csv(output_file_path, index=False)

print(f"{output_file_path}")
