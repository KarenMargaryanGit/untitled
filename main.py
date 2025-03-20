import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Example data (replace with your actual data)
# Assuming you have a DataFrame `df` with features and a target column 'target'
# df = pd.read_csv('your_data.csv')

# For demonstration, let's create a synthetic dataset
np.random.seed(42)
data = {
    'feature1': np.random.rand(1000),
    'feature2': np.random.rand(1000),
    'feature3': np.random.rand(1000),
    'target': np.random.choice([0, 1], 1000, p=[0.7, 0.3])  # 70% label 0, 30% label 1
}
df = pd.DataFrame(data)

# Separate features and target
X = df.drop('target', axis=1)
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize CatBoostClassifier
model = CatBoostClassifier(iterations=100, learning_rate=0.1, depth=3, verbose=0)

# Train the model
model.fit(X_train, y_train)

# Get feature importance
feature_importance = model.get_feature_importance()

# Create a DataFrame to display feature importance
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importance
})

# Sort by importance
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Display feature importance
print("Feature Importance:")
print(importance_df)

# Compare feature distributions between label 0 and label 1
print("\nComparing Feature Distributions:")
for feature in X.columns:
    plt.figure(figsize=(8, 4))
    sns.kdeplot(df[df['target'] == 0][feature], label='Label 0', shade=True)
    sns.kdeplot(df[df['target'] == 1][feature], label='Label 1', shade=True)
    plt.title(f'Distribution of {feature} by Label')
    plt.xlabel(feature)
    plt.ylabel('Density')
    plt.legend()
    plt.show()
