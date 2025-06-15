import pandas as pd


def load_data(filepath):
    df = pd.read_csv(filepath, sep='|', low_memory=False)
    return df
