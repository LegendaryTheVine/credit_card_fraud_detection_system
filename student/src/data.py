"""Loading and splitting data."""
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "creditcard.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the Kaggle credit card fraud dataset."""
    return pd.read_csv(path)
