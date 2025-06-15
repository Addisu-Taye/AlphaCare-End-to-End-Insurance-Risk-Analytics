import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Master EDA Module
# ------------------------------------------------------------------

def univariate_analysis(df):
    """Performs univariate EDA: statistics + single variable plots"""
    
    # Ensure folders exist
    os.makedirs('data/eda/univariate', exist_ok=True)
    os.makedirs('plots/eda_plots/univariate', exist_ok=True)

    # 1. Descriptive Statistics
    stats = df.describe(include='all')
    stats.to_csv('data/eda/univariate/basic_statistics.csv')

    # 2. Missing Values
    missing = df.isnull().sum().sort_values(ascending=False)
    missing.to_csv('data/eda/univariate/missing_values.csv')

    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing[missing > 0].values, y=missing[missing > 0].index, palette="viridis")
    plt.title("Missing Values per Column")
    plt.xlabel("Missing Count")
    plt.tight_layout()
    plt.savefig("plots/eda_plots/univariate/missing_values_barplot.png")
    plt.close()

    # 3. Distributions for Numeric Columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color='skyblue')
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(f"plots/eda_plots/univariate/{col}_distribution.png")
        plt.close()


def bivariate_analysis(df):
    """Performs bivariate EDA: relationships between variables"""

    # Ensure folders exist
    os.makedirs('data/eda/bivariate', exist_ok=True)
    os.makedirs('plots/eda_plots/bivariate', exist_ok=True)

    # 1. Monthly Total Premium Over Time
    monthly_premium = df.groupby(df['TransactionMonth'].dt.to_period('M'))['TotalPremium'].sum()
    monthly_premium.to_csv("data/eda/bivariate/monthly_total_premium.csv")

    plt.figure(figsize=(12, 6))
    monthly_premium.plot()
    plt.title('Monthly Total Premium Over Time')
    plt.ylabel('Total Premium')
    plt.xlabel('Transaction Month')
    plt.tight_layout()
    plt.savefig("plots/eda_plots/bivariate/monthly_total_premium.png")
    plt.close()

    # 2. Loss Ratio by Province
    province_loss = df.groupby('Province')['LossRatio'].mean()
    province_loss.to_csv("data/eda/bivariate/loss_ratio_by_province.csv")

    plt.figure(figsize=(10, 6))
    sns.barplot(x=province_loss.index, y=province_loss.values, palette='pastel')
    plt.title('Average Loss Ratio by Province')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/eda_plots/bivariate/loss_ratio_by_province.png")
    plt.close()

    # 3. Loss Ratio by Vehicle Type
    vehicle_analysis = df.groupby('VehicleType').agg({'TotalClaims':'sum','TotalPremium':'sum'})
    vehicle_analysis['LossRatio'] = vehicle_analysis['TotalClaims'] / vehicle_analysis['TotalPremium']
    vehicle_analysis.sort_values('LossRatio', ascending=False).to_csv("data/eda/bivariate/loss_ratio_by_vehicle_type.csv")

    plt.figure(figsize=(12, 6))
    vehicle_analysis['LossRatio'].sort_values(ascending=False).plot(kind='bar', color='steelblue')
    plt.title('Loss Ratio by Vehicle Type')
    plt.ylabel('Loss Ratio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/eda_plots/bivariate/loss_ratio_by_vehicle_type.png")
    plt.close()

    # 4. Correlation Heatmap
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    corr.to_csv("data/eda/bivariate/correlation_matrix.csv")

    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig("plots/eda_plots/bivariate/correlation_matrix.png")
    plt.close()

    # 5. Outlier Detection (Boxplot of Total Claims)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['TotalClaims'], color="lightcoral")
    plt.title('Boxplot of Total Claims')
    plt.tight_layout()
    plt.savefig("plots/eda_plots/bivariate/total_claims_boxplot.png")
    plt.close()


# Master EDA pipeline runner
def run_full_eda(df):
    univariate_analysis(df)
    bivariate_analysis(df)
    print("✅ Full EDA complete. All outputs saved.")
