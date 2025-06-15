import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + '/../')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw/raw_data.txt')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
