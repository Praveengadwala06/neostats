import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Create the server_metrics table in Azure SQL Database"""
    
    server = os.getenv('AZURE_SQL_SERVER', 'praveensql.database.windows.net')
    database = os.getenv('AZURE_SQL_DATABASE', 'server-monitoring-db')
    username = os.getenv('AZURE_SQL_USERNAME', 'azureadmin')
    password = os.getenv('AZURE_SQL_PASSWORD', 'Praveen@9390')
    
    try:
        # Connect to Azure SQL Database
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
        
        # Create table
        create_table_sql = """
        CREATE TABLE server_metrics (
            id INT IDENTITY(1,1) PRIMARY KEY,
            timestamp DATETIME,
            server_id VARCHAR(50),
            cpu_usage FLOAT,
            memory_usage FLOAT,
            disk_usage FLOAT,
            network_usage FLOAT,
            location VARCHAR(50),
            os_type VARCHAR(50),
            instance_size VARCHAR(50),
            cpu_status VARCHAR(20),
            memory_status VARCHAR(20),
            alert VARCHAR(50)
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✓ Table 'server_metrics' created successfully!")
        
        cursor.close()
        conn.close()
        
    except pyodbc.Error as e:
        print(f"✗ Database error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Setting up Azure SQL Database...")
    setup_database()