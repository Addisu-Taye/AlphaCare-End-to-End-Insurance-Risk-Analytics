import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os  # Import the os module to handle directory creation

# Load the data
df = pd.read_csv('data/raw/machinelearningrating_v3.txt', sep='|')

# Basic data cleaning
def clean_data(df):
    # Convert TransactionMonth to datetime
    df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'])
    
    # Replace empty strings with NaN
    df.replace(' ', np.nan, inplace=True)
    
    # Handle numeric columns with .000000 values
    numeric_cols = ['TotalPremium', 'TotalClaims', 'CalculatedPremiumPerTerm', 
                   'CustomValueEstimate', 'CapitalOutstanding']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace(0, np.nan)  # Assuming 0 claims/premiums are missing data
    
    # Create useful derived columns
    df['VehicleAge'] = df['TransactionMonth'].dt.year - df['RegistrationYear']
    df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']
    
    # Convert binary columns to boolean
    binary_cols = ['AlarmImmobiliser', 'TrackingDevice', 'NewVehicle', 
                  'WrittenOff', 'Rebuilt', 'Converted', 'CrossBorder']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': True, 'No': False, None: np.nan})
    
    return df

cleaned_df = clean_data(df)

# Save the cleaned data
# Create the cleaned directory if it doesn't exist
os.makedirs('data/cleaned', exist_ok=True)

# Save the cleaned dataframe
cleaned_df.to_csv('data/cleaned/machinelearningrating_v3_cleaned.csv', index=False)