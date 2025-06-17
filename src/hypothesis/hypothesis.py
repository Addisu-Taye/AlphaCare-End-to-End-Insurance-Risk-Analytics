import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor # Make sure xgboost is installed (pip install xgboost)
from sklearn.metrics import mean_squared_error, r2_score
import shap # Make sure shap is installed (pip install shap)
from docx import Document # Make sure python-docx is installed (pip install python-docx)
from docx.shared import Inches
import logging
from datetime import datetime
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Hypothesis testing functions
def perform_hypothesis_tests(df):
    """Perform all hypothesis tests"""
    logger.info("Performing hypothesis tests...")
    results = {}

    # 1. Province Risk Differences
    # Claim Frequency
    contingency = pd.crosstab(df['Province'], df['HasClaim'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    results['province_claim_frequency'] = {
        'test': 'Chi-square',
        'chi2': chi2,
        'p_value': p,
        'conclusion': 'Reject H0' if p < 0.05 else 'Fail to reject H0'
    }

    # Claim Severity
    province_groups = [group['TotalClaims'] for name, group in df[df['TotalClaims'] > 0].groupby('Province')]
    f_stat, p_val = stats.f_oneway(*province_groups)
    results['province_claim_severity'] = {
        'test': 'ANOVA',
        'f_stat': f_stat,
        'p_value': p_val,
        'conclusion': 'Reject H0' if p_val < 0.05 else 'Fail to reject H0'
    }

    # Post-hoc test if ANOVA significant
    if p_val < 0.05:
        tukey = pairwise_tukeyhsd(
            df[df['TotalClaims'] > 0]['TotalClaims'],
            df[df['TotalClaims'] > 0]['Province']
        )
        results['province_posthoc'] = tukey.summary()

        # Plot post-hoc results
        plt.figure(figsize=(10, 6))
        tukey.plot_simultaneous()
        plt.title('Tukey HSD Test for Claim Severity by Province')
        plt.tight_layout()
        plt.savefig('plots/hypothesis_testing/province_tukey.png')
        plt.close()

    # 2. Zip Code Risk Differences
    # Sample analysis for top 10 zip codes by policy count
    top_zips = df['PostalCode'].value_counts().nlargest(10).index
    zip_df = df[df['PostalCode'].isin(top_zips)]

    # Claim Frequency
    zip_contingency = pd.crosstab(zip_df['PostalCode'], zip_df['HasClaim'])
    chi2, p, dof, expected = stats.chi2_contingency(zip_contingency)
    results['zip_claim_frequency'] = {
        'test': 'Chi-square',
        'chi2': chi2,
        'p_value': p,
        'conclusion': 'Reject H0' if p < 0.05 else 'Fail to reject H0'
    }

    # 3. Zip Code Margin Differences
    f_stat, p_val = stats.f_oneway(
        *[group['Margin'] for name, group in zip_df.groupby('PostalCode')]
    )
    results['zip_margin'] = {
        'test': 'ANOVA',
        'f_stat': f_stat,
        'p_value': p_val,
        'conclusion': 'Reject H0' if p_val < 0.05 else 'Fail to reject H0'
    }

    # 4. Gender Risk Differences
    # Filter for specified genders only
    gender_df = df[df['Gender'].isin(['Male', 'Female'])]

    # Claim Frequency
    gender_contingency = pd.crosstab(gender_df['Gender'], gender_df['HasClaim'])
    chi2, p, dof, expected = stats.chi2_contingency(gender_contingency)
    results['gender_claim_frequency'] = {
        'test': 'Chi-square',
        'chi2': chi2,
        'p_value': p,
        'conclusion': 'Reject H0' if p < 0.05 else 'Fail to reject H0'
    }

    # Claim Severity
    male_claims = gender_df[(gender_df['Gender'] == 'Male') & (gender_df['TotalClaims'] > 0)]['TotalClaims']
    female_claims = gender_df[(gender_df['Gender'] == 'Female') & (gender_df['TotalClaims'] > 0)]['TotalClaims']
    t_stat, p_val = stats.ttest_ind(male_claims, female_claims, equal_var=False)
    results['gender_claim_severity'] = {
        'test': 'Welch\'s t-test',
        't_stat': t_stat,
        'p_value': p_val,
        'conclusion': 'Reject H0' if p_val < 0.05 else 'Fail to reject H0'
    }

    return results
