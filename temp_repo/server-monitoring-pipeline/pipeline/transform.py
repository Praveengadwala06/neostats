import pandas as pd
from sklearn.ensemble import IsolationForest
from logger import log_message

def clean_data(df):

    df = df.drop_duplicates()

    df = df.dropna()

    return df

def cpu_status(cpu):

    if cpu >= 90:
        return "Critical"

    elif cpu >= 70:
        return "High"

    elif cpu >= 50:
        return "Moderate"

    else:
        return "Normal"

def memory_status(memory):

    if memory >= 85:
        return "Critical"

    elif memory >= 65:
        return "Warning"

    else:
        return "Healthy"

def generate_alert(row):

    if row["CPU_Utilization (%)"] > 90:
        return "CPU Critical"

    if row["Memory_Usage (%)"] > 90:
        return "Memory Critical"

    if row["Disk_IO (%)"] > 95:
        return "Disk Critical"

    return "Normal"

def detect_anomalies(df):

    features = df[['CPU_Utilization (%)', 'Memory_Usage (%)', 'Disk_IO (%)']]

    model = IsolationForest(contamination=0.1, random_state=42)

    model.fit(features)

    df['anomaly_score'] = model.decision_function(features)

    df['is_anomaly'] = model.predict(features) == -1

    anomalies_count = df['is_anomaly'].sum()

    log_message(f"Detected {anomalies_count} anomalies")

    print(f"Anomalies detected: {anomalies_count}")

    return df

def correct_anomalies(df):

    for col in ['CPU_Utilization (%)', 'Memory_Usage (%)', 'Disk_IO (%)']:

        median_val = df[col].median()

        df.loc[df['is_anomaly'], col] = median_val

    log_message("Anomalies corrected with median values")

    print("Anomalies corrected")

    return df

def transform_data(df):

    df = clean_data(df)

    df["cpu_status"] = df["CPU_Utilization (%)"].apply(cpu_status)

    df["memory_status"] = df["Memory_Usage (%)"].apply(memory_status)

    df["alert"] = df.apply(generate_alert, axis=1)

    df = detect_anomalies(df)

    df = correct_anomalies(df)

    print("Data transformed")
    return df

def save_processed_data(df):

    df.to_csv("data/processed/processed_logs.csv", index=False)

    print("Processed dataset saved")