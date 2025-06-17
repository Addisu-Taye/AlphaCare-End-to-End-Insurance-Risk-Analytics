# 🚀 Insurance Risk Analytics & Predictive Modeling

An end-to-end analytics pipeline to identify low-risk insurance segments and build predictive pricing models.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Methodology](#-methodology)
- [Folder Structure](#-folder-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output Files](#-output-files)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

This project analyzes historical car insurance data from **AlphaCare Insurance Solutions (ACIS)** to optimize marketing strategies and identify low-risk customer segments where premiums can be reduced.

The analysis includes:

- Exploratory Data Analysis (EDA)
- Hypothesis Testing
- Statistical Modeling
- Machine Learning Prediction of Claim Severity and Optimal Premium
- Dynamic Word Report Generation

All steps are version-controlled using **DVC** for reproducibility and compliance with financial industry standards.

---

## 🛠️ Methodology

### 1. Data Loading & Cleaning
- Loaded `sample_data.txt` using **Pandas**
- Handled missing values, outliers, and invalid entries
- Cleaned and converted relevant columns

### 2. Exploratory Data Analysis (EDA)
- Calculated **Loss Ratio**: `Claims / Premiums`
- Visualized trends by **province**, **gender**, and **vehicle type**
- Identified **high-risk** and **low-risk** segments

### 3. Hypothesis Testing
- Tested risk difference hypotheses across:
  - Provinces
  - Zipcodes
  - Margin between zipcodes
  - Genders
- Used **Chi-Square**, **T-Tests**, and **ANOVA**

### 4. Statistical & Machine Learning Modeling
- Models built: **Linear Regression**, **Random Forest**, **XGBoost**
- Evaluation metrics: **RMSE**, **R² Score**
- **XGBoost** selected as best-performing model

### 5. Model Interpretation
- Used **SHAP** values to explain feature importance

### 6. Dynamic Report Generation
- Created a professional **Word (.docx)** report with embedded visualizations

---

## 📁 Folder Structure

AlphaCare-End-to-End-Insurance-Risk-Analytics/
├── data/
│ └── raw/
│ └── raw_data.txt # Raw dataset
├── reports/
│ ├── images/ # Auto-generated visualizations
│ 
├── plors/
├── README.md # This file
├── requirements.txt # Required libraries
└── .gitignore # Git ignored files



---

## ⚙️ Requirements

Ensure you have:

- Python 3.8+
- pip

### 📦 Libraries Used

```bash
pandas numpy matplotlib seaborn scikit-learn xgboost python-docx shap dvc
Install them with:

bash
Copy
Edit
pip install -r requirements.txt
🚀 Installation
Step-by-step Setup
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/insurance-analytics.git
cd insurance-analytics
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Place your dataset:

Copy your sample_data.txt to the data/raw/ folder.

Run the analysis and generate the report:

bash
Copy
Edit
python generate_report.py
Open the generated report:

Navigate to reports/insurance_analytics_report.docx

📄 Output Files
After execution, you will find:

reports/images/loss_ratio_by_province.png – Loss ratio chart

reports/images/shap_feature_importance.png – SHAP feature importance

reports/insurance_analytics_report.docx – Full insights and visuals in Word format

🤝 Contributing
Contributions are welcome! Follow these steps:

bash
Copy
Edit
# Fork and clone the repo
# Create a new branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m 'Add new feature'

# Push your branch
git push origin feature/your-feature-name

# Open a Pull Request
📄 License
MIT License – see LICENSE
