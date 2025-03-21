# Separate data into two clusters
cluster_0 = df[df['target'] == 0]
cluster_1 = df[df['target'] == 1]

# Statistical summary comparison
print("Statistical Summary:")
for feature in df.columns[:-1]:  # Exclude the target column
    print(f"\nFeature: {feature}")
    print(f"Cluster 0 - Mean: {cluster_0[feature].mean():.4f}, Median: {cluster_0[feature].median():.4f}")
    print(f"Cluster 1 - Mean: {cluster_1[feature].mean():.4f}, Median: {cluster_1[feature].median():.4f}")

    # Perform t-test (for normally distributed data)
    t_stat, p_value = ttest_ind(cluster_0[feature], cluster_1[feature])
    print(f"T-test: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")

    # Perform Mann-Whitney U test (for non-parametric data)
    u_stat, p_value_mw = mannwhitneyu(cluster_0[feature], cluster_1[feature])
    print(f"Mann-Whitney U: U-statistic = {u_stat:.4f}, p-value = {p_value_mw:.4f}")

# Visualize differences using box plots
print("\nVisualizing Differences:")
for feature in df.columns[:-1]:  # Exclude the target column
    plt.figure(figsize=(8, 4))
    sns.boxplot(x='target', y=feature, data=df, palette='Set2')
    plt.title(f'Comparison of {feature} between Clusters')
    plt.xlabel('Cluster')
    plt.ylabel(feature)
    plt.xticks(ticks=[0, 1], labels=['Cluster 0', 'Cluster 1'])
    plt.show()
