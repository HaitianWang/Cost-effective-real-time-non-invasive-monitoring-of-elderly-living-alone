import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 读取数据集
df = pd.read_csv('extracted_features.csv')

# Step 1: 准备数据
X = df.drop(columns=['label'])  # 特征
y = df['label']  # 标签

# 将标签进行编码处理（转换为数字形式，假设 'Static' = 0, 'Walking' = 1, 'Fall_Down' = 2）
y_numeric = y.map({'Static': 0, 'Walking': 1, 'Fall_Down': 2})

# Step 2: 使用 RandomForestClassifier 作为基模型
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Step 3: 使用 RFE 进行递归特征消除，选择前10个重要特征
selector = RFE(estimator=model, n_features_to_select=10, step=1)
selector = selector.fit(X, y_numeric)

# Step 4: 输出被选择的特征
selected_features = X.columns[selector.support_]
print("Selected Features: ", selected_features)

# Step 5: 将选出的特征数据保存
selected_features_df = X[selected_features]
selected_features_df['label'] = y  # 重新加上标签
selected_features_df.to_csv('selected_features_via_rfe.csv', index=False)

# 输出排序的特征重要性
ranking = selector.ranking_
feature_ranking = pd.DataFrame({'Feature': X.columns, 'Ranking': ranking})
print(feature_ranking.sort_values(by='Ranking'))
