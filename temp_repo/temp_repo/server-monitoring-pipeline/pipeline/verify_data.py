import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_data():
    """Verify data in Azure SQL Database"""
    
    server = os.getenv('AZURE_SQL_SERVER', 'praveensql.database.windows.net')
    database = os.getenv('AZURE_SQL_DATABASE', 'server-monitoring-db')
    username = os.getenv('AZURE_SQL_USERNAME', 'azureadmin')
    password = os.getenv('AZURE_SQL_PASSWORD', 'Praveen@9390')
    
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
        
        # Count total records
        cursor.execute("SELECT COUNT(*) as record_count FROM server_metrics")
        count = cursor.fetchone()[0]
        print(f"✓ Total records in database: {count}")
        
        # Show sample records
        print("\n✓ Sample data from server_metrics table:")
        cursor.execute("""
        SELECT TOP 5 
            server_id, cpu_usage, memory_usage, cpu_status, memory_status, alert
        FROM server_metrics
        ORDER BY id DESC
        """)
        
        results = cursor.fetchall()
        for row in results:
            print(f"  Server: {row[0]}, CPU: {row[1]:.2f}%, Memory: {row[2]:.2f}%, Status: {row[3]}, Alert: {row[5]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    verify_data()