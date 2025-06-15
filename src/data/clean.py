import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Main data cleaning function
def clean_data(df):
    # Convert TransactionMonth to datetime
    df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'], errors='coerce')
    
    # Replace empty strings with NaN
    df.replace(' ', np.nan, inplace=True)
    
    # Handle numeric columns
    numeric_cols = ['TotalPremium', 'TotalClaims', 'CalculatedPremiumPerTerm', 
                   'CustomValueEstimate', 'CapitalOutstanding']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace(0, np.nan)
    
    # Derived columns
    df['VehicleAge'] = df['TransactionMonth'].dt.year - df['RegistrationYear']
    df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']
    
    # Convert binary columns to boolean
    binary_cols = ['AlarmImmobiliser', 'TrackingDevice', 'NewVehicle', 
                  'WrittenOff', 'Rebuilt', 'Converted', 'CrossBorder']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': True, 'No': False, None: np.nan})

    # Ensure output directories exist
    os.makedirs('data/cleaned', exist_ok=True)
    os.makedirs('plots/cleaning', exist_ok=True)

    # Save cleaned data
    df.to_csv('data/cleaned/cleaned_data.csv', index=False)

    # Generate Cleaning Plots
    generate_cleaning_plots(df)

    return df


def generate_cleaning_plots(df):
    # Plot 1: Missing Values
    missing = df.isnull().sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing.values, y=missing.index, palette='viridis')
    plt.title("Missing Values per Column")
    plt.xlabel("Missing Count")
    plt.ylabel("Columns")
    plt.tight_layout()
    plt.savefig("plots/cleaning/missing_values.png")
    plt.close()

    # Plot 2: Distribution of Numeric Columns After Cleaning
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), bins=30, kde=True, color='skyblue')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"plots/cleaning/{col}_distribution.png")
        plt.close()

    # Plot 3: Correlation Heatmap
    
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("plots/cleaning/correlation_heatmap.png")
    plt.close()
