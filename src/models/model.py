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

# Modeling functions
def build_models(df):
    """Build and evaluate predictive models with robust missing value handling"""
    logger.info("Building predictive models...")
    results = {}

    try:
        # Prepare data for claim severity model
        claims_df = df[df['TotalClaims'] > 0].copy()

        # Define expected features with fallback options
        feature_map = {
            'VehicleAge': ['VehicleAge', 'vehicle_age', 'Age'],
            'Cubiccapacity': ['Cubiccapacity', 'cubiccapacity', 'EngineSize', 'engine_size'],
            'Kilowatts': ['Kilowatts', 'kilowatts', 'Power', 'power'],
            'SumInsured': ['SumInsured', 'sum_insured', 'Coverage'],
            'Province': ['Province', 'province', 'Region'],
            'VehicleType': ['VehicleType', 'vehicle_type', 'Type'],
            'CoverType': ['CoverType', 'cover_type', 'CoverageType']
        }

        # Find actual column names in the dataframe
        available_features = {}
        for feature_name, possible_names in feature_map.items():
            for name in possible_names:
                if name in claims_df.columns:
                    available_features[feature_name] = name
                    break

        # Check if we have minimum required features
        required_features = ['VehicleAge', 'SumInsured', 'Province', 'VehicleType', 'CoverType']
        missing_features = [f for f in required_features if f not in available_features]

        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}. Available columns: {list(claims_df.columns)}")

        # Separate numeric and categorical features
        # Ensure only available features are used
        numeric_features = [available_features[f] for f in ['VehicleAge', 'Cubiccapacity', 'Kilowatts', 'SumInsured'] if f in available_features]
        categorical_features = [available_features[f] for f in ['Province', 'VehicleType', 'CoverType'] if f in available_features]

        logger.info(f"Using numeric features: {numeric_features}")
        logger.info(f"Using categorical features: {categorical_features}")

        # Check for missing values
        logger.info("Checking for missing values...")
        missing_values = claims_df[numeric_features + categorical_features].isna().sum()
        logger.info(f"Missing values per column:\n{missing_values}")

        # Create preprocessing pipeline
        numeric_transformer = make_pipeline(
            SimpleImputer(strategy='median'),  # Impute missing numeric values with median
        )

        categorical_transformer = make_pipeline(
            SimpleImputer(strategy='most_frequent'),  # Impute missing categorical values with mode
            OneHotEncoder(handle_unknown='ignore')
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )

        # Prepare target
        y = claims_df['TotalClaims']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            claims_df[numeric_features + categorical_features], # Pass original features to preprocessor
            y,
            test_size=0.3,
            random_state=42
        )

        # 1. Linear Regression with imputation
        logger.info("Training Linear Regression model...")
        lr_pipeline = make_pipeline(
            preprocessor,
            LinearRegression()
        )
        lr_pipeline.fit(X_train, y_train)
        lr_preds = lr_pipeline.predict(X_test)
        results['linear_regression'] = {
            'rmse': mean_squared_error(y_test, lr_preds, squared=False),
            'r2': r2_score(y_test, lr_preds)
        }

        # 2. Random Forest (handles missing values in numeric features)
        logger.info("Training Random Forest model...")
        rf_pipeline = make_pipeline(
            preprocessor,
            RandomForestRegressor(random_state=42, n_jobs=-1)
        )
        rf_pipeline.fit(X_train, y_train)
        rf_preds = rf_pipeline.predict(X_test)
        results['random_forest'] = {
            'rmse': mean_squared_error(y_test, rf_preds, squared=False),
            'r2': r2_score(y_test, rf_preds)
        }

        # 3. XGBoost
        logger.info("Training XGBoost model...")
        xgb_pipeline = make_pipeline(
            preprocessor,
            XGBRegressor(random_state=42, n_jobs=-1) # REMOVED enable_categorical=True
        )
        xgb_pipeline.fit(X_train, y_train)
        xgb_preds = xgb_pipeline.predict(X_test)
        results['xgboost'] = {
            'rmse': mean_squared_error(y_test, xgb_preds, squared=False),
            'r2': r2_score(y_test, xgb_preds)
        }

        # Feature Importance Analysis with SHAP
        try:
            logger.info("Calculating feature importance...")
            # Get feature names after preprocessing
            # This is critical for SHAP to display correctly with one-hot encoding
            # Apply preprocessing to a small sample of training data to get feature names
            X_train_transformed_sample = preprocessor.transform(X_train.head(1))
            
            # Get names for numeric features
            num_feature_names_out = numeric_features
            
            # Get names for categorical features from the OneHotEncoder
            # Access the OneHotEncoder step within the 'cat' transformer
            cat_ohe_step = preprocessor.named_transformers_['cat'].named_steps['onehotencoder']
            cat_feature_names_out = cat_ohe_step.get_feature_names_out(categorical_features)
            
            feature_names = list(num_feature_names_out) + list(cat_feature_names_out)

            # Get the trained XGBoost model from the pipeline
            xgb_model = xgb_pipeline.named_steps['xgbregressor']

            # Get the transformed training data
            X_train_transformed = preprocessor.transform(X_train)

            # Ensure X_train_transformed is in a format SHAP expects, e.g., a dense numpy array
            if hasattr(X_train_transformed, 'toarray'):
                X_train_transformed = X_train_transformed.toarray()
            
            # Pass feature_names directly to the explainer for better labeling
            explainer = shap.Explainer(xgb_model, X_train_transformed, feature_names=feature_names)
            shap_values = explainer(X_train_transformed)
            
            # Ensure shap_values.data is a DataFrame with feature names for summary_plot
            # If it's a numpy array, convert it
            if isinstance(shap_values.data, np.ndarray):
                shap_values.data = pd.DataFrame(shap_values.data, columns=feature_names)

            plt.figure(figsize=(10, 8))
            # Pass feature_names to summary_plot explicitly if shap_values.data is not a DataFrame with columns
            shap.summary_plot(shap_values, X_train_transformed, feature_names=feature_names, show=False)
            plt.tight_layout()
            plt.savefig('plots/modeling/shap_feature_importance.png')
            plt.close()

            # Get top features (using mean absolute SHAP value)
            # Ensure shap_values.values is aligned with feature_names
            if isinstance(shap_values.values, np.ndarray) and shap_values.values.shape[1] == len(feature_names):
                feature_importance = pd.DataFrame({
                    'feature': feature_names,
                    'importance': np.abs(shap_values.values).mean(axis=0)
                }).sort_values('importance', ascending=False)
            else:
                logger.warning("SHAP values and feature names mismatch, falling back to default feature importance if available.")
                # Fallback if SHAP values are not correctly aligned
                if hasattr(xgb_model, 'feature_importances_'):
                    feature_importance = pd.DataFrame({
                        'feature': feature_names,
                        'importance': xgb_model.feature_importances_
                    }).sort_values('importance', ascending=False)
                else:
                    feature_importance = pd.DataFrame() # Empty if no other importance available

            if not feature_importance.empty:
                results['top_features'] = feature_importance.head(10).to_dict('records')
            else:
                 results['top_features'] = "Feature importance analysis failed or no features found."

        except Exception as e:
            logger.warning(f"SHAP analysis failed: {str(e)}")
            results['top_features'] = "Feature importance analysis failed"

    except Exception as e:
        logger.error(f"Model building failed: {str(e)}")
        raise

    return results