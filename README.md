## Methodology

- **Data Understanding and Profiling:**
    - Initial inspection of the raw dataset structure, column data types, and business context understanding.
    - Verified availability and completeness of key financial and policyholder fields.

- **Comprehensive Data Cleaning:**
    - Parsed and converted date fields into proper datetime formats.
    - Replaced empty strings and invalid placeholders with standardized missing values (`NaN`).
    - Converted financial and numeric fields into consistent data types, handling non-numeric anomalies and zero-value placeholders.
    - Engineered new analytical features including:
        - **VehicleAge** — derived as the difference between transaction year and vehicle registration year.
        - **LossRatio** — calculated as `TotalClaims / TotalPremium` for each policy.

- **Exploratory Data Analysis (EDA):**
    - **Univariate Analysis:**
        - Computed descriptive statistics (mean, median, standard deviation, percentiles).
        - Visualized distributions for key numeric fields using histograms and density plots.
        - Analyzed missing value patterns across all fields.
    - **Bivariate Analysis:**
        - Examined pairwise relationships between target (`TotalClaims`, `LossRatio`) and predictors using barplots, aggregations, and correlation heatmaps.
        - Grouped and analyzed claim severity by key categorical features such as Province, VehicleType, Gender, Make, and Model.
    - **Temporal Analysis:**
        - Aggregated premiums and claims across transaction months to identify seasonal patterns or volatility trends.
    - **Outlier Detection:**
        - Applied statistical thresholds (99th percentile) to identify extreme claim amounts (`TotalClaims`) and insured values (`CustomValueEstimate`) that could influence modeling stability.
    - All EDA visualizations, aggregations, and summaries were automatically generated and version-controlled for reproducibility.


