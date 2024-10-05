import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据集
df = pd.read_csv('extracted_features.csv')

# 只选择与Z轴相关的特征
features = ['mean_z', 'std_z', 'max_z', 'psd_z', 'dominant_freq_z']
X = df[features]
y = df['label']

# 将类别标签转换为数值 (0: No_Fall, 1: Fall_Down)
y_binary = y.map({'Static': 0, 'Walking': 0, 'Fall_Down': 1})

# 划分数据集为训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)

# 标准化数据
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 定义模型集合
models = {
    "Random Forest": RandomForestClassifier(class_weight='balanced', n_estimators=200, max_depth=10, random_state=42),
    "Support Vector Machine": SVC(kernel='linear', probability=True, C=0.5, class_weight='balanced', random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Logistic Regression": LogisticRegression(class_weight='balanced', random_state=42),
    "Decision Tree": DecisionTreeClassifier(class_weight='balanced', random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
}

# 绘制每个模型的ROC曲线
plt.figure(figsize=(15, 10))
for name, model in models.items():
    print(f"Training and Evaluating {name}...")
    
    # 训练模型
    model.fit(X_train_scaled, y_train)
    
    # 预测概率
    y_pred_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    # 绘制ROC曲线
    fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=2, label=f'{name} (AUC = {roc_auc:.2f})')

# 绘制参考线和设置图表
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Different Models')
plt.legend(loc="lower right")
plt.show()
