def perform_eda(df):
    # 1. Basic statistics
    print("Basic Statistics:")
    print(df.describe(include='all'))
    
    # 2. Missing values analysis
    print("\nMissing Values:")
    missing_data = df.isnull().sum().sort_values(ascending=False)
    print(missing_data[missing_data > 0])
    
    # 3. Temporal analysis
    plt.figure(figsize=(12, 6))
    df.groupby(df['TransactionMonth'].dt.to_period('M'))['TotalPremium'].sum().plot()
    plt.title('Monthly Total Premium Over Time')
    plt.ylabel('Total Premium')
    plt.show()
    
    # 4. Loss Ratio by Province
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Province', y='LossRatio', data=df, estimator=np.mean)
    plt.title('Average Loss Ratio by Province')
    plt.xticks(rotation=45)
    plt.show()
    
    # 5. Vehicle Type Analysis
    plt.figure(figsize=(12, 6))
    vehicle_analysis = df.groupby('VehicleType').agg({'TotalClaims': 'sum', 'TotalPremium': 'sum'})
    vehicle_analysis['LossRatio'] = vehicle_analysis['TotalClaims'] / vehicle_analysis['TotalPremium']
    vehicle_analysis.sort_values('LossRatio', ascending=False).plot(kind='bar', y='LossRatio')
    plt.title('Loss Ratio by Vehicle Type')
    plt.ylabel('Loss Ratio')
    plt.show()
    
    # 6. Correlation Analysis
    numeric_df = df.select_dtypes(include=[np.number])
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Numerical Variables')
    plt.show()
    
    # 7. Outlier Detection
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df['TotalClaims'])
    plt.title('Boxplot of Total Claims')
    plt.show()

perform_eda(cleaned_df)