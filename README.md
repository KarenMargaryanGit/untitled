import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def plot_cluster_heatmap(features, labels, cmap="coolwarm", center=0):
    """
    Plots a heatmap of cluster centers with clusters as columns and features as rows.
    
    Parameters:
    - features: DataFrame of numerical features.
    - labels: Cluster labels (Series or array).
    - cmap: Colormap for the heatmap.
    - center: Center value for heatmap color scaling.
    """
    # Standardize features
    scaler = StandardScaler()
    features_scaled = pd.DataFrame(scaler.fit_transform(features), 
                                   index=features.index, 
                                   columns=features.columns)

    # Compute cluster centers
    cluster_centers_scaled = features_scaled.groupby(labels).mean()
    cluster_centers = features.groupby(labels).mean()
    
    # Sort clusters by mean value (optional)
    sorted_clusters = cluster_centers_scaled.mean(axis=1).sort_values(ascending=False).index
    cluster_centers_scaled = cluster_centers_scaled.loc[sorted_clusters]
    cluster_centers = cluster_centers.loc[sorted_clusters]

    # Transpose for heatmap: Features as rows, clusters as columns
    cluster_centers_scaled = cluster_centers_scaled.T
    cluster_centers = cluster_centers.T

    # Format annotation data
    annot_data = cluster_centers.map(lambda x: f"{x:,.0f}" if x >= 1e3 else f"{x:.1f}")

    # Plot heatmap
    plt.figure(figsize=(12, 36))
    sns.heatmap(cluster_centers_scaled, cmap=cmap, center=center, annot=annot_data.values, 
                xticklabels=cluster_centers_scaled.columns, yticklabels=cluster_centers_scaled.index, 
                linewidths=0.5, cbar=False, fmt="")

    plt.xticks(fontsize=8, rotation=0)
    plt.yticks(fontsize=8, rotation=0)
    plt.title("Cluster Centers Heatmap (Clusters as Columns, Features as Rows)")
    plt.show()
