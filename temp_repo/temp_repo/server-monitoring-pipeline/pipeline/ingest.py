import pandas as pd
from logger import log_message

def ingest_data(file_path):

    try:

        log_message("Starting data ingestion")

        df = pd.read_csv(file_path)

        print("Data loaded successfully")

        log_message("CSV file loaded")

        print(df.head())

        validate_data(df)

        save_raw_data(df)

        return df

    except Exception as e:

        log_message(f"Error occurred: {e}")
        print("Error:", e)

def validate_data(df):

    if df.isnull().sum().sum() > 0:

        print("Warning: Missing values found")

    if (df["CPU_Utilization (%)"] > 100).any():

        print("Invalid CPU values detected")

    if (df["Memory_Usage (%)"] > 100).any():

        print("Invalid memory values detected")

    print("Data validation completed")

def save_raw_data(df):

    df.to_csv("data/processed/raw_backup.csv", index=False)

    print("Raw data backup saved")