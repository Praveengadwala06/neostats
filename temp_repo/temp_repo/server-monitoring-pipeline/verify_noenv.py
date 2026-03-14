import pyodbc
print("Testing Azure SQL connection without .env...")

server = 'praveensql.database.windows.net'
database = 'server-monitoring-db'
username = 'azureadmin'
password = 'Praveen@9390'

try:
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
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM server_metrics")
    count = cursor.fetchone()[0]
    print(f"✓ SUCCESS: {count} records found!")
    
    cursor.execute("SELECT TOP 3 server_id, cpu_usage FROM server_metrics ORDER BY id DESC")
    for row in cursor.fetchall():
        print(f"  Server: {row[0][:8]}... CPU: {row[1]:.1f}%")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ FAILED: {e}")

