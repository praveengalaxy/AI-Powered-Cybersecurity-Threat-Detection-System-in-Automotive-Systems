import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    """
    Preprocess dataset:
    - Drops "Timestamp" column if present.
    - Encodes categorical columns using category codes (avoiding unseen label issues).
    - Scales numerical features using StandardScaler.
    """
    print("Preprocessing data...")

    # Drop 'Timestamp' column if it exists
    df = df.drop(columns=["Timestamp"], errors="ignore")

    # Identify categorical columns (object type)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Apply label encoding using category codes
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes

    # Apply StandardScaler to numerical columns
    scaler = StandardScaler()
    df[df.columns] = scaler.fit_transform(df[df.columns])

    print("Preprocessing complete.")
    return df
