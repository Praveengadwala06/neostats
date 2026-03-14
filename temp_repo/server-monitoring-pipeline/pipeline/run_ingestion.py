from ingest import ingest_data
from transform import transform_data, save_processed_data
from load_azure import load_data

file_path = "data/raw/server_logs.csv"

df = ingest_data(file_path)

df = transform_data(df)

save_processed_data(df)

load_data(df)

print("Pipeline completed successfully")