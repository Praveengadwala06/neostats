import pyodbc
import pandas as pd
import os

def connect_db():
    # For Azure SQL Database
    server = os.getenv('AZURE_SQL_SERVER', 'your-server.database.windows.net')
    database = os.getenv('AZURE_SQL_DATABASE', 'server_monitoring')
    username = os.getenv('AZURE_SQL_USERNAME', 'your-username')
    password = os.getenv('AZURE_SQL_PASSWORD', 'your-password')
    
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
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
    conn = connect_db()
    cursor = conn.cursor()
    
    # Enable bulk insert for performance
    cursor.fast_executemany = True
    
    insert_query = """
    INSERT INTO server_metrics
    (timestamp,server_id,cpu_usage,memory_usage,disk_usage,network_usage,location,os_type,instance_size,cpu_status,memory_status,alert)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """
    
    data = [
        (
            pd.to_datetime(row['Log_Timestamp']),
            row['Server_ID'],
            row['CPU_Utilization (%)'],
            row['Memory_Usage (%)'],
            row['Disk_IO (%)'],
            row['Network_Traffic_In (MB/s)'],
            row['Server_Location'],
            row['OS_Type'],
            'Standard',
            row['cpu_status'],
            row['memory_status'],
            row['alert']
        )
        for index, row in df.iterrows()
    ]
    
    cursor.executemany(insert_query, data)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data successfully loaded to Azure SQL")
