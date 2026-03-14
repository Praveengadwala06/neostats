import pyodbc
import pandas as pd
import os

def connect_azure():
    server = os.getenv('AZURE_SQL_SERVER', 'praveensql.database.windows.net')
    database = os.getenv('AZURE_SQL_DATABASE', 'server-monitoring-db')
    username = os.getenv('AZURE_SQL_USERNAME', 'azureadmin')
    password = os.getenv('AZURE_SQL_PASSWORD', 'Praveen@9390')
    
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    return conn

def load_data(df):
    conn = connect_azure()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # Prepare data with proper column mapping and ordering
    insert_query = """
    INSERT INTO server_metrics
    (timestamp,server_id,cpu_usage,memory_usage,disk_usage,network_usage,
    location,os_type,instance_size,cpu_status,memory_status,alert)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """

    # Build tuples in the correct order for SQL INSERT
    data = []
    for _, row in df.iterrows():
        try:
            data.append((
                pd.to_datetime(row['Log_Timestamp']),  # timestamp
                row['Server_ID'],  # server_id
                float(row['CPU_Utilization (%)']),  # cpu_usage
                float(row['Memory_Usage (%)']),  # memory_usage
                float(row['Disk_IO (%)']),  # disk_usage
                float(row['Network_Traffic_In (MB/s)']),  # network_usage
                row['Server_Location'],  # location
                row['OS_Type'],  # os_type
                'Standard',  # instance_size
                row['cpu_status'],  # cpu_status
                row['memory_status'],  # memory_status
                row['alert']  # alert
            ))
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    if data:
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Data loaded to Azure SQL - Inserted {len(data)} records")
    else:
        print("No data to insert")
    
    cursor.close()
    conn.close()