import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# 读取数据
data = pd.read_csv('Data_Fall_Down_Bathroom_Floor.csv')

# 特征和标签
X = data[['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)', 'Magnitude']]
y = data['label']

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# 初始化并训练SVM模型
svm_model = SVC(kernel='linear', C=1.0, random_state=42)
svm_model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = svm_model.predict(X_test)

# 输出分类报告和准确率
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# 保存模型
import joblib
joblib.dump(svm_model, 'fall_detection_svm_model.pkl')











