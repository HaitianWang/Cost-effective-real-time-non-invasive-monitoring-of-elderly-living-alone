import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据集
df = pd.read_csv(r'C:\Simon\Master of Professional Engineering\Engineering Research Project\Experiment\Vibration_folder\z_axis_extracted_features.csv')

# 只选择与Z轴相关的特征
features = ['mean_z', 'std_z', 'max_z', 'psd_z', 'dominant_freq_z']
X = df[features]
y = df['label']

# 将类别标签转换为数值
y_numeric = y.map({'Static': 0, 'Walking': 1, 'Fall_Down': 2})

# 将标签二值化用于绘制多分类的ROC曲线
y_binary = label_binarize(y_numeric, classes=[0, 1, 2])
n_classes = y_binary.shape[1]

# 划分数据集为训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(X, y_numeric, test_size=0.2, random_state=42)

# 标准化数据
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 使用递归特征消除 (RFE) 进行特征选择

# 定义SVM模型，设置更高的惩罚参数C和设置class_weight为'balanced'以提高recall
svm = SVC(kernel='linear', probability=True, C=0.5, class_weight='balanced')

# 使用RFE进行特征选择
rfe_svm = RFE(estimator=svm, n_features_to_select=3)
rfe_svm.fit(X_train_scaled, y_train)

# 训练并评估SVM模型
svm.fit(X_train_scaled[:, rfe_svm.support_], y_train)
y_pred_svm = svm.predict(X_test_scaled[:, rfe_svm.support_])
y_pred_svm_prob = svm.predict_proba(X_test_scaled[:, rfe_svm.support_])

# 输出SVM结果
print("SVM accuracy:", accuracy_score(y_test, y_pred_svm))
print("SVM classification report:\n", classification_report(y_test, y_pred_svm))

# 绘制混淆矩阵
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)
sns.heatmap(conf_matrix_svm, annot=True, fmt="d", cmap="Blues")
plt.title('SVM Confusion Matrix')
plt.show()

# 绘制SVM的ROC曲线
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_binary[:, i], y_pred_svm_prob[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure()
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label="Random guess")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - SVM')
plt.legend(loc='lower right')
plt.show()

# 随机森林模型，设置class_weight为'balanced'以提高recall
rf = RandomForestClassifier(class_weight='balanced', n_estimators=200, max_depth=10, random_state=42)

# 使用RFE进行特征选择
rfe_rf = RFE(estimator=rf, n_features_to_select=3)
rfe_rf.fit(X_train_scaled, y_train)

# 训练并评估随机森林模型
rf.fit(X_train_scaled[:, rfe_rf.support_], y_train)
y_pred_rf = rf.predict(X_test_scaled[:, rfe_rf.support_])
y_pred_rf_prob = rf.predict_proba(X_test_scaled[:, rfe_rf.support_])

# 输出随机森林结果
print("Random Forest accuracy:", accuracy_score(y_test, y_pred_rf))
print("Random Forest classification report:\n", classification_report(y_test, y_pred_rf))

# 绘制随机森林的混淆矩阵
conf_matrix_rf = confusion_matrix(y_test, y_pred_rf)
sns.heatmap(conf_matrix_rf, annot=True, fmt="d", cmap="Greens")
plt.title('Random Forest Confusion Matrix')
plt.show()

# 绘制随机森林的ROC曲线
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_binary[:, i], y_pred_rf_prob[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure()
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label="Random guess")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Random Forest')
plt.legend(loc='lower right')
plt.show()
