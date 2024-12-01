import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# 读取数据集
df = pd.read_csv(r'C:\Simon\Master of Professional Engineering\Engineering Research Project\Experiment\Vibration_folder\z_axis_extracted_features.csv')

# 删除含有 NaN 的行
df.dropna(inplace=True)

# Step 1: 准备数据（特征和标签）
X = df.drop(columns=['label'])
y = df['label']

# 将标签进行二值化处理（适用于多分类任务中的ROC曲线）
classes = y.unique()
y_bin = label_binarize(y, classes=classes)

# Step 2: 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.90, random_state=66)

# Step 3: 标准化数据
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 4: 定义机器学习模型
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Support Vector Machine": SVC(kernel='linear', probability=True, random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42)
}

# Step 5: 创建ROC曲线绘图
plt.figure(figsize=(10, 8))

# Step 6: 训练并评估模型
for name, model in models.items():
    print(f"Training and Evaluating {name}...")

    # 训练模型
    model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = model.predict(X_test)

    # 分类报告
    print(f"Classification Report for {name}:\n{classification_report(y_test, y_pred)}\n")

    # 混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix for {name}:\n{cm}\n")

    # 可视化混淆矩阵
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix for {name}')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    # ROC曲线和AUC
    if len(classes) == 2:  # 二分类情况
        y_score = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=2, label=f'{name} (AUC = {roc_auc:.2f})')
    else:  # 多分类情况
        y_score = model.predict_proba(X_test) if hasattr(model, "predict_proba") else model.decision_function(X_test)
        for i, class_name in enumerate(classes):
            fpr, tpr, _ = roc_curve(y_bin[:, i], y_score[:, i])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'{name} - Class {class_name} (AUC = {roc_auc:.2f})')

# 绘制所有模型的ROC曲线
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Chance')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Different Models')
plt.legend(loc="lower right")
plt.show()
